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
    nao_ip = os.environ.get('NAO_IP', "192.168.10.4")
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
        
        # 身体稍微前倾（使用左右髋关节同时控制）
        names = ["LHipPitch", "RHipPitch"]
        angles = [0.1, 0.1]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0, 0.0]
        times = [0.3, 0.3]
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

# ==================== 幽默性格专属动作 ====================

def humorous_quick_nod(motion):
    """快速小幅度点头，配合头部微微扬起"""
    if motion is None:
        return
    try:
        # 快速点头
        names = ["HeadPitch"]
        for i in range(2):
            angles = [0.15]  # 小幅度
            times = [0.15]  # 快速
            motion.angleInterpolation(names, angles, times, True)
            angles = [-0.1]  # 微微扬起
            times = [0.15]
            motion.angleInterpolation(names, angles, times, True)
        # 恢复
        angles = [0.0]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous quick nod error: %s" % e)

def humorous_tilt_head(motion):
    """歪头"""
    if motion is None:
        return
    try:
        names = ["HeadYaw"]
        # 向右歪
        angles = [0.3]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        # 向左歪
        angles = [-0.3]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        # 恢复
        angles = [0.0]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous tilt head error: %s" % e)

def humorous_hip_sway(motion):
    """扭屁股：轻微左右摇摆髋关节，配合手臂摆动"""
    if motion is None:
        return
    try:
        # 髋关节左右摇摆
        names = ["HipRoll"]
        angles = [0.1]  # 向右
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.1]  # 向左
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]  # 恢复
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 配合手臂摆动
        names = ["LShoulderRoll", "RShoulderRoll"]
        angles = [0.2, -0.2]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.2, 0.2]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.1, -0.1]
        times = [0.2, 0.2]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous hip sway error: %s" % e)

