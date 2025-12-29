#!/bin/bash

# 启动带性格选择的心理咨询师（使用 DeepSeek API）

echo "=========================================="
echo "NAO 心理咨询师系统（性格选择版）"
echo "使用 DeepSeek API"
echo "=========================================="
echo ""

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 初始化conda（自动检测路径）
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
    source "/opt/anaconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then
    source "/root/miniconda3/etc/profile.d/conda.sh"
fi

# 检查并激活环境
if command -v conda &> /dev/null; then
    if conda env list | grep -q "nao_env"; then
        conda activate nao_env
        echo "✓ 已激活 nao_env 环境"
    else
        echo "⚠  nao_env 环境不存在，将使用系统 Python"
    fi
fi

echo ""

# 检查 DeepSeek API 配置
echo "检查 DeepSeek API 配置..."
if [ -z "$DEEPSEEK_API_KEY" ]; then
    # 如果没有设置环境变量，使用代码中的默认值
    echo "⚠️  提示: 未设置 DEEPSEEK_API_KEY 环境变量"
    echo "将使用代码中的默认 API Key"
    echo "如需设置环境变量，可以运行："
    echo "  export DEEPSEEK_API_KEY='sk-d93e850223e548578946315a173c6b70'"
else
    echo "✓ DeepSeek API Key 已设置"
fi

echo ""

# 检查百度语音识别 API 配置
echo "检查百度语音识别 API 配置..."
if [ -z "$BAIDU_ASR_API_KEY" ] || [ -z "$BAIDU_ASR_SECRET" ]; then
    echo "⚠️  提示: 未设置百度语音识别 API 环境变量"
    echo "将使用代码中的默认配置"
    echo "如需设置环境变量，可以运行："
    echo "  export BAIDU_ASR_API_KEY='we9cxZ31lcySBTow6G6cqUqm'"
    echo "  export BAIDU_ASR_SECRET='pUwUWRWj6yKEdiee1y3ijS8LnPdiDoSw'"
else
    echo "✓ 百度语音识别 API 配置已设置"
fi

echo ""

# 检查NAO连接
if [ -z "$NAO_IP" ]; then
    # 设置默认 IP
    export NAO_IP=192.168.10.4
    export NAO_PORT=9559
    echo "✓ 使用默认 NAO IP: $NAO_IP"
else
    echo "✓ NAO机器人IP: $NAO_IP"
fi

# 确保端口已设置
if [ -z "$NAO_PORT" ]; then
    export NAO_PORT=9559
fi

echo ""
echo "=========================================="
echo "启动心理咨询师系统..."
echo "=========================================="
echo ""

# 运行主程序（使用 DeepSeek 版本）
python2 personality_counselor_deepseek.py

