# -*- coding: utf-8 -*-
# 带性格选择的心理咨询师主程序
# 支持三种性格：幽默、温柔、专业
# 集成 NAO 动作和语音交互

import os
import sys
import json
import io
import time
import requests
import threading

# 导入性格配置
from personality_config import (
    get_personality_config, get_system_prompt, 
    list_personalities, COUNSELING_STAGES
)

# 导入 NAO SDK 和动作
from nao_sdk_helper import setup_naoqi_sdk
from nao_motions import (
    get_nao_proxies, wake_up, stand_init,
    select_action_by_text, perform_action_during_speech,
    gentle_nod, greeting_action, closing_action
)

# 设置 SDK
if not setup_naoqi_sdk():
    print("Warning: NAOqi SDK not found, NAO features will be disabled")

try:
    from naoqi import ALProxy
except ImportError:
    try:
        from qi import naoqi
        ALProxy = naoqi.ALProxy
    except ImportError:
        ALProxy = None

# SoulChat2.0 API 配置
SOULCHAT_API_KEY = os.getenv('SOULCHAT_API_KEY', 'soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30')
SOULCHAT_BASE_URL = os.getenv('SOULCHAT_BASE_URL', 'http://localhost:8001/v1')
SOULCHAT_MODEL_NAME = os.getenv('SOULCHAT_MODEL_NAME', 'SoulChat2.0-Llama-3.1-8B')

# 会话文件
SESSION_FILE = './counseling_session.json'

def uprint(s):
    """安全的Unicode打印函数"""
    try:
        if isinstance(s, unicode):
            sys.stdout.write((s + u"\n").encode('utf-8'))
        else:
            sys.stdout.write(unicode(s, 'utf-8', 'ignore').encode('utf-8') + "\n")
    except Exception:
        try:
            sys.stdout.write(str(s) + "\n")
        except Exception:
            pass
    sys.stdout.flush()

def load_session():
    """加载会话状态"""
    if os.path.exists(SESSION_FILE):
        try:
            with io.open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        'personality': None,
        'stage': 0,
        'conversation_history': [],
        'user_info': {},
        'started': False,
        'finished': False
    }

def save_session(session):
    """保存会话状态"""
    with io.open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

def select_personality():
    """选择性格"""
    uprint(u"\n" + "=" * 60)
    uprint(u"请选择心理咨询师的性格：")
    uprint("=" * 60)
    
    personalities = list_personalities()
    for i, p in enumerate(personalities, 1):
        config = get_personality_config(p)
        uprint(u"%d. %s - %s" % (i, config['name'], config['description']))
    
    uprint("=" * 60)
    
    while True:
        try:
            choice = raw_input(u"\n请输入选项 (1-%d): " % len(personalities)).strip()
            idx = int(choice) - 1
            if 0 <= idx < len(personalities):
                selected = personalities[idx]
                config = get_personality_config(selected)
                uprint(u"\n✓ 已选择：%s" % config['name'])
                uprint(u"  %s\n" % config['description'])
                return selected
            else:
                uprint(u"无效选项，请重新输入")
        except (ValueError, KeyboardInterrupt):
            uprint(u"\n取消选择")
            sys.exit(0)