def humorous_shrug(motion):
    """耸肩摊手：单肩或双肩耸起，手臂外展"""
    if motion is None:
        return
    try:
        # 双肩耸起
        names = ["LShoulderPitch", "RShoulderPitch"]
        angles = [0.3, 0.3]  # 耸肩
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 手臂外展
        names = ["LShoulderRoll", "RShoulderRoll"]
        angles = [0.3, -0.3]  # 摊手
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"]
        angles = [1.3, 1.3, 0.1, -0.1]
        times = [0.3, 0.3, 0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous shrug error: %s" % e)

def humorous_cover_face(motion):
    """捂脸：用手遮住"脸"，低头左右轻微晃动"""
    if motion is None:
        return
    try:
        # 双手遮脸
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, 0.4, -1.0, -0.8, 0.5, -0.4, 1.0, 0.8]  # 双手举到脸前
        times = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        # 低头
        names = ["HeadPitch"]
        angles = [0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 左右轻微晃动
        names = ["HeadYaw"]
        for i in range(2):
            angles = [0.15]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
            angles = [-0.15]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["HeadPitch", "HeadYaw"]
        angles = [0.0, 0.0]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [1.3, 0.1, -1.5, -1.0, 1.3, -0.1, 1.5, 1.0]
        times = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous cover face error: %s" % e)

def humorous_finger_circle(motion):
    """手指绕圈：用手指绕圈，配合眨眼或点头"""
    if motion is None:
        return
    try:
        # 右手举起，手指绕圈
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [0.3, -0.2, 0.5, 0.3, 0.0]
        times = [0.3, 0.3, 0.3, 0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 手腕绕圈（模拟手指绕圈）
        for i in range(2):
            names = ["RWristYaw"]
            angles = [1.0]
            times = [0.3]
            motion.angleInterpolation(names, angles, times, True)
            angles = [-1.0]
            times = [0.3]
            motion.angleInterpolation(names, angles, times, True)
        
        # 配合点头
        names = ["HeadPitch"]
        angles = [0.1]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.2]
        motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [1.3, -0.1, 0.0, -1.0, 0.0]
        times = [0.3, 0.3, 0.3, 0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous finger circle error: %s" % e)

def humorous_look_around(motion):
    """张望：手举到额前做"张望"状"""
    if motion is None:
        return
    try:
        # 右手举到额前
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.2, -0.3, 0.8, 0.5]  # 手举到额前
        times = [0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        # 头部左右转动（张望）
        names = ["HeadYaw"]
        angles = [0.3]  # 向右看
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        angles = [-0.3]  # 向左看
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]  # 恢复
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [1.3, -0.1, 0.0, -1.0]
        times = [0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous look around error: %s" % e)

def humorous_sway_forward_back(motion):
    """轻微前后摇摆（幅度小）"""
    if motion is None:
        return
    try:
        # 使用左右髋关节同时控制前后摇摆
        names = ["LHipPitch", "RHipPitch"]
        # 向前
        angles = [0.08, 0.08]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        # 向后
        angles = [-0.08, -0.08]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
        # 恢复
        angles = [0.0, 0.0]
        times = [0.3, 0.3]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Humorous sway forward back error: %s" % e)

# ==================== 温柔性格专属动作 ====================

def gentle_bow(motion):
    """微微鞠躬：缓慢低头，保持1-2秒后抬起"""
    if motion is None:
        return
    try:
        names = ["HeadPitch"]
        # 缓慢低头
        angles = [0.25]
        times = [0.8]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        # 保持
        time.sleep(1.5)
        # 缓慢抬起
        angles = [0.0]
        times = [0.8]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle bow error: %s" % e)

def gentle_wave(motion):
    """轻轻挥手：手臂缓慢抬起，手指微微弯曲，左右小幅摆动"""
    if motion is None:
        return
    try:
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
        # 缓慢抬起
        angles = [0.4, 0.25, -1.3, -0.2]
        times = [0.6, 0.6, 0.6, 0.6]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        
        # 左右小幅摆动
        for i in range(2):
            angles = [0.4, 0.3, -1.3, -0.1]
            times = [0.4, 0.4, 0.4, 0.4]
            motion.angleInterpolation(names, angles, times, True)
            angles = [0.4, 0.2, -1.3, -0.3]
            times = [0.4, 0.4, 0.4, 0.4]
            motion.angleInterpolation(names, angles, times, True)
        
        # 缓慢恢复
        angles = [1.3, 0.1, -1.5, -1.0]
        times = [0.6, 0.6, 0.6, 0.6]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle wave error: %s" % e)

def gentle_hands_heart(motion):
    """双手捧心：双手在胸前合拢或轻轻交叠，头部微微倾斜"""
    if motion is None:
        return
    try:
        # 双手在胸前合拢
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.7, 0.15, -1.2, -0.6, 0.7, -0.15, 1.2, 0.6]  # 双手在胸前
        times = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        
        # 头部微微倾斜
        names = ["HeadYaw"]
        angles = [0.15]
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        # 保持
        time.sleep(1.0)
        
        # 恢复
        names = ["HeadYaw"]
        angles = [0.0]
        times = [0.4]
        motion.angleInterpolation(names, angles, times, True)
        
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [1.3, 0.1, -1.5, -1.0, 1.3, -0.1, 1.5, 1.0]
        times = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle hands heart error: %s" % e)

def gentle_slow_nod(motion):
    """缓慢点头：配合眼神交流，点头频率慢"""
    if motion is None:
        return
    try:
        names = ["HeadPitch"]
        # 缓慢点头
        angles = [0.15]
        times = [0.5]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        angles = [0.0]
        times = [0.5]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle slow nod error: %s" % e)

def gentle_invite_gesture(motion):
    """伸手邀请：单手臂平缓伸出，手掌向上"""
    if motion is None:
        return
    try:
        # 右手平缓伸出
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [0.2, -0.2, 0.3, 0.0, 0.5]  # 手臂伸出，手掌向上
        times = [0.7, 0.7, 0.7, 0.7, 0.7]  # 平缓
        motion.angleInterpolation(names, angles, times, True)
        
        # 保持
        time.sleep(1.0)
        
        # 缓慢恢复
        angles = [1.3, -0.1, 0.0, -1.0, 0.0]
        times = [0.7, 0.7, 0.7, 0.7, 0.7]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle invite gesture error: %s" % e)

def gentle_listen_tilt(motion):
    """侧头倾听：头部向一侧倾斜，保持静止"""
    if motion is None:
        return
    try:
        names = ["HeadYaw"]
        # 向一侧倾斜
        angles = [0.25]
        times = [0.5]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        # 保持静止（倾听）
        time.sleep(2.0)
        # 恢复
        angles = [0.0]
        times = [0.5]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle listen tilt error: %s" % e)

def gentle_pat_shoulder(motion):
    """轻轻拍肩：用手轻拍自己的肩膀"""
    if motion is None:
        return
    try:
        # 右手轻拍左肩
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, -0.4, 0.8, 0.6]  # 手到肩膀位置
        times = [0.5, 0.5, 0.5, 0.5]
        motion.angleInterpolation(names, angles, times, True)
        
        # 轻拍动作（上下轻微移动）
        for i in range(2):
            names = ["RElbowRoll"]
            angles = [0.7]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
            angles = [0.5]
            times = [0.2]
            motion.angleInterpolation(names, angles, times, True)
        
        # 恢复
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [1.3, -0.1, 0.0, -1.0]
        times = [0.4, 0.4, 0.4, 0.4]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle pat shoulder error: %s" % e)

