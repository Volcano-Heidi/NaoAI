# SoulChat2.0 集成说明

## 概述

代码已从 DeepSeek API 迁移到本地 SoulChat2.0 模型（通过 vLLM 提供 OpenAI 兼容 API）。

## 修改内容

### 1. `gpt3_code.py` 修改
- 将 API 端点从 `https://api.deepseek.com/chat/completions` 改为本地 `http://localhost:8001/v1/chat/completions`
- 将模型名称从 `deepseek-chat` 改为 `SoulChat2.0-Llama-3.1-8B`
- 支持通过环境变量配置 API 参数

### 2. 环境变量配置

#### 必需的环境变量（可选，有默认值）
- `SOULCHAT_API_KEY`: SoulChat2.0 API 密钥（默认：`soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30`）
- `SOULCHAT_API_URL`: API 服务地址（默认：`http://localhost:8001/v1/chat/completions`）
- `SOULCHAT_MODEL_NAME`: 模型名称（默认：`SoulChat2.0-Llama-3.1-8B`）

#### 其他环境变量（保持不变）
- `ROBOT_PERSONA`: 机器人人格设置
- `ROBOT_ID`: 机器人 ID
- `RESPONSE_MAX_WORDS`: 响应最大字数限制

## 使用步骤

### 1. 启动 SoulChat2.0 模型服务

首先确保 SoulChat2.0 模型已下载并配置好模型路径，然后运行：

```bash
cd /root
./start_soulchat.sh
```

或者手动设置模型路径：

```bash
export MODEL_NAME_OR_PATH=/path/to/your/SoulChat2.0-Llama-3.1-8B
./start_soulchat.sh
```

### 2. 验证服务运行

检查服务是否在端口 8001 上运行：

```bash
curl http://localhost:8001/v1/models
```

### 3. 运行您的应用

```bash
cd /root/NaoAI-Assistant-main
python2 keyboard_dialogue.py
```

或

```bash
python2 main.py
```

## 模型下载

如果还没有下载 SoulChat2.0 模型，可以使用以下方法：

### 方法 1：使用 ModelScope

```python
from modelscope import snapshot_download
model_dir = snapshot_download('YIRONGCHEN/SoulChat2.0-Llama-3.1-8B')
```

### 方法 2：使用 git-lfs

```bash
cd /root/models
git lfs install
git clone https://www.modelscope.cn/YIRONGCHEN/SoulChat2.0-Llama-3.1-8B.git
```

### 方法 3：使用 modelscope CLI

```bash
cd /root/models
modelscope download --model 'YIRONGCHEN/SoulChat2.0-Llama-3.1-8B' --include '*'
```

## 注意事项

1. **系统提示词**：根据 SoulChat2.0 文档，进行模型推理时需要加上系统提示词。当前代码中的 `system_text` 已经包含了系统提示词。

2. **模型路径**：确保 `start_soulchat.sh` 中的 `MODEL_NAME_OR_PATH` 指向正确的模型路径。

3. **端口冲突**：如果端口 8001 已被占用，可以修改 `start_soulchat.sh` 中的 `PORT` 环境变量，并相应更新 `SOULCHAT_API_URL`。

4. **API 兼容性**：SoulChat2.0 通过 vLLM 提供 OpenAI 兼容的 API，所以代码修改最小化，保持了原有的接口调用方式。

## 故障排除

### 问题：连接被拒绝
- 检查 SoulChat2.0 服务是否正在运行
- 检查端口是否正确（默认 8001）
- 查看 `start_soulchat.sh` 的输出日志

### 问题：模型路径不存在
- 确认模型已正确下载
- 设置正确的 `MODEL_NAME_OR_PATH` 环境变量

### 问题：API 密钥错误
- 检查 `start_soulchat.sh` 中的 `API_KEY` 是否与代码中的 `SOULCHAT_API_KEY` 匹配

## 参考链接

- SoulChat2.0 GitHub: https://github.com/scutcyr/SoulChat2.0
- vLLM 文档: https://docs.vllm.ai/

