#!/bin/bash

# 启动带性格选择的心理咨询师

echo "=========================================="
echo "NAO 心理咨询师系统（性格选择版）"
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

# 检查SoulChat2.0服务
echo "检查SoulChat2.0服务..."
if ! curl -s http://localhost:8001/v1/models > /dev/null 2>&1; then
    echo "⚠️  警告: SoulChat2.0服务未运行"
    echo "请先启动SoulChat2.0服务:"
    echo "  设置 MODEL_NAME_OR_PATH 环境变量后运行 vLLM 服务"
    echo "  或参考 SOULCHAT_SETUP.md 文档"
    echo ""
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ SoulChat2.0服务运行正常"
fi

echo ""

# 检查NAO连接
if [ -z "$NAO_IP" ]; then
    echo "⚠️  未设置NAO_IP环境变量"
    echo "提示: 设置NAO_IP后，NAO将语音回复并执行动作"
    echo "      export NAO_IP=你的NAO机器人IP地址"
    echo ""
    echo "当前将使用文本模式"
else
    echo "✓ NAO机器人IP: $NAO_IP"
fi

echo ""
echo "=========================================="
echo "启动心理咨询师系统..."
echo "=========================================="
echo ""

# 运行主程序
python2 personality_counselor.py