def get_llm_response(personality, stage, user_input, conversation_history):
    """获取 LLM 响应"""
    # 生成系统提示词
    system_prompt = get_system_prompt(personality, stage, conversation_history)
    
    # 构建消息列表
    messages = [{"role": "system", "content": system_prompt}]
    
    # 添加对话历史（最近3轮）
    for msg in conversation_history[-3:]:
        messages.append({"role": "user", "content": msg['user']})
        messages.append({"role": "assistant", "content": msg['assistant']})
    
    # 添加当前用户输入
    messages.append({"role": "user", "content": user_input})
    
    # 构建请求
    payload = {
        "model": SOULCHAT_MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    headers = {
        'Authorization': 'Bearer %s' % SOULCHAT_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # 发送请求
    resp = None
    for attempt in range(3):
        try:
            resp = requests.post(
                '%s/chat/completions' % SOULCHAT_BASE_URL,
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                timeout=(10, 60)
            )
            if resp.status_code == 200:
                break
        except Exception as e:
            if attempt == 2:
                uprint(u"[错误] 无法连接到 SoulChat2.0 服务: %s" % str(e))
                return None
            time.sleep(2 * (attempt + 1))
    
    if resp is None or resp.status_code != 200:
        uprint(u"[错误] SoulChat2.0 API 错误: %s" % resp.status_code if resp else "无响应")
        return None
    
    try:
        data = resp.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        uprint(u"[错误] 解析响应失败: %s" % str(e))
        return None

def speak_with_actions(tts, text, motion, animation, personality):
    """说话并执行动作"""
    if tts is None:
        uprint(text)
        return
    
    try:
        text_u = text if isinstance(text, unicode) else unicode(text, 'utf-8', 'ignore')
    except:
        text_u = unicode(text)
    
    # 设置语言
    try:
        has_non_ascii = any(ord(c) > 127 for c in text_u)
        if has_non_ascii:
            tts.setLanguage('Chinese')
        else:
            tts.setLanguage('English')
    except:
        pass
    
    # 估算说话时长
    text_length = len(text_u)
    estimated_duration = text_length / 3.0 if has_non_ascii else text_length / 5.0
    estimated_duration = max(2.0, min(estimated_duration, 15.0))
    
    # 根据性格调整动作
    if motion is not None:
        # 说话前执行动作
        try:
            # 根据性格和文本选择动作
            select_action_by_text(text_u, motion, animation, personality)
            time.sleep(0.3)
        except Exception as e:
            print("Action error: %s" % e)
        
        # 在说话期间执行动作（后台线程）
        def action_thread():
            try:
                perform_action_during_speech(text_u, motion, animation, estimated_duration, personality)
            except:
                pass
        
        action_t = threading.Thread(target=action_thread)
        action_t.daemon = True
        action_t.start()
    
    # 执行 TTS
    try:
        tts.say(text_u.encode('utf-8'))
    except Exception as e:
        uprint(u"[错误] TTS 失败: %s" % str(e))
        uprint(text_u)
        return
    
    # 等待说话完成
    time.sleep(max(estimated_duration, 2))
    
    # 说话后的动作
    if motion is not None:
        try:
            gentle_nod(motion, 1)
        except:
            pass

def main():
    """主程序"""
    uprint(u"\n" + "=" * 60)
    uprint(u"NAO 心理咨询师系统")
    uprint("=" * 60)
    
    # 加载会话
    session = load_session()
    
    # 选择性格（如果未选择）
    if session.get('personality') is None:
        personality = select_personality()
        session['personality'] = personality
        save_session(session)
    else:
        personality = session['personality']
        config = get_personality_config(personality)
        uprint(u"\n当前性格: %s" % config['name'])
        uprint(u"如需更换，请删除会话文件: %s\n" % SESSION_FILE)
    
    # 初始化 NAO
    nao_ip = os.environ.get('NAO_IP', "192.168.10.3")
    nao_port = int(os.environ.get('NAO_PORT', '9559'))
    
    tts = None
    motion = None
    animation = None
    posture = None
    
    if ALProxy is not None:
        try:
            tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
            tts.getVolume()  # 测试连接
            uprint(u"✓ 已连接到 NAO 机器人 (IP: %s)" % nao_ip)
            
            # 初始化动作系统
            motion, animation, posture = get_nao_proxies()
            if motion is not None:
                try:
                    wake_up(motion)
                    stand_init(posture)
                except:
                    pass
        except Exception as e:
            uprint(u"⚠ 无法连接到 NAO 机器人: %s" % str(e))
            uprint(u"将使用文本模式")
            tts = None
    
    # 开场白
    if not session['started']:
        config = get_personality_config(personality)
        greeting = config['greeting']
        
        # 执行开场动作
        if motion is not None:
            try:
                greeting_action(motion, animation)
            except:
                pass
        
        # 说话
        speak_with_actions(tts, greeting, motion, animation, personality)
        
        session['started'] = True
        session['stage'] = 0
        save_session(session)
    
    # 主对话循环
    uprint(u"\n" + "-" * 60)
    uprint(u"对话开始（输入 'quit' 或 'exit' 退出）")
    uprint("-" * 60 + "\n")
    
    while not session['finished']:
        try:
            # 获取用户输入
            user_input = raw_input(u"您: ").strip()
            
            if not user_input:
                continue
            
            # 检查终止规则（支持多种终止关键词）
            termination_keywords = ['quit', 'exit', '退出', '结束', '回答完毕', '完毕']
            if any(keyword in user_input for keyword in termination_keywords):
                # 立即跳转到结束阶段
                session['stage'] = 8
                session['finished'] = True
                save_session(session)
                
                # 结束语
                config = get_personality_config(personality)
                closing = config['closing']
                
                if motion is not None:
                    try:
                        closing_action(motion)
                    except:
                        pass
                
                speak_with_actions(tts, closing, motion, animation, personality)
                break
            
            # 获取 LLM 响应
            uprint(u"\nNAO 正在思考...")
            response = get_llm_response(
                personality,
                session['stage'],
                user_input,
                session['conversation_history']
            )
            
            if response is None:
                uprint(u"[错误] 无法获取响应，请检查 SoulChat2.0 服务")
                continue
            
            # 更新会话
            session['conversation_history'].append({
                'user': user_input,
                'assistant': response,
                'stage': session['stage']
            })
            
            # 阶段推进逻辑（由 LLM 根据 prompt 中的流程控制，这里只做简单辅助）
            # 注意：主要的阶段控制应该由 LLM 根据 prompt 中的 Dialogue Phases 来执行
            # 这里只做基本的阶段跟踪，不强制推进
            
            # 如果到达结束阶段，标记完成
            if session['stage'] >= 8:
                session['finished'] = True
                # 自动执行结束语
                config = get_personality_config(personality)
                closing = config['closing']
                
                if motion is not None:
                    try:
                        closing_action(motion)
                    except:
                        pass
                
                speak_with_actions(tts, closing, motion, animation, personality)
                break
            
            save_session(session)
            
            # NAO 说话
            uprint(u"\nNAO: ", end='')
            speak_with_actions(tts, response, motion, animation, personality)
            uprint("")
            
        except KeyboardInterrupt:
            uprint(u"\n\n对话已中断")
            break
        except Exception as e:
            uprint(u"[错误] %s" % str(e))
            import traceback
            traceback.print_exc()
    
    uprint(u"\n感谢使用 NAO 心理咨询师系统！")

if __name__ == '__main__':
    main()

