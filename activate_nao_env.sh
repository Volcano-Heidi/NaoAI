#!/bin/bash

# 激活NAO环境的脚本

echo "激活NAO Python 2.7环境..."

# 初始化conda（自动检测路径）
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
    source "/opt/anaconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "/root/miniconda3/etc/profile.d/conda.sh" ]; then
    source "/root/miniconda3/etc/profile.d/conda.sh"
else
    echo "警告: 未找到conda，尝试使用系统conda命令"
    if ! command -v conda &> /dev/null; then
        echo "错误: 未找到conda，请先安装conda或miniconda"
        exit 1
    fi
fi

# 检查环境是否存在
if conda env list | grep -q "nao_env"; then
    echo "✓ 找到nao_env环境"
else
    echo "创建nao_env环境..."
    conda create -n nao_env python=2.7 -y
fi

# 激活环境
conda activate nao_env

echo "✓ 环境已激活"
echo "Python版本: $(python --version)"
echo ""
echo "现在可以运行："
echo "  python voice_counselor.py"
echo "  或"
echo "  python voice_counselor_simple.py"

