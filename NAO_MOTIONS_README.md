# NAO机器人心理咨询师动作系统

## 概述

为NAO机器人设计了专门的心理咨询师动作库，让机器人在说话时能够做出相应的动作，增强交互的真实感和共情效果。

## 动作库

### 1. 开场问候动作 (greeting_action)
- **触发时机**: 开场白、欢迎语
- **动作内容**: 
  - 友好的挥手
  - 点头致意
- **适用场景**: 咨询开始时的问候

### 2. 倾听动作 (listening_action)
- **触发时机**: 默认动作，当没有特定关键词时
- **动作内容**:
  - 轻微点头
  - 身体稍微前倾
- **适用场景**: 倾听来访者说话时

### 3. 思考动作 (thinking_action)
- **触发时机**: 包含"让我"、"我想"、"考虑"、"分析"等关键词
- **动作内容**:
  - 头部倾斜
  - 手部思考手势
- **适用场景**: 需要思考或分析时

### 4. 鼓励动作 (encouraging_action)
- **触发时机**: 包含"很好"、"不错"、"可以"、"一定"等鼓励性词汇
- **动作内容**:
  - 点头肯定
  - 手臂张开（鼓励手势）
- **适用场景**: 鼓励来访者时

### 5. 共情动作 (empathetic_action)
- **触发时机**: 包含"理解"、"感受"、"明白"、"知道"等共情词汇
- **动作内容**:
  - 双手放在胸前
  - 轻微点头
- **适用场景**: 表达理解和共情时

### 6. 提问动作 (questioning_action)
- **触发时机**: 包含问号或"什么"、"怎么"、"为什么"等疑问词
- **动作内容**:
  - 头部倾斜（表示疑问）
  - 手部指向或手势
- **适用场景**: 向来访者提问时

### 7. 结束动作 (closing_action)
- **触发时机**: 包含"感谢"、"再见"、"祝你"、"结束"等结束语
- **动作内容**:
  - 挥手告别
  - 点头致意
- **适用场景**: 咨询结束时

### 8. 温和点头 (gentle_nod)
- **触发时机**: 说话期间定期执行
- **动作内容**: 轻微的点头
- **适用场景**: 表示理解和关注

## 动作触发机制

### 自动识别
系统会根据说话内容自动识别关键词，选择相应的动作：

```python
# 关键词匹配示例
开场: "你好"、"感谢"、"开始"、"欢迎"
结束: "感谢"、"再见"、"祝你"、"结束"
提问: "？"、"什么"、"怎么"、"为什么"
鼓励: "很好"、"不错"、"可以"、"一定"
共情: "理解"、"感受"、"明白"、"知道"
思考: "让我"、"我想"、"考虑"、"分析"
```

### 动作执行时机
1. **说话前**: 根据文本内容预判，执行相应动作
2. **说话中**: 定期执行倾听动作（点头）
3. **说话后**: 执行温和点头，表示完成

## 使用方法

### 自动集成
动作系统已自动集成到 `nao_tts_code.py` 中，无需额外配置。

### 手动调用
如果需要手动控制动作：

```python
from nao_motions import *

motion, animation, posture = get_nao_proxies()
if motion is not None:
    # 执行特定动作
    greeting_action(motion, animation)
    listening_action(motion)
    encouraging_action(motion)
    # ...
```

## 动作参数调整

### 动作速度
在 `nao_motions.py` 中可以调整动作的 `times` 参数来控制速度：

```python
# 快速动作
times = [0.2, 0.4, 0.6]  # 较快

# 慢速动作
times = [0.5, 1.0, 1.5]  # 较慢，更自然
```

### 动作幅度
调整 `angles` 参数来控制动作幅度：

```python
# 大幅度动作
angles = [0.5, 0.3, -1.5, -0.3]  # 更明显

# 小幅度动作
angles = [0.2, 0.1, -0.5, -0.1]  # 更温和
```

## 动作设计原则

1. **自然流畅**: 动作过渡平滑，避免突兀
2. **符合场景**: 动作与心理咨询场景匹配
3. **适度表达**: 不过度夸张，保持专业
4. **共情导向**: 动作传达理解和支持
5. **非干扰性**: 动作不干扰对话内容

## 动作组合建议

### 开场流程
```
1. 站立初始化
2. 挥手问候
3. 点头致意
4. 开始说话
```

### 倾听流程
```
1. 身体前倾
2. 轻微点头
3. 保持倾听姿势
```

### 提问流程
```
1. 头部倾斜（疑问）
2. 手部指向
3. 等待回答
```

### 结束流程
```
1. 挥手告别
2. 点头致意
3. 恢复初始姿势
```

## 故障排除

### 问题1: 动作不执行
- 检查NAO_IP环境变量是否正确
- 检查NAO机器人是否在线
- 检查网络连接

### 问题2: 动作不流畅
- 调整动作的times参数
- 检查NAO机器人电量
- 确保机器人处于站立状态

### 问题3: 动作与语音不同步
- 系统会自动估算语音时长
- 可以手动调整estimated_duration

## 扩展动作

### 添加新动作
在 `nao_motions.py` 中添加新函数：

```python
def my_custom_action(motion):
    """自定义动作"""
    if motion is None:
        return
    try:
        names = ["HeadPitch"]
        angles = [0.2]
        times = [0.3]
        motion.angleInterpolation(names, angles, times, True)
    except Exception as e:
        print("Action error: %s" % e)
```

### 添加触发条件
在 `select_action_by_text` 函数中添加：

```python
if any(keyword in text for keyword in [u'你的关键词']):
    my_custom_action(motion)
    return
```

## 注意事项

1. **安全第一**: 确保动作不会让机器人失去平衡
2. **电量管理**: 动作会消耗电量，注意监控
3. **空间要求**: 确保机器人周围有足够空间
4. **动作幅度**: 根据实际环境调整动作幅度
5. **测试验证**: 在实际使用前充分测试动作

## 技术细节

### 使用的NAO API
- `ALMotion`: 控制关节运动
- `ALAnimationPlayer`: 播放预定义动画（可选）
- `ALRobotPosture`: 控制机器人姿势

### 关节控制
主要控制的关节：
- `HeadPitch`: 头部俯仰
- `HeadYaw`: 头部左右
- `LShoulderPitch/RShoulderPitch`: 肩膀俯仰
- `LShoulderRoll/RShoulderRoll`: 肩膀旋转
- `LElbowYaw/RElbowYaw`: 肘部左右
- `LElbowRoll/RElbowRoll`: 肘部旋转
- `HipPitch`: 髋部俯仰

## 参考资源

- [NAOqi API文档](http://doc.aldebaran.com/)
- [ALMotion API](http://doc.aldebaran.com/2-8/naoqi/motion/almotion-api.html)
- [ALAnimationPlayer API](http://doc.aldebaran.com/2-8/naoqi/motion/alanimationplayer-api.html)

