# -*- coding: utf-8 -*-
# 带性格选择的心理咨询师主程序 - DeepSeek API 版本
# 支持两种性格：专业评估、共情
# 集成 NAO 动作和语音交互

import os
import sys
import json
import io
import time
import requests
import threading
import base64
import tempfile

# 抑制 SSL 警告（因为使用 verify=False 进行开发环境测试）
import warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

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
    gentle_nod
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

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-d93e850223e548578946315a173c6b70')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
DEEPSEEK_MODEL_NAME = os.getenv('DEEPSEEK_MODEL_NAME', 'deepseek-chat')

# 百度语音识别 API 配置（可选，用于显示用户说的话）
BAIDU_ASR_API_KEY = os.getenv('BAIDU_ASR_API_KEY', 'we9cxZ31lcySBTow6G6cqUqm')
BAIDU_ASR_SECRET = os.getenv('BAIDU_ASR_SECRET', 'pUwUWRWj6yKEdiee1y3ijS8LnPdiDoSw')
BAIDU_ASR_DEV_PID = int(os.getenv('BAIDU_ASR_DEV_PID', '1537'))  # 1537 = 中文普通话

# NAO SFTP 配置（用于下载录音文件）
NAO_USERNAME = os.getenv('NAO_USERNAME', 'nao')
NAO_PASSWORD = os.getenv('NAO_PASSWORD', 'nao')

# 本地音频文件目录
LOCAL_AUDIO_DIR = os.path.expanduser('~/nao_audio')
if not os.path.exists(LOCAL_AUDIO_DIR):
    os.makedirs(LOCAL_AUDIO_DIR)

# 会话文件
SESSION_FILE = './counseling_session.json'

def uprint(s, end='\n'):
    """安全的Unicode打印函数"""
    try:
        if isinstance(s, unicode):
            sys.stdout.write(s.encode('utf-8'))
        else:
            sys.stdout.write(unicode(s, 'utf-8', 'ignore').encode('utf-8'))
        if end:
            sys.stdout.write(end.encode('utf-8') if isinstance(end, unicode) else end)
    except Exception:
        try:
            sys.stdout.write(str(s))
            if end:
                sys.stdout.write(end)
        except Exception:
            pass
    sys.stdout.flush()

def load_session():
    """加载会话状态"""
    if os.path.exists(SESSION_FILE):
        try:
            with io.open(SESSION_FILE, 'r', encoding='utf-8') as f:
                session = json.load(f)
                # 确保 question_index 存在
                if 'question_index' not in session:
                    session['question_index'] = 0
                
                # 兼容旧版本的性格类型，自动转换
                personality_mapping = {
                    'humorous': 'professional',  # 旧版本：幽默 -> 新版本：专业评估
                    'gentle': 'empathetic'       # 旧版本：温柔 -> 新版本：共情
                }
                
                if 'personality' in session and session['personality'] in personality_mapping:
                    old_personality = session['personality']
                    session['personality'] = personality_mapping[old_personality]
                    # 保存更新后的会话
                    save_session(session)
                    uprint(u"[提示] 已自动将性格类型从 '%s' 更新为 '%s'" % (old_personality, session['personality']))
                
                return session
        except:
            pass
    return {
        'personality': None,
        'stage': 0,
        'question_index': 0,
        'conversation_history': [],
        'user_info': {},
        'started': False,
        'finished': False
    }

