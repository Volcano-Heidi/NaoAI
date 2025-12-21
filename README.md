# NAO 心理咨询师系统

一个基于 NAO 机器人的智能心理咨询师系统，支持三种不同性格（幽默、温柔、专业），集成大语言模型（SoulChat2.0）和 NAO 机器人动作系统。

## ✨ 功能特点

- 🎭 **三种性格选择**：幽默、温柔、专业，每种性格有独特的语言风格和交互方式
- 🤖 **NAO 机器人集成**：支持 NAO 机器人语音回复和肢体动作
- 🧠 **大语言模型**：使用 SoulChat2.0 模型生成个性化心理咨询回复
- 💬 **智能对话**：8 阶段结构化心理咨询流程
- 🎯 **动作系统**：根据性格和对话内容自动执行相应的肢体动作
- 💾 **会话管理**：自动保存对话历史和咨询进度

## 📋 系统要求

### 必需
- Python 2.7（NAO SDK 要求）
- SoulChat2.0 模型服务（通过 vLLM 运行）
- NAOqi SDK（macOS 或 Linux 版本）

### 可选
- NAO 机器人硬件（用于语音和动作）
- 麦克风设备（用于语音输入，如果使用语音模式）

## 🚀 快速开始

### 1. 环境准备

#### macOS 环境

```bash
# 安装依赖
./install_dependencies.sh

# 激活环境
./activate_nao_env.sh

# 检查 NAO SDK
python2 check_nao_sdk.py
```

详细设置请参考：[macOS 迁移指南](MACOS_MIGRATION.md)

#### Linux 环境

```bash
# 安装依赖
./install_dependencies.sh

# 设置 NAO SDK
./setup_nao_sdk.sh
```

### 2. 下载 SoulChat2.0 模型

```bash
# 方法1: 使用 Python 脚本
python3 download_soulchat.py ~/models

# 方法2: 使用 Shell 脚本
./download_soulchat.sh ~/models
```

模型大小约 16GB，下载可能需要一些时间。

### 3. 启动 SoulChat2.0 服务

```bash
# 设置模型路径
export MODEL_NAME_OR_PATH=~/models/YIRONGCHEN/SoulChat2.0-Llama-3.1-8B

# 启动 vLLM 服务（需要 GPU）
python -m vllm.entrypoints.openai.api_server \
    --served-model-name SoulChat2.0-Llama-3.1-8B \
    --model $MODEL_NAME_OR_PATH \
    --port 8001 \
    --api-key soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30
```

详细设置请参考：[SoulChat2.0 设置指南](SOULCHAT_SETUP.md)

### 4. 配置 NAO 机器人（可选）

```bash
# 设置 NAO 机器人 IP
export NAO_IP=192.168.10.3
export NAO_PORT=9559
```

如果不使用 NAO 硬件，系统会自动切换到文本模式。

### 5. 启动系统

```bash
./start_personality_counselor.sh
```

或直接运行：

```bash
python2 personality_counselor.py
```

## 🎭 性格说明

### 幽默性格
- **语言风格**：轻松幽默，使用年轻人的语言，适当使用 Emoji
- **动作风格**：活泼、动作幅度较大
- **适用场景**：适合需要轻松氛围的来访者
- **开场白**："哈喽！感谢你愿意来找我聊天。我是你的AI心理支持助手..."

### 温柔性格
- **语言风格**：温暖、舒缓、包容、耐心
- **动作风格**：温和、动作幅度较小
- **适用场景**：适合需要情感支持的来访者
- **开场白**："你好呀，我是你的AI心理咨询师。真的非常感谢你愿意来到这里..."

### 专业性格
- **语言风格**：专业、冷静、尊重、客观
- **动作风格**：正式、动作较为克制
- **适用场景**：适合需要专业分析的来访者
- **开场白**："你好，感谢你来到这里。我是你的心理支持助手..."

## 📖 使用流程

