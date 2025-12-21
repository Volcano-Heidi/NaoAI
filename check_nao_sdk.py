# -*- coding: utf-8 -*-
# 检查NAOqi SDK配置

import os
import sys

# 添加项目目录到路径
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from nao_sdk_helper import setup_naoqi_sdk

print("检查NAOqi SDK路径...")
print("")

if setup_naoqi_sdk():
    print("✓ 找到NAOqi SDK")
    print("")
    
    # 测试导入
    try:
        from naoqi import ALProxy
        print("✓ 可以导入ALProxy")
        print("")
        
        # 测试连接NAO（可选）
        import os
        nao_ip = os.environ.get('NAO_IP', '192.168.10.3')
        nao_port = 9559
        
        print("测试连接NAO机器人 (IP: %s)..." % nao_ip)
        try:
            tts = ALProxy('ALTextToSpeech', nao_ip, nao_port)
            print("✓ 可以连接到NAO机器人")
        except Exception as e:
            print("⚠ 无法连接到NAO机器人: %s" % str(e))
            print("  但SDK已正确配置")
    except ImportError as e:
        print("✗ 无法导入ALProxy: %s" % str(e))
else:
    print("✗ 未找到NAOqi SDK")
    print("")
    import platform
    is_macos = platform.system() == 'Darwin'
    is_linux = platform.system() == 'Linux'
    
    if is_macos:
        print("请设置PYNAOQI_PATH环境变量：")
        print("  export PYNAOQI_PATH=/path/to/pynaoqi-python2.7-2.8.6.23-mac64")
        print("")
        print("或者下载NAOqi SDK并解压到以下位置之一：")
        print("  - ~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4")
        print("  - 项目目录: %s/pynaoqi-python2.7-2.8.6.23-mac64" % project_dir)
        print("  - /opt/naoqi/pynaoqi-python2.7-2.8.6.23-mac64")
        print("  - /usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-mac64")
        print("  - ~/pynaoqi-python2.7-2.8.6.23-mac64")
    elif is_linux:
        print("请设置PYNAOQI_PATH环境变量：")
        print("  export PYNAOQI_PATH=/path/to/pynaoqi-python2.7-2.8.6.23-linux64")
        print("")
        print("或者下载NAOqi SDK并解压到以下位置之一：")
        print("  - /opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64")
        print("  - /usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-linux64")
        print("  - /home/nao/pynaoqi-python2.7-2.8.6.23-linux64")
        print("  - /root/pynaoqi-python2.7-2.8.6.23-linux64")
        print("  - /opt/aldebaran/pynaoqi-python2.7-2.8.6.23-linux64")
        print("  - 项目目录: %s/pynaoqi-..." % project_dir)
    else:
        print("请设置PYNAOQI_PATH环境变量指向NAOqi SDK路径")