def save_session(session):
    """保存会话状态"""
    try:
        # 确保所有字符串都是unicode
        def ensure_unicode_recursive(obj):
            if isinstance(obj, dict):
                return {ensure_unicode(k): ensure_unicode_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [ensure_unicode_recursive(item) for item in obj]
            elif isinstance(obj, str):
                return obj.decode('utf-8', 'ignore')
            elif isinstance(obj, unicode):
                return obj
            else:
                return obj
        
        def ensure_unicode(s):
            if isinstance(s, str):
                return s.decode('utf-8', 'ignore')
            return s
        
        # 递归处理会话数据
        session_unicode = ensure_unicode_recursive(session)
        
        # 转换为 JSON 字符串
        json_str = json.dumps(session_unicode, ensure_ascii=False, indent=2)
        
        # 确保是unicode字符串
        if isinstance(json_str, str):
            json_str = json_str.decode('utf-8', 'ignore')
        
        # 写入文件
        with io.open(SESSION_FILE, 'w', encoding='utf-8') as f:
            f.write(json_str)
    except Exception as e:
        uprint(u"[警告] 保存会话失败: %s" % str(e))
        import traceback
        traceback.print_exc()

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
            # 使用 ASCII 字符串提示，避免 Unicode 问题
            sys.stdout.write("\n请输入选项 (1-%d): " % len(personalities))
            sys.stdout.flush()
            
            # 读取输入
            try:
                choice_str = raw_input()
            except (EOFError, KeyboardInterrupt):
                uprint(u"\n取消选择")
                sys.exit(0)
            
            if not choice_str:
                uprint(u"请输入有效选项")
                continue
            
            choice_str = choice_str.strip()
            try:
                idx = int(choice_str) - 1
            except ValueError:
                uprint(u"请输入数字")
                continue
                
            if 0 <= idx < len(personalities):
                selected = personalities[idx]
                config = get_personality_config(selected)
                uprint(u"\n✓ 已选择：%s" % config['name'])
                uprint(u"  %s\n" % config['description'])
                return selected
            else:
                uprint(u"无效选项，请输入 1-%d" % len(personalities))
        except Exception as e:
            uprint(u"输入错误: %s" % str(e))
            continue

def get_baidu_token():
    """获取百度语音识别 Token"""
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_ASR_API_KEY,
        "client_secret": BAIDU_ASR_SECRET
    }
    try:
        response = requests.get(token_url, params=params, timeout=10, verify=False)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        return None
    except Exception as e:
        uprint(u"[错误] 获取百度 Token 失败: %s" % str(e))
        return None

def speech_to_text_baidu(audio_file_path):
    """使用百度 API 进行语音识别"""
    try:
        # 读取音频文件
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
            base64_data = base64.b64encode(audio_data)
        
        # 获取 Token
        token = get_baidu_token()
        if not token:
            return None
        
        # 调用百度语音识别 API
        url = "https://vop.baidu.com/server_api"
        data = {
            "format": "wav",
            "rate": 16000,
            "channel": 1,
            "cuid": "nao_robot",
            "token": token,
            "dev_pid": BAIDU_ASR_DEV_PID,
            "speech": base64_data,
            "len": len(audio_data)
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers, timeout=10, verify=False)
        
        if response.status_code != 200:
            return None
        
        result_json = response.json()
        
        # 检查错误
        if 'error_code' in result_json:
            return None
        
        # 返回识别结果（确保返回 unicode）
        if 'result' in result_json and result_json['result']:
            result_text = result_json["result"][0]
            # 确保返回 unicode
            if isinstance(result_text, str):
                return result_text.decode('utf-8', 'ignore')
            elif isinstance(result_text, unicode):
                return result_text
            else:
                return unicode(result_text, 'utf-8', 'ignore')
        return None
            
    except Exception as e:
        uprint(u"[错误] 语音识别失败: %s" % str(e))
        return None

