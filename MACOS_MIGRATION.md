# macOS 环境迁移指南

## 概述

本项目已从 Linux 环境迁移到 macOS 环境。本文档说明迁移后的配置和使用方法。

## 已完成的迁移工作

### 1. SDK 路径检测
- ✅ 更新 `nao_sdk_helper.py` 支持 macOS pynaoqi 路径
- ✅ 更新 `find_naoqi_sdk.py` 添加 macOS 路径搜索
- ✅ 更新 `check_nao_sdk.py` 显示 macOS 路径提示

### 2. 脚本适配
- ✅ 更新所有脚本的 conda 路径检测（支持 macOS 常见路径）
- ✅ 移除硬编码的 `/root` 路径
- ✅ 添加自动路径检测功能

### 3. 环境配置
- ✅ 支持 macOS 的 conda/miniconda/anaconda 安装路径
- ✅ 支持 zsh 和 bash shell

## macOS 环境配置步骤

### 1. 确认 pynaoqi SDK 位置

您的 pynaoqi SDK 位于：
```
/Users/heidi/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4
```

系统会自动检测此路径，或您可以手动设置环境变量：

```bash
export PYNAOQI_PATH="/Users/heidi/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4"
```

### 2. 设置 Python 2.7 环境

#### 使用 conda（推荐）

```bash
# 创建 Python 2.7 环境
conda create -n nao_env python=2.7 -y

# 激活环境
conda activate nao_env

# 安装依赖
pip install SpeechRecognition==3.8.1
conda install pyaudio -y
```

#### 使用系统 Python 2.7（如果已安装）

```bash
# macOS 通常自带 Python 2.7，但建议使用 conda
python2 --version
```

### 3. 验证 NAOqi SDK

```bash
cd /Users/heidi/Downloads/NaoAI-main
python check_nao_sdk.py
```

如果显示 "✓ 找到NAOqi SDK" 和 "✓ 可以导入ALProxy"，说明配置成功。

### 4. 设置 NAO 机器人 IP

```bash
export NAO_IP=192.168.10.3  # 替换为您的 NAO 机器人 IP
export NAO_PORT=9559
```

将环境变量添加到 shell 配置文件（永久设置）：

```bash
# 对于 zsh（macOS 默认）
echo 'export NAO_IP=192.168.10.3' >> ~/.zshrc
echo 'export NAO_PORT=9559' >> ~/.zshrc

# 对于 bash
echo 'export NAO_IP=192.168.10.3' >> ~/.bash_profile
echo 'export NAO_PORT=9559' >> ~/.bash_profile
```

### 5. 安装依赖

运行安装脚本（会自动检测 conda 路径）：

```bash
./install_dependencies.sh
```

或手动安装：

```bash
conda activate nao_env
pip install SpeechRecognition requests
conda install pyaudio -y
```

## 运行项目

### 1. 键盘对话模式

```bash
conda activate nao_env
python2 keyboard_dialogue.py
```

### 2. 语音咨询师

```bash
./run_voice_counselor.sh
```

或

```bash
./start_voice_counselor.sh
```

### 3. 主程序

```bash
conda activate nao_env
python2 main.py
```

## macOS 特定注意事项

### 1. 权限设置

macOS 可能需要授予麦克风权限：
- 系统偏好设置 → 安全性与隐私 → 隐私 → 麦克风
- 确保终端或 Python 有麦克风访问权限

### 2. PyAudio 安装

如果 `pip install pyaudio` 失败，可以：

```bash
# 使用 conda 安装（推荐）
conda install pyaudio -y

# 或使用 Homebrew 安装 portaudio 后安装
brew install portaudio
pip install pyaudio
```

### 3. 网络连接

确保 macOS 和 NAO 机器人在同一网络中，可以互相访问。

### 4. conda 路径

脚本会自动检测以下 conda 路径：
- `~/miniconda3/etc/profile.d/conda.sh`
- `/opt/anaconda3/etc/profile.d/conda.sh`
- `~/anaconda3/etc/profile.d/conda.sh`
- `/root/miniconda3/etc/profile.d/conda.sh` (Linux 兼容)

如果您的 conda 在其他位置，可以手动设置：

```bash
source /path/to/your/conda/etc/profile.d/conda.sh
```

## 故障排除

### 问题：找不到 NAOqi SDK

**解决方案：**
1. 检查 pynaoqi 目录是否存在
2. 设置 `PYNAOQI_PATH` 环境变量
3. 运行 `python check_nao_sdk.py` 查看详细错误信息

### 问题：conda 命令未找到

**解决方案：**
1. 安装 miniconda 或 anaconda
2. 或手动设置 conda 路径
3. 或使用系统 Python（不推荐）

### 问题：无法连接到 NAO 机器人

**解决方案：**
1. 检查 NAO 机器人是否开机
2. 检查网络连接（ping NAO_IP）
3. 检查防火墙设置
4. 确认 NAO_IP 和 NAO_PORT 设置正确

### 问题：麦克风不可用

**解决方案：**
1. 检查 macOS 麦克风权限
2. 检查 PyAudio 是否正确安装
3. 尝试使用 NAO 机器人的麦克风（设置 NAO_IP）

## 与 Linux 环境的差异

| 项目 | Linux | macOS |
|------|-------|-------|
| conda 路径 | `/root/miniconda3` | `~/miniconda3` 或 `/opt/anaconda3` |
| shell | bash | zsh (默认) |
| SDK 路径 | `/root/pynaoqi-...` | `~/Downloads/pynaoqi-...` |
| 配置文件 | `~/.bashrc` | `~/.zshrc` 或 `~/.bash_profile` |

## 参考文档

- `SETUP_MACOS.md` - macOS 原始设置指南
- `NAO_SDK_SETUP.md` - NAO SDK 详细设置
- `SOULCHAT_SETUP.md` - SoulChat2.0 模型设置

## 更新日志

- 2024-12-20: 完成从 Linux 到 macOS 的迁移
  - 更新所有脚本支持 macOS conda 路径
  - 添加 macOS pynaoqi SDK 路径检测
  - 移除硬编码的 Linux 路径

