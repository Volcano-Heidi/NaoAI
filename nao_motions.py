# -*- coding: utf-8 -*-
# NAO机器人动作库 - 心理咨询师专用

import os
import sys
import time
import io

# 使用统一的SDK helper
from nao_sdk_helper import setup_naoqi_sdk

# 设置SDK路径
if not setup_naoqi_sdk():
    print("Warning: NAOqi SDK not found, some functions may not work")

# 尝试导入ALProxy
try:
    from naoqi import ALProxy
except ImportError:
    # 尝试从qi.naoqi导入
    try:
        from qi import naoqi
        ALProxy = naoqi.ALProxy
    except ImportError:
        ALProxy = None
        print("Warning: Cannot import ALProxy from naoqi or qi.naoqi")

def get_nao_proxies():
    """获取NAO代理对象"""
    nao_ip = os.environ.get('NAO_IP', "192.168.10.3")
    nao_port = int(os.environ.get('NAO_PORT', '9559'))
    
    if ALProxy is None:
        return None, None, None
    
    try:
        motion = ALProxy("ALMotion", nao_ip, nao_port)
        animation = ALProxy("ALAnimationPlayer", nao_ip, nao_port)
        posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
        return motion, animation, posture
    except Exception as e:
        print("Error initializing NAO proxies: %s" % e)
        return None, None, None

def wake_up(motion):
    """唤醒NAO机器人"""
    if motion is None:
        return
    try:
        motion.wakeUp()
    except:
        pass

def rest(motion):
    """让NAO休息"""
    if motion is None:
        return
    try:
        motion.rest()
    except:
        pass

def stand_init(posture):
    """站立初始姿势"""
    if posture is None:
        return
    try:
        posture.goToPosture("StandInit", 0.5)
    except:
        pass

# ==================== 心理咨询师动作库 ====================

def greeting_action(motion, animation):
    """开场问候动作 - 友好的挥手和点头"""
    if motion is None or animation is None:
        return
    
    try:
        # 先站立
        motion.setStiffnesses("Body", 1.0)
        motion.moveInit()
        
        # 挥手动作（使用手臂）
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        angles = [0.5, 0.3, -1.5, -0.3, 0.0]
        times = [0.5, 1.0, 1.5, 2.0, 2.5]
        motion.angleInterpolation(names, angles, times, True)
        
        # 挥手回来
        angles = [1.3, 0.1, -1.5, -1.0, 0.0]
        times = [0.3, 0.6, 0.9, 1.2, 1.5]
        motion.angleInterpolation(names, angles, times, True)
        
        # 点头
        names = ["HeadPitch"]
        angles = [0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Greeting action error: %s" % e)

def listening_action(motion):
    """倾听动作 - 轻微点头和身体前倾"""
    if motion is None:
        return
    
    try:
        # 轻微点头
        names = ["HeadPitch"]
        angles = [0.1]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.1]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        
        # 身体稍微前倾
        names = ["HipPitch"]
        angles = [0.1]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Listening action error: %s" % e)

def thinking_action(motion):
    """思考动作 - 手托下巴或头部倾斜"""
    if motion is None:
        return
    
    try:
        # 头部稍微倾斜
        names = ["HeadYaw"]
        angles = [0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 手部动作（模拟思考）
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, -0.3, 1.0, 0.5]
        times = [0.4, 0.8, 1.2, 1.6]
        motion.angleInterpolation(names, angles, times, True)
        angles = [1.3, 0.1, 0.0, -1.0]
        times = [0.3, 0.6, 0.9, 1.2]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Thinking action error: %s" % e)

def encouraging_action(motion):
    """鼓励动作 - 点头和张开手臂"""
    if motion is None:
        return
    
    try:
        # 点头
        names = ["HeadPitch"]
        for i in range(2):
            angles = [0.15]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
            angles = [-0.15]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
        
        # 手臂张开（鼓励的手势）
        names = ["LShoulderRoll", "RShoulderRoll"]
        angles = [0.3, -0.3]
        times = [0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.1, -0.1]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Encouraging action error: %s" % e)

def empathetic_action(motion):
    """共情动作 - 温和的手势和身体语言"""
    if motion is None:
        return
    
    try:
        # 双手放在胸前（共情的手势）
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.8, 0.2, -1.0, -0.5, 0.8, -0.2, 1.0, 0.5]
        times = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        motion.angleInterpolation(names, angles, times, True)
        
        # 轻微点头
        names = ["HeadPitch"]
        angles = [0.1]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [1.3, 0.1, -1.5, -1.0, 1.3, -0.1, 1.5, 1.0]
        times = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Empathetic action error: %s" % e)

