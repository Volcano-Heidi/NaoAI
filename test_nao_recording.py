# -*- coding: utf-8 -*-
# NAO机器人录音功能测试脚本

import os
import sys
import time

# 设置SDK
from nao_sdk_helper import setup_naoqi_sdk
if not setup_naoqi_sdk():
    print("Warning: NAOqi SDK not found")

try:
    from naoqi import ALProxy
except ImportError:
    try:
        from qi import naoqi
        ALProxy = naoqi.ALProxy
    except ImportError:
        ALProxy = None
        print("Error: Cannot import ALProxy")
        sys.exit(1)

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

def test_recording():
    """测试录音功能"""
    # 获取NAO IP
    nao_ip = os.environ.get('NAO_IP', '172.20.10.4')
    nao_port = int(os.environ.get('NAO_PORT', '9559'))
    
    uprint(u"\n" + "=" * 60)
    uprint(u"NAO 录音功能测试")
    uprint("=" * 60)
    uprint(u"NAO IP: %s" % nao_ip)
    uprint(u"NAO Port: %s" % nao_port)
    uprint("=" * 60 + "\n")
    
    # 初始化音频录制
    audio_recorder = None
    try:
        audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
        uprint(u"✓ 成功连接到 ALAudioRecorder 服务")
    except Exception as e:
        uprint(u"✗ 无法连接到 ALAudioRecorder: %s" % str(e))
        return False
    
    # 测试录音
    duration = 5  # 测试录音5秒
    remote_path = "/home/nao/test_recording_%d.wav" % int(time.time())
    
    try:
        # 停止之前的录音（如果有）
        try:
            audio_recorder.stopMicrophonesRecording()
            time.sleep(0.3)
            uprint(u"[已停止之前的录音]")
        except:
            pass
        
        uprint(u"\n[开始测试录音...]")
        uprint(u"[录音时长: %d秒]" % duration)
        uprint(u"[保存路径: %s]" % remote_path)
        uprint(u"[请对着NAO机器人说话...]\n")
        
        # 开始录音
        audio_recorder.startMicrophonesRecording(
            remote_path,
            "wav",
            16000,  # 采样率
            [1, 0, 0, 0]  # 前左麦克风
        )
        
        # 倒计时
        for i in range(duration):
            time.sleep(1)
            uprint(u"[录音中... %d/%d秒]" % (i + 1, duration))
        
        # 停止录音
        audio_recorder.stopMicrophonesRecording()
        time.sleep(0.5)  # 等待文件写入
        
        uprint(u"\n[录音完成！]")
        uprint(u"[文件已保存到: %s]" % remote_path)
        uprint(u"\n[提示] 您可以通过以下方式下载录音文件：")
        uprint(u"  scp nao@%s:%s ./test_recording.wav" % (nao_ip, remote_path))
        uprint(u"  或使用SFTP客户端连接下载")
        
        return True
        
    except Exception as e:
        uprint(u"\n[错误] 录音测试失败: %s" % str(e))
        import traceback
        traceback.print_exc()
        return False

def test_multiple_recordings():
    """测试多次录音"""
    nao_ip = os.environ.get('NAO_IP', '172.20.10.4')
    nao_port = int(os.environ.get('NAO_PORT', '9559'))
    
    audio_recorder = None
    try:
        audio_recorder = ALProxy("ALAudioRecorder", nao_ip, nao_port)
    except Exception as e:
        uprint(u"✗ 无法连接: %s" % str(e))
        return False
    
    uprint(u"\n[测试多次连续录音...]")
    
    for i in range(3):
        uprint(u"\n[第 %d 次录音]" % (i + 1))
        remote_path = "/home/nao/test_recording_%d_%d.wav" % (int(time.time()), i)
        
        try:
            # 停止之前的录音
            try:
                audio_recorder.stopMicrophonesRecording()
                time.sleep(0.2)
            except:
                pass
            
            # 开始录音
            audio_recorder.startMicrophonesRecording(
                remote_path,
                "wav",
                16000,
                [1, 0, 0, 0]
            )
            
            uprint(u"[录音中... 3秒]")
            time.sleep(3)
            
            # 停止录音
            audio_recorder.stopMicrophonesRecording()
            time.sleep(0.3)
            
            uprint(u"[完成] 文件: %s" % remote_path)
            
        except Exception as e:
            uprint(u"[错误] 第%d次录音失败: %s" % (i + 1, str(e)))
    
    uprint(u"\n[多次录音测试完成]")
    return True

if __name__ == '__main__':
    uprint(u"\n选择测试模式：")
    uprint(u"1. 单次录音测试（5秒）")
    uprint(u"2. 多次连续录音测试（3次，每次3秒）")
    
    try:
        choice = raw_input("\n请输入选项 (1-2): ").strip()
        
        if choice == '1':
            test_recording()
        elif choice == '2':
            test_multiple_recordings()
        else:
            uprint(u"无效选项，执行单次录音测试")
            test_recording()
    except KeyboardInterrupt:
        uprint(u"\n\n测试已取消")
    except Exception as e:
        uprint(u"\n[错误] %s" % str(e))
        import traceback
        traceback.print_exc()

