# macOS 系统配置指南

如果您在 **macOS 系统**上运行，可以使用 macOS 版本的 NAOqi SDK。

## 当前状态

✓ 您已经有了 macOS 版本的 qi 包：
- `qi/_qi.so` (macOS Mach-O 格式)
- `qi/_inaoqi.so` (macOS 格式)
- `qi/_allog.so` (macOS 格式)
- `qi/naoqi.py` (包含 ALProxy 类)

## macOS 配置步骤

### 1. 确保在 macOS 系统上

```bash
# 检查系统
uname -a
# 应该显示 Darwin 或 macOS 相关信息
```

### 2. 设置 Python 2.7 环境

```bash
# 创建 conda 环境（如果还没有）
conda create -n nao_env python=2.7
conda activate nao_env

# 安装必要的包
pip install SpeechRecognition==3.8.1
conda install pyaudio
```

### 3. 配置 NAOqi SDK

由于 qi 包已经在项目目录中，系统会自动使用它。

### 4. 设置 NAO 机器人 IP

```bash
export NAO_IP=192.168.10.3
export NAO_PORT=9559
```

### 5. 测试连接

```bash
cd /path/to/NaoAI-Assistant-main
python -c "
import sys
sys.path.insert(0, '.')
from qi import naoqi
import os

nao_ip = os.environ.get('NAO_IP', '192.168.10.3')
tts = naoqi.ALProxy('ALTextToSpeech', nao_ip, 9559)
print('✓ 成功连接到 NAO 机器人！')
"
```

### 6. 启动语音咨询系统

```bash
./run_voice_counselor.sh
```

## 注意事项

1. **系统兼容性**：macOS 版本的 SDK 只能在 macOS 系统上运行
2. **Python 版本**：需要 Python 2.7（NAOqi SDK 的要求）
3. **网络连接**：确保能访问 NAO 机器人的 IP 地址

## 如果当前在 Linux 系统

如果您当前在 Linux 系统上，有两个选择：

1. **切换到 macOS 系统**：在 macOS 上运行程序
2. **获取 Linux 版本 SDK**：下载 Linux 版本的 NAOqi SDK

## 验证配置

运行以下命令验证：

```bash
python check_nao_sdk.py
```

如果显示 "✓ 找到 NAOqi SDK" 和 "✓ 可以导入 ALProxy"，说明配置成功！