def questioning_action(motion):
    """提问动作 - 头部倾斜和手部动作"""
    if motion is None:
        return
    
    try:
        # 头部稍微倾斜（表示疑问）
        names = ["HeadYaw"]
        angles = [0.3]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 手部动作（指向或手势）
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, -0.2, 0.5, 0.3]
        times = [0.3, 0.3, 0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [1.3, -0.1, 0.0, -1.0]
        times = [0.3, 0.3, 0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Questioning action error: %s" % e)

def closing_action(motion):
    """结束动作 - 告别手势"""
    if motion is None:
        return
    
    try:
        # 挥手告别
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
        angles = [0.5, 0.3, -1.5, -0.3]
        times = [0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        # 挥手动作
        for i in range(2):
            angles = [0.5, 0.4, -1.5, -0.2]
            times = [0.2, 0.2, 0.2, 0.2]
            motion.angleInterpolation(names, angles, times, True)
            angles = [0.5, 0.2, -1.5, -0.4]
            times = [0.2, 0.2, 0.2, 0.2]
            motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        angles = [1.3, 0.1, -1.5, -1.0]
        times = [0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        # 点头
        names = ["HeadPitch"]
        angles = [0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
    except Exception as e:
        print("Closing action error: %s" % e)

def gentle_nod(motion, count=1):
    """温和的点头"""
    if motion is None:
        return
    
    try:
        names = ["HeadPitch"]
        for i in range(count):
            angles = [0.1]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
            angles = [0.0]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Nod action error: %s" % e)

# ==================== 动作选择函数 ====================

def select_action_by_text(text, motion, animation, personality=None):
    """根据文本内容和性格选择动作"""
    if motion is None:
        return
    
    text_lower = text.lower() if isinstance(text, str) else text
    text_u = text if isinstance(text, unicode) else unicode(text, 'utf-8', 'ignore')
    
    # 开场白关键词
    if any(keyword in text_u for keyword in [u'你好', u'感谢', u'开始', u'欢迎', u'准备好了']):
        greeting_action(motion, animation)
        return
    
    # 结束语关键词
    if any(keyword in text_u for keyword in [u'感谢', u'再见', u'祝你', u'结束', u'再见', u'欢迎回来']):
        closing_action(motion)
        return
    
    # 根据性格调整动作风格
    if personality == 'humorous':
        # 幽默性格：更活泼的动作
        if any(keyword in text_u for keyword in [u'有趣', u'好笑', u'开心', u'愉快', u'轻松']):
            # 活泼的手势
            try:
                names = ["LShoulderRoll", "RShoulderRoll"]
                angles = [0.4, -0.4]
                times = [0.3, 0.3]
                motion.angleInterpolation(names, angles, times, True)
                angles = [0.1, -0.1]
                times = [0.3, 0.3]
                motion.angleInterpolation(names, angles, times, True)
            except:
                pass
            return
    
    elif personality == 'gentle':
        # 温柔性格：更温和的动作
        if any(keyword in text_u for keyword in [u'温柔', u'温暖', u'体贴', u'慢慢']):
            empathetic_action(motion)
            return
    
    elif personality == 'professional':
        # 专业性格：更正式的动作
        if any(keyword in text_u for keyword in [u'专业', u'科学', u'分析', u'建议']):
            thinking_action(motion)
            return
    
    # 提问关键词
    if any(keyword in text_u for keyword in [u'？', u'?', u'什么', u'怎么', u'为什么', u'可以', u'能', u'如何']):
        questioning_action(motion)
        return
    
    # 鼓励关键词
    if any(keyword in text_u for keyword in [u'很好', u'不错', u'可以', u'能够', u'一定', u'会好', u'加油']):
        encouraging_action(motion)
        return
    
    # 共情关键词
    if any(keyword in text_u for keyword in [u'理解', u'感受', u'明白', u'知道', u'体会', u'理解你', u'我懂']):
        empathetic_action(motion)
        return
    
    # 思考关键词
    if any(keyword in text_u for keyword in [u'让我', u'我想', u'考虑', u'分析', u'建议']):
        thinking_action(motion)
        return
    
    # 默认：倾听动作
    listening_action(motion)

def perform_action_during_speech(text, motion, animation, duration, personality=None):
    """在说话期间执行动作"""
    if motion is None:
        return
    
    import threading
    
    # 根据文本和性格选择动作
    action_thread = threading.Thread(
        target=select_action_by_text, 
        args=(text, motion, animation, personality)
    )
    action_thread.daemon = True
    action_thread.start()
    
    # 在说话期间，定期执行倾听动作
    if duration > 2:
        nod_interval = 2.0
        if personality == 'humorous':
            nod_interval = 1.5  # 幽默性格：更频繁的点头
        elif personality == 'gentle':
            nod_interval = 2.5  # 温柔性格：更慢的点头
        
        for i in range(int(duration / nod_interval)):
            time.sleep(nod_interval)
            if i % 2 == 0:
                gentle_nod(motion, 1)