def transfer_audio_from_nao(remote_path, local_path, nao_ip):
    """通过 SFTP 从 NAO 传输音频文件"""
    if not PARAMIKO_AVAILABLE:
        uprint(u"[提示] paramiko 未安装，无法传输音频文件")
        uprint(u"[提示] 请安装: pip install paramiko")
        return False
    
    try:
        # 创建 SFTP 连接
        transport = paramiko.Transport((nao_ip, 22))
        transport.connect(username=NAO_USERNAME, password=NAO_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 下载文件
        sftp.get(remote_path, local_path)
        
        # 关闭连接
        sftp.close()
        transport.close()
        
        return True
    except Exception as e:
        uprint(u"[错误] 文件传输失败: %s" % str(e))
        return False

def get_llm_response(personality, stage, user_input, conversation_history, question_index=0):
    """获取 LLM 响应 - 使用 DeepSeek API（使用三个性格的系统提示词）"""
    # 生成系统提示词（使用 personality_config.py 中的三个性格提示词）
    system_prompt = get_system_prompt(personality, stage, conversation_history, question_index)
    
    # 确保所有字符串都是 unicode
    def ensure_unicode(s):
        if isinstance(s, str):
            return s.decode('utf-8', 'ignore')
        return s
    
    # 构建消息列表
    messages = [{"role": "system", "content": ensure_unicode(system_prompt)}]
    
    # 添加对话历史（最近3轮）
    for msg in conversation_history[-3:]:
        user_msg = ensure_unicode(msg.get('user', ''))
        assistant_msg = ensure_unicode(msg.get('assistant', ''))
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    # 添加当前用户输入
    messages.append({"role": "user", "content": ensure_unicode(user_input)})
    
    # 构建请求
    payload = {
        "model": DEEPSEEK_MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    headers = {
        'Authorization': 'Bearer %s' % DEEPSEEK_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # 发送请求
    resp = None
    last_error = None
    for attempt in range(3):
        try:
            # 确保 JSON 编码正确
            payload_json = json.dumps(payload, ensure_ascii=False)
            if isinstance(payload_json, unicode):
                payload_bytes = payload_json.encode('utf-8')
            else:
                payload_bytes = payload_json
            
            resp = requests.post(
                '%s/chat/completions' % DEEPSEEK_BASE_URL,
                headers=headers,
                data=payload_bytes,
                timeout=(5, 30)  # 减少超时时间：连接5秒，读取30秒
            )
            if resp.status_code == 200:
                break
            else:
                last_error = "HTTP %d" % resp.status_code
        except UnicodeDecodeError as e:
            last_error = "编码错误: %s" % str(e)
            if attempt == 2:
                uprint(u"[错误] 编码问题: %s" % str(e))
                return None
        except Exception as e:
            last_error = str(e)
            if attempt == 2:
                # 安全地显示错误信息
                try:
                    error_msg = unicode(str(e), 'utf-8', 'ignore')
                except:
                    error_msg = str(e)
                uprint(u"[错误] 无法连接到 DeepSeek API: %s" % error_msg)
                return None
            time.sleep(2 * (attempt + 1))
    
    if resp is None:
        uprint(u"[错误] DeepSeek API 无响应")
        return None
        
    if resp.status_code != 200:
        try:
            error_detail = resp.text[:200]
            uprint(u"[错误] DeepSeek API 错误: HTTP %d" % resp.status_code)
            uprint(u"详情: %s" % error_detail)
        except:
            uprint(u"[错误] DeepSeek API 错误: HTTP %d" % resp.status_code)
        return None
    
    try:
        data = resp.json()
        response_text = data['choices'][0]['message']['content']
        # 确保返回 unicode
        if isinstance(response_text, str):
            return response_text.decode('utf-8', 'ignore')
        return response_text
    except Exception as e:
        uprint(u"[错误] 解析响应失败: %s" % str(e))
        return None

def record_audio_after_speech(audio_recorder, duration=10, nao_ip=None, motion=None, personality=None):
    """在说话后录制音频，并自动识别显示（立即开始，无延迟）"""
    if audio_recorder is None:
        uprint(u"[提示] 音频录制功能未启用")
        return None
    
    try:
        # 停止之前的录音（如果有），参考用户提供的代码
        try:
            audio_recorder.stopMicrophonesRecording()
            # 不等待，立即开始新的录音（参考用户提供的代码，没有延迟）
        except Exception as e:
            # 如果没有正在进行的录音，忽略错误
            pass
        
        # 创建临时文件路径（在NAO机器人上）
        # 使用NAO机器人的/home/nao目录，这个目录通常有写权限
        remote_path = "/home/nao/nao_recording_%d.wav" % int(time.time())
        
        uprint(u"\n[开始录音，请说话...（%d秒）]" % duration)
        
        # 立即开始录音（不等待，参考用户提供的代码）
        audio_recorder.startMicrophonesRecording(
            remote_path,
            "wav",
            16000,
            [1, 0, 0, 0]  # 使用前左麦克风
        )
        
        # 在录音期间只做头部动作，停止所有身体动作
        if motion is not None:
            try:
                # 停止所有正在执行的动作
                # 方法1: 停止所有关节的运动
                try:
                    motion.stopMove()  # 停止所有移动
                except:
                    pass
                
                # 方法2: 设置身体关节刚度为0，只保留头部关节
                # 这样可以防止身体动作执行，但允许头部动作
                body_joints = [
                    "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
                    "LHipPitch", "LHipRoll", "LKneePitch", "LAnklePitch", "LAnkleRoll",
                    "RHipPitch", "RHipRoll", "RKneePitch", "RAnklePitch", "RAnkleRoll",
                    "HipRoll", "HipPitch"
                ]
                # 停止身体所有关节
                stiffnesses = [0.0] * len(body_joints)
                motion.setStiffnesses(body_joints, stiffnesses)
                
                # 确保头部关节可用
                head_joints = ["HeadPitch", "HeadYaw"]
                motion.setStiffnesses(head_joints, [1.0, 1.0])
                
                time.sleep(0.2)  # 短暂等待，确保动作停止
                
                # 在录音期间只做头部动作（后台线程）
                from nao_motions import perform_head_actions_during_recording
                perform_head_actions_during_recording(motion, duration, personality)
            except Exception as e:
                uprint(u"[提示] 停止身体动作失败: %s" % str(e))
        
        # 等待录音完成
        uprint(u"[正在录音中...]")
        for i in range(duration):
            time.sleep(1)
            if (i + 1) % 2 == 0:
                uprint(u"[剩余时间: %d秒]" % (duration - i - 1))
        
        # 停止录音
        audio_recorder.stopMicrophonesRecording()
        time.sleep(0.5)  # 等待文件写入完成
        
        # 录音结束后，恢复所有关节的刚度
        if motion is not None:
            try:
                # 恢复身体所有关节的刚度
                body_joints = [
                    "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
                    "LHipPitch", "LHipRoll", "LKneePitch", "LAnklePitch", "LAnkleRoll",
                    "RHipPitch", "RHipRoll", "RKneePitch", "RAnklePitch", "RAnkleRoll",
                    "HipRoll", "HipPitch"
                ]
                stiffnesses = [1.0] * len(body_joints)
                motion.setStiffnesses(body_joints, stiffnesses)
                
                # 确保头部关节也保持可用
                head_joints = ["HeadPitch", "HeadYaw"]
                motion.setStiffnesses(head_joints, [1.0, 1.0])
            except Exception as e:
                uprint(u"[提示] 恢复身体动作失败: %s" % str(e))
        
        uprint(u"[录音完成]")
        
        # 尝试识别语音并显示
        if nao_ip and PARAMIKO_AVAILABLE:
            uprint(u"[正在识别语音...]")
            local_audio_path = os.path.join(LOCAL_AUDIO_DIR, 'audio_%d.wav' % int(time.time()))
            
            # 传输音频文件
            if transfer_audio_from_nao(remote_path, local_audio_path, nao_ip):
                # 语音识别
                recognized_text = speech_to_text_baidu(local_audio_path)
                
                if recognized_text:
                    uprint(u"\n" + "=" * 60)
                    uprint(u"您说: %s" % recognized_text)
                    uprint("=" * 60)
                    
                    # 清理本地音频文件
                    try:
                        if os.path.exists(local_audio_path):
                            os.remove(local_audio_path)
                    except:
                        pass
                    
                    return recognized_text
                else:
                    uprint(u"[提示] 未能识别到语音内容")
            else:
                uprint(u"[提示] 无法传输音频文件，跳过语音识别")
        else:
            if not PARAMIKO_AVAILABLE:
                uprint(u"[提示] paramiko 未安装，无法进行语音识别")
                uprint(u"[提示] 录音文件已保存到: %s" % remote_path)
        
        return remote_path
        
    except Exception as e:
        uprint(u"[错误] 录音失败: %s" % str(e))
        import traceback
        traceback.print_exc()
        return None

def speak_with_actions(tts, text, motion, animation, personality, audio_recorder=None, auto_record=False):
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
    
    # 在说话过程中执行动作
    if motion is not None:
        # 说话开始时立即触发一个动作
        try:
            if personality == 'empathetic':
                # 共情性格：开始时使用共情动作（点头、歪头、挥手、拥抱、拍肩、抚摸、心口轻触、礼物呈递）
                import random
                from nao_motions import (
                    gentle_slow_nod, empathetic_gentle_tilt, gentle_wave,
                    empathetic_hug, empathetic_pat_shoulder, empathetic_stroke,
                    empathetic_heart_touch, empathetic_gift_presentation
                )
                empathetic_start_actions = [
                    gentle_slow_nod,  # 点头
                    empathetic_gentle_tilt,  # 歪头（轻微）
                    gentle_wave,  # 挥手
                    empathetic_hug,  # 拥抱
                    empathetic_pat_shoulder,  # 拍肩膀
                    empathetic_stroke,  # 抚摸
                    empathetic_heart_touch,  # 心口轻触
                    empathetic_gift_presentation  # 礼物呈递
                ]
                action = random.choice(empathetic_start_actions)
                action(motion)
            elif personality == 'professional':
                # 专业性格：开始时使用点头或挥手
                import random
                from nao_motions import professional_small_nod, gentle_wave
                if random.random() < 0.5:
                    professional_small_nod(motion)
                else:
                    gentle_wave(motion)
            else:
                # 默认：轻微点头
                from nao_motions import gentle_nod
                gentle_nod(motion, 1)
        except Exception as e:
            pass
        
        # 在说话期间持续执行动作（后台线程）
        def action_thread():
            try:
                perform_action_during_speech(text_u, motion, animation, estimated_duration, personality)
            except:
                pass
        
        action_t = threading.Thread(target=action_thread)
        action_t.daemon = True
        action_t.start()
    
    # 执行 TTS（异步，不阻塞）
    try:
        tts.say(text_u.encode('utf-8'))
    except Exception as e:
        uprint(u"[错误] TTS 失败: %s" % str(e))
        uprint(text_u)
        return
    
    # TTS是异步的，不需要等待，立即返回
        # 如果启用了自动录音，在TTS开始后立即开始录音（不等待TTS完成）
        if auto_record and audio_recorder is not None:
            # 立即开始录音，不等待TTS完成（参考用户提供的代码，TTS是异步的，录音可以立即开始）
            nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
            # 在后台线程中录音，避免阻塞
            def start_recording():
                record_audio_after_speech(audio_recorder, duration=10, nao_ip=nao_ip, motion=motion, personality=personality)
            recording_t = threading.Thread(target=start_recording)
            recording_t.daemon = True
            recording_t.start()

def main():
    """主程序"""
    uprint(u"\n" + "=" * 60)
    uprint(u"NAO 心理咨询师系统（DeepSeek API 版本）")
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
    nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
    nao_port = int(os.environ.get('NAO_PORT', '9559'))
    
    tts = None
    motion = None
    animation = None
    posture = None
    audio_recorder = None
    
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
            
            # 初始化音频录制
            try:
                audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
                uprint(u"✓ 音频录制功能已启用")
            except Exception as e:
                uprint(u"⚠ 无法初始化音频录制: %s" % str(e))
                audio_recorder = None
        except Exception as e:
            uprint(u"⚠ 无法连接到 NAO 机器人: %s" % str(e))
            uprint(u"将使用文本模式")
            tts = None
    
    # 开场白
    if not session.get('started', False):
        config = get_personality_config(personality)
        greeting = config['greeting']
        
        # 执行开场动作（根据性格）
        if motion is not None:
            try:
                if personality == 'professional':
                    # 专业评估性格：挥手+点头
                    from nao_motions import gentle_wave, professional_small_nod
                    gentle_wave(motion)
                    time.sleep(0.3)
                    professional_small_nod(motion)
                else:  # empathetic
                    # 共情性格：挥手+轻微点头
                    from nao_motions import gentle_wave, gentle_slow_nod
                    gentle_wave(motion)
                    time.sleep(0.3)
                    gentle_slow_nod(motion)
            except Exception as e:
                uprint(u"[提示] 开场动作执行失败: %s" % str(e))
        
        # 说话（说话过程中会做动作，但说话前后不做额外动作）
        speak_with_actions(tts, greeting, motion, animation, personality, audio_recorder, auto_record=False)
        
        session['started'] = True
        session['stage'] = 1  # 开场后进入问题阶段
        session['question_index'] = 0
        save_session(session)
        
        # 开场白后，立即问第一个问题（不重复开场白）
        from personality_config import COUNSELING_QUESTIONS
        
        # 直接使用第一个问题，不通过LLM生成（避免重复开场白）
        if session['question_index'] < len(COUNSELING_QUESTIONS):
            first_question = COUNSELING_QUESTIONS[session['question_index']]
            
            # 根据性格添加前缀
            if personality == 'professional':
                question_prefix = u"那我们开始第一个问题。"
            else:  # empathetic
                question_prefix = u"让我们开始第一个问题。"
            
            first_question_response = question_prefix + first_question
            
            uprint(u"\nNAO: ", end='')
            # 问完问题后立即开始录音
            speak_with_actions(tts, first_question_response, motion, animation, personality, audio_recorder, auto_record=False)
            uprint("")
            
            # 记录第一个问题的响应
            session['conversation_history'].append({
                'user': u"开始",
                'assistant': first_question_response,
                'stage': session['stage'],
                'question_index': session['question_index']
            })
            save_session(session)
            
            # 问完第一个问题后立即开始录音（不等待，立即开始）
            if audio_recorder is not None:
                nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
                recognized_text = record_audio_after_speech(audio_recorder, duration=10, nao_ip=nao_ip, motion=motion, personality=personality)
                
                if recognized_text:
                    # 使用识别到的文本作为用户输入，进入主循环处理
                    # 确保 user_input 是 unicode
                    if isinstance(recognized_text, str):
                        user_input = recognized_text.decode('utf-8', 'ignore')
                    else:
                        user_input = recognized_text
                    uprint(u"\n[已识别您的语音]")
                    
                    # 检查终止规则（确保都是 unicode）
                    termination_keywords = [u'quit', u'exit', u'退出', u'结束', u'回答完毕', u'完毕']
                    if any(keyword in user_input for keyword in termination_keywords):
                        session['stage'] = 8
                        session['finished'] = True
                        save_session(session)
                        
                        config = get_personality_config(personality)
                        closing = config['closing']
                        
                        # 说结束语（说话过程中会做动作）
                        speak_with_actions(tts, closing, motion, animation, personality, audio_recorder, auto_record=False)
                        
                        # 结束语后做鞠躬
                        if motion is not None:
                            try:
                                from nao_motions import gentle_bow
                                gentle_bow(motion)
                            except Exception as e:
                                uprint(u"[提示] 鞠躬动作执行失败: %s" % str(e))
                    else:
                        # 更新会话（用户回答第一个问题）
                        session['conversation_history'].append({
                            'user': user_input,
                            'assistant': first_question_response,
                            'stage': session['stage'],
                            'question_index': session.get('question_index', 0)
                        })
                        
                        # 推进问题索引（第一个问题已回答，准备问第二个问题）
                        current_index = session.get('question_index', 0)
                        if current_index < len(COUNSELING_QUESTIONS) - 1:
                            session['question_index'] = current_index + 1
                        else:
                            session['stage'] = 8
                            session['finished'] = True
                        
                        save_session(session)
                        
                        # 思考用户回答并生成回复（共情+建议+下一个问题）
                        if not session.get('finished', False):
                            response = get_llm_response(
                                personality,
                                session['stage'],
                                user_input,
                                session['conversation_history'],
                                session.get('question_index', 0)
                            )
                            
                            if response:
                                # 更新会话
                                session['conversation_history'].append({
                                    'user': user_input,
                                    'assistant': response,
                                    'stage': session['stage'],
                                    'question_index': session.get('question_index', 0)
                                })
                                
                                # 推进问题索引（为下一个问题做准备）
                                from personality_config import COUNSELING_QUESTIONS
                                current_index = session.get('question_index', 0)
                                if current_index < len(COUNSELING_QUESTIONS) - 1:
                                    session['question_index'] = current_index + 1
                                else:
                                    session['stage'] = 8
                                    session['finished'] = True
                                
                                save_session(session)
                                
                                # NAO 说话（回答+下一个问题）
                                uprint(u"\nNAO: ", end='')
                                speak_with_actions(tts, response, motion, animation, personality, audio_recorder, auto_record=False)
                                uprint("")
                                
                                # 问完问题后立即开始录音（等待用户回答下一个问题）
                                if not session.get('finished', False) and audio_recorder is not None:
                                    nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
                                    recognized_text = record_audio_after_speech(audio_recorder, duration=10, nao_ip=nao_ip, motion=motion, personality=personality)
                                    
                                    if recognized_text:
                                        # 使用识别到的文本作为用户输入，直接处理，不进入主循环的录音部分
                                        if isinstance(recognized_text, str):
                                            user_input = recognized_text.decode('utf-8', 'ignore')
                                        else:
                                            user_input = recognized_text
                                        uprint(u"\n[已识别您的语音]")
                                        
                                        # 检查终止规则
                                        termination_keywords = [u'quit', u'exit', u'退出', u'结束', u'回答完毕', u'完毕']
                                        if any(keyword in user_input for keyword in termination_keywords):
                                            session['stage'] = 8
                                            session['finished'] = True
                                            save_session(session)
                                            
                                            config = get_personality_config(personality)
                                            closing = config['closing']
                                            
                                            # 说结束语（说话过程中会做动作）
                                            speak_with_actions(tts, closing, motion, animation, personality, audio_recorder, auto_record=False)
                                            
                                            # 结束语后做鞠躬
                                            if motion is not None:
                                                try:
                                                    from nao_motions import gentle_bow
                                                    gentle_bow(motion)
                                                except Exception as e:
                                                    uprint(u"[提示] 鞠躬动作执行失败: %s" % str(e))
                                            # 已经设置finished=True，主循环会退出
                                        else:
                                            # 已经识别了，直接进入主循环处理，跳过主循环的第一次录音
                                            # 设置一个标志，让主循环知道已经有输入了
                                            session['_pending_user_input'] = user_input
                                    else:
                                        uprint(u"\n[未能识别到语音]")
                                        # 如果识别失败，进入主循环等待下一次录音
                                        user_input = None
                else:
                    uprint(u"\n[未能识别到语音]")
    
    # 主对话循环（纯语音模式）
    uprint(u"\n" + "-" * 60)
    uprint(u"语音对话模式（说 '结束' 或 '回答完毕' 退出）")
    uprint(u"提示: 机器人问完问题后会自动开始录音")
    uprint("-" * 60 + "\n")
    
    while not session.get('finished', False):
        try:
            # 获取用户语音输入（通过录音识别）
            user_input = None
            
            # 检查是否有待处理的用户输入（从NAO说完话后录音识别传入）
            if '_pending_user_input' in session and session['_pending_user_input']:
                user_input = session['_pending_user_input']
                del session['_pending_user_input']  # 清除标志
                uprint(u"\n[使用已识别的语音输入]")
            else:
                # 如果没有待处理的输入，说明这是第一次进入主循环（第一个问题回答后）
                # 或者录音失败，需要等待NAO说完话后的录音
                # 这里不录音，直接continue，等待NAO说完话后的录音逻辑
                if audio_recorder is None:
                    # 如果没有录音功能，提示用户
                    uprint(u"[错误] 音频录制功能未启用，无法进行语音对话")
                    uprint(u"[提示] 请确保NAO机器人已连接")
                    break
                # 如果没有待处理的输入，继续循环，等待NAO说完话后的录音
                # 注意：第一次进入主循环时，应该已经有_pending_user_input了（从第一个问题回答后设置）
                # 如果没有，说明可能是第一次循环，需要等待
                continue
            
            if not user_input:
                continue
            
            # 检查终止规则（支持多种终止关键词，确保都是 unicode）
            termination_keywords = [u'quit', u'exit', u'退出', u'结束', u'回答完毕', u'完毕']
            if any(keyword in user_input for keyword in termination_keywords):
                # 立即跳转到结束阶段
                session['stage'] = 8
                session['finished'] = True
                save_session(session)
                
                # 结束语
                config = get_personality_config(personality)
                closing = config['closing']
                
                # 说结束语（说话过程中会做动作）
                speak_with_actions(tts, closing, motion, animation, personality, audio_recorder, auto_record=False)
                
                # 结束语后做鞠躬
                if motion is not None:
                    try:
                        from nao_motions import gentle_bow
                        gentle_bow(motion)
                    except Exception as e:
                        uprint(u"[提示] 鞠躬动作执行失败: %s" % str(e))
                break
            
            # 获取 LLM 响应
            response = get_llm_response(
                personality,
                session['stage'],
                user_input,
                session['conversation_history'],
                session.get('question_index', 0)
            )
            
            if response is None:
                uprint(u"[错误] 无法获取响应，请检查 DeepSeek API 配置")
                continue
            
            # 更新会话
            session['conversation_history'].append({
                'user': user_input,
                'assistant': response,
                'stage': session['stage'],
                'question_index': session.get('question_index', 0)
            })
            
            # 阶段和问题推进逻辑
            if session['stage'] == 0:
                # 开场后进入问题阶段
                session['stage'] = 1
                session['question_index'] = 0
            elif session['stage'] == 1:
                # 在问题阶段，用户回答后推进到下一个问题
                from personality_config import COUNSELING_QUESTIONS
                current_index = session.get('question_index', 0)
                if current_index < len(COUNSELING_QUESTIONS) - 1:
                    # 还有问题未问，推进到下一个
                    session['question_index'] = current_index + 1
                else:
                    # 所有问题都问完了，进入结束阶段
                    session['stage'] = 8
                    session['finished'] = True
            
            # 如果到达结束阶段，标记完成
            if session['stage'] >= 8:
                session['finished'] = True
                # 自动执行结束语
                config = get_personality_config(personality)
                closing = config['closing']
                
                # 说结束语（说话过程中会做动作）
                speak_with_actions(tts, closing, motion, animation, personality, audio_recorder, auto_record=False)
                
                # 结束语后做鞠躬
                if motion is not None:
                    try:
                        from nao_motions import gentle_bow
                        gentle_bow(motion)
                    except Exception as e:
                        uprint(u"[提示] 鞠躬动作执行失败: %s" % str(e))
                break
            
            save_session(session)
            
            # NAO 说话（问完问题后立即开始录音）
            uprint(u"\nNAO: ", end='')
            speak_with_actions(tts, response, motion, animation, personality, audio_recorder, auto_record=False)
            uprint("")
            
            # 问完问题后立即开始录音（不等待，立即开始，参考用户提供的代码）
            if session['stage'] == 1 and audio_recorder is not None:
                # 立即开始录音，获取用户回答（TTS是异步的，可以立即开始录音）
                nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
                recognized_text = record_audio_after_speech(audio_recorder, duration=10, nao_ip=nao_ip, motion=motion, personality=personality)
                
                if recognized_text:
                    # 使用识别到的文本作为用户输入
                    # 确保 user_input 是 unicode
                    if isinstance(recognized_text, str):
                        user_input = recognized_text.decode('utf-8', 'ignore')
                    else:
                        user_input = recognized_text
                    uprint(u"\n[已识别您的语音]")
                    
                    # 检查终止规则（确保都是 unicode）
                    termination_keywords = [u'quit', u'exit', u'退出', u'结束', u'回答完毕', u'完毕']
                    if any(keyword in user_input for keyword in termination_keywords):
                        session['stage'] = 8
                        session['finished'] = True
                        save_session(session)
                        
                        config = get_personality_config(personality)
                        closing = config['closing']
                        
                        # 说结束语（说话过程中会做动作）
                        speak_with_actions(tts, closing, motion, animation, personality, audio_recorder, auto_record=False)
                        
                        # 结束语后做鞠躬
                        if motion is not None:
                            try:
                                from nao_motions import gentle_bow
                                gentle_bow(motion)
                            except Exception as e:
                                uprint(u"[提示] 鞠躬动作执行失败: %s" % str(e))
                        break
                    
                    # 已经识别了，设置标志，让下次循环使用这个输入，避免重复录音
                    session['_pending_user_input'] = user_input
                    # 继续循环，下次循环会使用_pending_user_input，跳过录音，直接处理
                    continue
                else:
                    uprint(u"\n[未能识别到语音，请重试]")
                    # 如果识别失败，继续循环等待下一次录音
                    continue
            
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