def gentle_share_gesture(motion):
    """分享动作：双手虚拟托着东西，慢慢递向对方"""
    if motion is None:
        return
    try:
        # 双手托着东西（在胸前）
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.6, 0.2, -1.1, -0.5, 0.6, -0.2, 1.1, 0.5]  # 双手在胸前
        times = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
        motion.angleInterpolation(names, angles, times, True)
        
        # 慢慢递向对方（向前伸出）
        angles = [0.4, 0.3, -1.3, -0.3, 0.4, -0.3, 1.3, 0.3]  # 向前伸出
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]  # 慢慢
        motion.angleInterpolation(names, angles, times, True)
        
        # 保持
        time.sleep(1.0)
        
        # 缓慢恢复
        angles = [1.3, 0.1, -1.5, -1.0, 1.3, -0.1, 1.5, 1.0]
        times = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle share gesture error: %s" % e)

def gentle_comforting_gesture(motion):
    """安抚性手势：双手手掌向上，从身体两侧缓慢抬至腰间"""
    if motion is None:
        return
    try:
        # 双手手掌向上，从身体两侧缓慢抬至腰间
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        # 起始位置（身体两侧，手掌向上）
        angles = [1.0, 0.5, -1.4, -0.8, 1.0, -0.5, 1.4, 0.8]
        times = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        motion.angleInterpolation(names, angles, times, True)
        
        # 缓慢抬至腰间
        angles = [0.8, 0.3, -1.2, -0.6, 0.8, -0.3, 1.2, 0.6]  # 腰间位置
        times = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # 缓慢
        motion.angleInterpolation(names, angles, times, True)
        
        # 保持
        time.sleep(1.5)
        
        # 缓慢恢复
        angles = [1.3, 0.1, -1.5, -1.0, 1.3, -0.1, 1.5, 1.0]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Gentle comforting gesture error: %s" % e)

# ==================== 动作选择函数 ====================

