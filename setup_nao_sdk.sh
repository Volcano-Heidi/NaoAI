#!/bin/bash

# NAOqi SDK配置脚本

echo "=========================================="
echo "NAOqi SDK 配置助手"
echo "=========================================="
echo ""

# 获取脚本所在目录
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
    else
        echo "警告: nao_env环境不存在，将使用系统Python"
    fi
fi

# 检查SDK
echo "检查NAOqi SDK..."
python check_nao_sdk.py

echo ""
echo "=========================================="
echo "如果未找到SDK，请按以下步骤操作："
echo "=========================================="
echo ""

# 检测系统类型
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到 macOS 系统"
    echo ""
    echo "1. 下载NAOqi SDK (macOS版本)"
    echo "   访问: https://www.aldebaran.com/en/support/nao-6/downloads"
    echo "   或搜索: pynaoqi-python2.7-2.8.6.23-mac64"
    echo ""
    echo "2. 解压SDK到某个目录，例如："
    echo "   ~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4"
    echo "   或项目目录: $SCRIPT_DIR/pynaoqi-python2.7-2.8.6.23-mac64"
    echo ""
    echo "3. 设置环境变量："
    echo "   export PYNAOQI_PATH=~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231\\ 4"
    echo "   echo 'export PYNAOQI_PATH=~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231\\ 4' >> ~/.zshrc"
    echo "   或 ~/.bash_profile (如果使用bash)"
else
    echo "检测到 Linux 系统"
    echo ""
    echo "1. 下载NAOqi SDK (Linux版本)"
    echo "   访问: https://www.aldebaran.com/en/support/nao-6/downloads"
    echo "   或搜索: pynaoqi-python2.7-2.8.6.23-linux64"
    echo ""
    echo "2. 解压SDK到某个目录，例如："
    echo "   ~/pynaoqi-python2.7-2.8.6.23-linux64"
    echo "   或 /opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64"
    echo ""
    echo "3. 设置环境变量："
    echo "   export PYNAOQI_PATH=~/pynaoqi-python2.7-2.8.6.23-linux64"
    echo "   echo 'export PYNAOQI_PATH=~/pynaoqi-python2.7-2.8.6.23-linux64' >> ~/.bashrc"
fi

echo ""
echo "4. 重新运行检查："
echo "   python check_nao_sdk.py"
echo ""

