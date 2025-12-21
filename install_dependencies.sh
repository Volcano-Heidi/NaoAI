#!/bin/bash

# 安装NAO语音对话系统所需依赖

echo "=========================================="
echo "安装NAO语音对话系统依赖"
echo "=========================================="
echo ""

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
    echo "警告: 未找到conda配置文件，尝试使用系统conda命令"
    if ! command -v conda &> /dev/null; then
        echo "错误: 未找到conda，请先安装conda或miniconda"
        echo "macOS安装方法: brew install miniconda 或访问 https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
fi

# 检查并创建环境
if ! conda env list | grep -q "nao_env"; then
    echo "创建Python 2.7环境..."
    conda create -n nao_env python=2.7 -y
fi

# 激活环境
echo "激活Python 2.7环境..."
conda activate nao_env

echo ""
echo "安装Python依赖包..."
echo ""

# 安装SpeechRecognition
echo "1. 安装 SpeechRecognition..."
pip install SpeechRecognition

# 尝试安装PyAudio（可能需要系统库）
echo ""
echo "2. 安装 PyAudio..."
pip install pyaudio 2>&1 | grep -E "(Successfully|error|Error)" || echo "   PyAudio安装可能需要系统库支持"

# 尝试安装pyttsx3（可选，用于系统TTS）
echo ""
echo "3. 安装 pyttsx3 (可选，用于系统TTS)..."
pip install pyttsx3 2>&1 | grep -E "(Successfully|error|Error)" || echo "   pyttsx3安装失败（可选）"

# 安装requests（通常已安装，但确保）
echo ""
echo "4. 确保 requests 已安装..."
pip install requests 2>&1 | grep -E "(already|Successfully)" || pip install requests

echo ""
echo "=========================================="
echo "依赖安装完成！"
echo "=========================================="
echo ""
echo "验证安装："
python -c "import speech_recognition; print('✓ SpeechRecognition 已安装')" 2>&1
python -c "import requests; print('✓ requests 已安装')" 2>&1
echo ""
echo "现在可以运行："
echo "  ./run_voice_counselor.sh"
echo ""

