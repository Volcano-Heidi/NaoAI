# SoulChat2.0 集成说明

## 概述

项目已成功从 DeepSeek API 迁移到本地部署的 SoulChat2.0 模型服务。

## 配置说明

### 1. 启动 SoulChat2.0 模型服务

首先需要启动 vLLM 服务：

```bash
cd /root
./start_soulchat.sh
```

或者手动设置环境变量后启动：

```bash
export MODEL_NAME_OR_PATH=/path/to/your/SoulChat2.0/model
export GPU_MEMORY_UTILIZATION=0.8
export PORT=8001
export API_KEY=soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30
export MAX_MODEL_LEN=20000

python -m vllm.entrypoints.openai.api_server \
    --served-model-name SoulChat2.0-Llama-3.1-8B \
    --model $MODEL_NAME_OR_PATH \
    --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
    --port $PORT \
    --api-key $API_KEY \
    --max-model-len $MAX_MODEL_LEN
```

### 2. 环境变量配置（可选）

如果需要自定义配置，可以设置以下环境变量：

```bash
# API Key（默认使用启动脚本中的值）
export SOULCHAT_API_KEY="your-api-key"

# API 基础 URL（默认: http://localhost:8001/v1）
export SOULCHAT_BASE_URL="http://localhost:8001/v1"

# 模型名称（默认: SoulChat2.0-Llama-3.1-8B）
export SOULCHAT_MODEL_NAME="SoulChat2.0-Llama-3.1-8B"
```

### 3. 代码修改说明

主要修改文件：`gpt3_code.py`

**修改内容：**
- ✅ 将 DeepSeek API 端点替换为本地 SoulChat2.0 vLLM 服务
- ✅ 更新模型名称为 `SoulChat2.0-Llama-3.1-8B`
- ✅ 使用环境变量支持灵活配置
- ✅ 保持原有的错误处理和重试机制

**API 端点变化：**
- 原：`https://api.deepseek.com/chat/completions`
- 新：`http://localhost:8001/v1/chat/completions`

## 使用说明

### 运行项目

```bash
cd /root/NaoAI-Assistant-main
python2 main.py
```

或者使用键盘对话模式：

```bash
python2 keyboard_dialogue.py
```

### 验证服务

确保 SoulChat2.0 服务正在运行：

```bash
# 检查端口
netstat -tlnp | grep 8001
# 或
ss -tlnp | grep 8001

# 测试 API
curl http://localhost:8001/v1/models \
  -H "Authorization: Bearer soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30"
```

## 注意事项

1. **模型路径**：确保 `MODEL_NAME_OR_PATH` 指向正确的模型文件路径
2. **GPU 内存**：根据您的 GPU 显存调整 `GPU_MEMORY_UTILIZATION`
3. **系统提示词**：SoulChat2.0 模型推理时需要添加系统提示词，具体内容可参考 [SoulChat2.0 数据集](https://github.com/scutcyr/SoulChat2.0) 中的 `system_prompt`
4. **模型下载**：如果还没有模型，可以从 [ModelScope](https://modelscope.cn/models/YIRONGCHEN/SoulChat2.0-Llama-3.1-8B) 下载

## 参考链接

- [SoulChat2.0 GitHub](https://github.com/scutcyr/SoulChat2.0)
- [vLLM 文档](https://docs.vllm.ai/)