1. **选择性格**：首次运行时会提示选择性格（1. 幽默 / 2. 温柔 / 3. 专业）
2. **开始对话**：系统会使用所选性格的开场白开始
3. **进行咨询**：输入您的问题或想法，NAO 会根据性格特点回复
4. **结束对话**：输入 `quit`、`exit`、`退出` 或 `回答完毕` 结束对话

## 📁 项目结构

### 核心文件

- `personality_counselor.py` - 主程序（带性格选择）
- `personality_config.py` - 性格配置和 Prompt
- `nao_motions.py` - NAO 动作库
- `nao_sdk_helper.py` - NAO SDK 辅助工具
- `gpt3_code.py` - LLM 调用（SoulChat2.0）
- `nao_tts_code.py` - 文本转语音模块

### 启动脚本

- `start_personality_counselor.sh` - 主启动脚本

### 工具脚本

- `check_nao_sdk.py` - 检查 NAO SDK 配置
- `find_naoqi_sdk.py` - 查找 NAOqi SDK
- `diagnose_nao_connection.py` - 诊断 NAO 连接
- `install_dependencies.sh` - 安装依赖
- `setup_nao_sdk.sh` - 设置 NAO SDK

### 文档

- `PERSONALITY_COUNSELOR_README.md` - 详细使用说明
- `PROMPT_INTEGRATION_SUMMARY.md` - Prompt 集成说明
- `SOULCHAT_SETUP.md` - SoulChat2.0 设置指南
- `NAO_SDK_SETUP.md` - NAO SDK 设置指南
- `MACOS_MIGRATION.md` - macOS 环境迁移指南
- `NAO_MOTIONS_README.md` - NAO 动作系统说明

## 🔧 配置说明

### 环境变量

```bash
# SoulChat2.0 配置
export SOULCHAT_API_KEY="your-api-key"
export SOULCHAT_BASE_URL="http://localhost:8001/v1"
export SOULCHAT_MODEL_NAME="SoulChat2.0-Llama-3.1-8B"

# NAO 机器人配置
export NAO_IP="192.168.10.3"
export NAO_PORT="9559"

# NAOqi SDK 配置
export PYNAOQI_PATH="/path/to/pynaoqi"
```

### 会话管理

对话历史保存在 `counseling_session.json` 文件中。如需重新选择性格，删除此文件即可。

## 🐛 故障排除

### 无法连接到 SoulChat2.0

1. 检查服务是否运行：`curl http://localhost:8001/v1/models`
2. 检查端口是否正确（默认 8001）
3. 查看 [SoulChat2.0 设置指南](SOULCHAT_SETUP.md)

### 无法连接到 NAO 机器人

1. 检查 NAO_IP 是否正确设置
2. 检查 NAO 机器人是否已开机
3. 运行 `python2 check_nao_sdk.py` 检查 SDK 配置
4. 运行 `python2 diagnose_nao_connection.py` 诊断连接

### NAO SDK 未找到

1. 设置 PYNAOQI_PATH 环境变量
2. 运行 `python2 find_naoqi_sdk.py` 查找 SDK
3. 查看 [NAO SDK 设置指南](NAO_SDK_SETUP.md)

## 📚 相关文档

- [详细使用说明](PERSONALITY_COUNSELOR_README.md)
- [Prompt 集成说明](PROMPT_INTEGRATION_SUMMARY.md)
- [SoulChat2.0 设置](SOULCHAT_SETUP.md)
- [NAO SDK 设置](NAO_SDK_SETUP.md)
- [macOS 迁移指南](MACOS_MIGRATION.md)
- [NAO 动作系统](NAO_MOTIONS_README.md)

## 🤝 贡献

本项目基于 NAO 机器人和 SoulChat2.0 模型开发，支持三种性格的心理咨询师系统。

## 📝 许可证

本项目为学术研究项目。

## 🔗 相关链接

- [SoulChat2.0 GitHub](https://github.com/scutcyr/SoulChat2.0)
- [vLLM 文档](https://docs.vllm.ai/)
- [NAO 机器人官网](https://www.aldebaran.com/)

---

**注意**：本项目需要 Python 2.7（NAO SDK 要求）和 SoulChat2.0 模型服务。请确保环境配置正确。
