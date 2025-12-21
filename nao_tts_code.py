# -*- coding: utf-8 -*-
import os
import sys
import time
import io
import threading

# 使用统一的SDK helper
from nao_sdk_helper import setup_naoqi_sdk, get_nao_proxy_safe

# 设置SDK路径
if not setup_naoqi_sdk():
    print("Error: NAOqi SDK not found")
    print("Please set PYNAOQI_PATH or ensure qi package is in project directory")
    ALProxy = None
    HAS_NAOQI = False
else:
    # 尝试导入ALProxy
    try:
        from naoqi import ALProxy
        HAS_NAOQI = True
    except ImportError:
        # 尝试从qi.naoqi导入
        try:
            from qi import naoqi
            ALProxy = naoqi.ALProxy
            HAS_NAOQI = True
        except ImportError:
            ALProxy = None
            HAS_NAOQI = False
            print("Error: Cannot import ALProxy from naoqi or qi.naoqi")

# 导入动作库
try:
    from nao_motions import (
        get_nao_proxies, wake_up, stand_init,
        select_action_by_text, perform_action_during_speech
    )
    HAS_MOTIONS = True
except ImportError:
    HAS_MOTIONS = False
    print("Warning: nao_motions module not found, actions will be disabled")

# Set the IP address and port of your NAO robot
nao_ip = os.environ.get('NAO_IP', "192.168.10.3")
nao_port = int(os.environ.get('NAO_PORT', '9559'))

# Create an ALTextToSpeech proxy
tts = None
if HAS_NAOQI:
    try:
        tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
        # 测试连接
        try:
            tts.getVolume()  # 测试调用
            print("✓ 成功连接到NAO机器人 (IP: %s)" % nao_ip)
        except Exception as e:
            print("⚠ 连接到NAO但无法调用服务: %s" % str(e))
            tts = None
    except Exception as e:
        error_msg = str(e)
        print("✗ 无法连接到NAO机器人")
        print("错误: %s" % error_msg)
        print("")
        print("请检查:")
        print("  1. NAO_IP是否正确: %s" % nao_ip)
        print("  2. NAO机器人是否已开机并完全启动（等待1-2分钟）")
        print("  3. 网络连接是否正常（本机IP: 可能在不同网段）")
        print("  4. 如果本机在Docker容器中，需要配置网络")
        print("  5. 运行诊断工具: python diagnose_nao_connection.py")
        print("")
        print("提示: 如果暂时无法连接，可以使用文本模式测试:")
        print("  python text_counselor.py")
        tts = None
else:
    print("错误: NAOqi SDK未正确配置，无法使用NAO功能")
file_content=""
# Set the text content you want NAO to say
file_path="./gpt_response.txt"
try:
    with io.open(file_path, 'r', encoding='utf-8-sig') as file:
        file_content = file.read().strip()
except Exception as e:
    print("Error reading file: %s" % e)
    

if tts is not None:
    try:
        text_u = file_content if isinstance(file_content, unicode) else unicode(file_content, 'utf-8', 'ignore')
    except Exception:
        text_u = unicode(file_content)
    try:
        has_non_ascii = any(ord(c) > 127 for c in text_u)
        if has_non_ascii:
            tts.setLanguage('Chinese')
        else:
            tts.setLanguage('English')
    except Exception:
        pass
    
    # 初始化动作系统
    motion, animation, posture = None, None, None
    if HAS_MOTIONS:
        motion, animation, posture = get_nao_proxies()
        if motion is not None:
            try:
                wake_up(motion)
                stand_init(posture)
            except:
                pass
    
    # 估算说话时长（简单估算：中文约3字/秒，英文约5字/秒）
    text_length = len(text_u)
    estimated_duration = text_length / 3.0 if has_non_ascii else text_length / 5.0
    estimated_duration = max(2.0, min(estimated_duration, 15.0))  # 限制在2-15秒
    
    # 在说话前执行动作
    if motion is not None:
        try:
            select_action_by_text(text_u, motion, animation)
            time.sleep(0.5)  # 动作执行时间
        except Exception as e:
            print("Action error: %s" % e)
    
    # 开始说话（在后台线程中执行动作）
    if motion is not None:
        def action_thread():
            try:
                perform_action_during_speech(text_u, motion, animation, estimated_duration)
            except:
                pass
        
        action_t = threading.Thread(target=action_thread)
        action_t.daemon = True
        action_t.start()
    
    # 执行TTS
    tts.say(text_u.encode('utf-8'))
    
    # 等待说话完成
    time.sleep(max(estimated_duration, 2))
    
    # 说话后的动作
    if motion is not None:
        try:
            from nao_motions import gentle_nod
            gentle_nod(motion, 1)
        except:
            pass
else:
    sys.exit(0)

# Release the proxy