def select_action_by_text(text, motion, animation, personality=None):
    """根据文本内容和性格选择动作"""
    if motion is None:
        return
    
    text_lower = text.lower() if isinstance(text, str) else text
    text_u = text if isinstance(text, unicode) else unicode(text, 'utf-8', 'ignore')
    
    # 开场白关键词
    if any(keyword in text_u for keyword in [u'你好', u'感谢', u'开始', u'欢迎', u'准备好了', u'嗨']):
        if personality == 'humorous':
            greeting_action(motion, animation)
            humorous_quick_nod(motion)
        elif personality == 'gentle':
            gentle_bow(motion)
            gentle_wave(motion)
        else:
            greeting_action(motion, animation)
        return
    
    # 结束语关键词
    if any(keyword in text_u for keyword in [u'感谢', u'再见', u'祝你', u'结束', u'再见', u'欢迎回来', u'先到这里']):
        if personality == 'humorous':
            closing_action(motion)
            humorous_quick_nod(motion)
        elif personality == 'gentle':
            gentle_bow(motion)
            gentle_wave(motion)
        else:
            closing_action(motion)
        return
    
    # 根据性格选择专属动作
    if personality == 'humorous':
        # 幽默性格：随机选择幽默动作
        import random
        humorous_actions = [
            humorous_quick_nod,
            humorous_tilt_head,
            humorous_hip_sway,
            humorous_shrug,
            humorous_finger_circle,
            humorous_sway_forward_back
        ]
        # 根据文本内容选择特定动作
        if any(keyword in text_u for keyword in [u'不知道', u'不清楚', u'不确定']):
            humorous_shrug(motion)
        elif any(keyword in text_u for keyword in [u'看', u'观察', u'发现']):
            humorous_look_around(motion)
        elif any(keyword in text_u for keyword in [u'尴尬', u'不好意思', u'害羞']):
            humorous_cover_face(motion)
        else:
            # 随机选择一个幽默动作
            action = random.choice(humorous_actions)
            action(motion)
        return
    
    elif personality == 'gentle':
        # 温柔性格：随机选择温柔动作
        import random
        gentle_actions = [
            gentle_slow_nod,
            gentle_listen_tilt,
            gentle_hands_heart,
            gentle_invite_gesture,
            gentle_pat_shoulder,
            gentle_share_gesture,
            gentle_comforting_gesture
        ]
        # 根据文本内容选择特定动作
        if any(keyword in text_u for keyword in [u'听', u'倾听', u'了解']):
            gentle_listen_tilt(motion)
        elif any(keyword in text_u for keyword in [u'理解', u'明白', u'知道', u'感受']):
            gentle_hands_heart(motion)
        elif any(keyword in text_u for keyword in [u'邀请', u'欢迎', u'来吧']):
            gentle_invite_gesture(motion)
        elif any(keyword in text_u for keyword in [u'安慰', u'支持', u'陪伴']):
            gentle_comforting_gesture(motion)
        elif any(keyword in text_u for keyword in [u'分享', u'给你', u'递']):
            gentle_share_gesture(motion)
        else:
            # 随机选择一个温柔动作
            action = random.choice(gentle_actions)
            action(motion)
        return
    
    # 默认动作（如果没有指定性格）
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
    
    # 默认：倾听动作
    listening_action(motion)

def perform_action_during_speech(text, motion, animation, duration, personality=None):
    """在说话期间执行动作"""
    if motion is None:
        return
    
    import threading
    import random
    
    # 在说话期间持续执行动作
    def continuous_actions():
        action_count = 0
        while action_count < int(duration / 2.0):  # 每2秒执行一个动作
            try:
                if personality == 'humorous':
                    # 幽默性格：频繁执行各种幽默动作
                    humorous_actions = [
                        humorous_quick_nod,
                        humorous_tilt_head,
                        humorous_sway_forward_back
                    ]
                    action = random.choice(humorous_actions)
                    action(motion)
                    time.sleep(1.5)  # 动作间隔短
                elif personality == 'gentle':
                    # 温柔性格：缓慢执行温柔动作
                    gentle_actions = [
                        gentle_slow_nod,
                        gentle_listen_tilt
                    ]
                    action = random.choice(gentle_actions)
                    action(motion)
                    time.sleep(2.5)  # 动作间隔长
                else:
                    # 默认：定期点头
                    gentle_nod(motion, 1)
                    time.sleep(2.0)
                action_count += 1
            except:
                break
    
    # 启动持续动作线程
    action_thread = threading.Thread(target=continuous_actions)
    action_thread.daemon = True
    action_thread.start()

