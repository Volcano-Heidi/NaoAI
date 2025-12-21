# -*- coding: utf-8 -*-
# NAO连接诊断工具

import os
import sys
import socket
import subprocess

# 添加项目目录到路径
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from nao_sdk_helper import setup_naoqi_sdk

print("=" * 60)
print("NAO机器人连接诊断")
print("=" * 60)
print("")

nao_ip = os.environ.get('NAO_IP', '192.168.10.3')
nao_port = 9559

print("NAO配置:")
print("  IP地址: %s" % nao_ip)
print("  端口: %s" % nao_port)
print("")

# 1. 检查网络连接
print("1. 检查网络连接...")
try:
    # Python 2.7兼容的ping检查
    result = subprocess.check_output(['ping', '-c', '2', '-W', '2', nao_ip], 
                                    stderr=subprocess.STDOUT)
    if '0 received' in result or '100% packet loss' in result:
        print("  ✗ 无法ping通NAO机器人")
        print("    可能原因:")
        print("    - NAO机器人未开机")
        print("    - IP地址不正确")
        print("    - 不在同一网络")
    else:
        print("  ✓ 可以ping通NAO机器人")
except Exception as e:
    if 'timeout' in str(e).lower() or 'timed out' in str(e).lower():
        print("  ✗ ping超时")
    else:
        print("  ✗ ping失败: %s" % str(e))

print("")

# 2. 检查端口连接
print("2. 检查端口连接 (9559)...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((nao_ip, nao_port))
    sock.close()
    if result == 0:
        print("  ✓ 端口9559可以连接")
    else:
        print("  ✗ 端口9559无法连接")
        print("    可能原因:")
        print("    - NAOqi服务未运行")
        print("    - 防火墙阻止连接")
except Exception as e:
    print("  ✗ 检查端口失败: %s" % str(e))

print("")

# 3. 检查SDK配置
print("3. 检查NAOqi SDK配置...")
if setup_naoqi_sdk():
    print("  ✓ SDK已配置")
    
    # 尝试导入
    try:
        from naoqi import ALProxy
        print("  ✓ ALProxy可以导入")
        
        # 尝试连接
        print("")
        print("4. 尝试连接NAO机器人...")
        try:
            tts = ALProxy('ALTextToSpeech', nao_ip, nao_port)
            print("  ✓ 成功连接到NAO机器人")
            print("")
            print("5. 测试TTS功能...")
            try:
                # 检查音量
                volume = tts.getVolume()
                print("  当前音量: %.2f" % volume)
                if volume < 0.3:
                    print("  ⚠ 音量较低，建议调高")
                
                # 测试说话
                test_text = u"测试"
                print("  发送测试语音...")
                tts.say(test_text.encode('utf-8'))
                print("  ✓ TTS命令已发送")
            except Exception as e:
                print("  ✗ TTS测试失败: %s" % str(e))
        except Exception as e:
            print("  ✗ 无法连接: %s" % str(e))
    except ImportError as e:
        print("  ✗ 无法导入ALProxy: %s" % str(e))
else:
    print("  ✗ SDK未配置")

print("")
print("=" * 60)
print("诊断完成")
print("=" * 60)
print("")
print("如果无法连接，请检查:")
print("1. NAO机器人是否已开机")
print("2. NAO机器人IP地址是否正确")
print("3. 电脑和NAO是否在同一网络")
print("4. NAO机器人的NAOqi服务是否运行")
print("5. 防火墙设置是否允许连接")

