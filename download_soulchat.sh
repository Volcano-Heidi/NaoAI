#!/bin/bash
# SoulChat2.0 模型下载脚本（使用 git-lfs 方法）

set -e

echo "=========================================="
echo "SoulChat2.0 模型下载脚本"
echo "=========================================="
echo ""

# 默认下载路径
DEFAULT_DOWNLOAD_DIR="$HOME/models"
DOWNLOAD_DIR="${1:-$DEFAULT_DOWNLOAD_DIR}"

# 模型仓库地址
MODEL_REPO="https://www.modelscope.cn/YIRONGCHEN/SoulChat2.0-Llama-3.1-8B.git"
MODEL_NAME="SoulChat2.0-Llama-3.1-8B"

echo "模型: $MODEL_NAME"
echo "下载路径: $DOWNLOAD_DIR"
echo ""
echo "注意: 模型大小约为 16GB，请确保有足够的磁盘空间"
echo ""

# 创建下载目录
mkdir -p "$DOWNLOAD_DIR"
cd "$DOWNLOAD_DIR"

# 检查是否已安装 git-lfs
if ! command -v git-lfs &> /dev/null; then
    echo "⚠️  未检测到 git-lfs"
    echo "正在尝试安装 git-lfs..."
    
    # 检测操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install git-lfs
        else
            echo "错误: 请先安装 Homebrew，然后运行: brew install git-lfs"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y git-lfs
        elif command -v yum &> /dev/null; then
            sudo yum install -y git-lfs
        else
            echo "错误: 请手动安装 git-lfs"
            exit 1
        fi
    else
        echo "错误: 不支持的操作系统，请手动安装 git-lfs"
        exit 1
    fi
fi

# 初始化 git-lfs
echo "初始化 git-lfs..."
git lfs install

# 检查模型是否已存在
if [ -d "$MODEL_NAME" ]; then
    echo ""
    echo "⚠️  检测到模型目录已存在: $DOWNLOAD_DIR/$MODEL_NAME"
    read -p "是否重新下载？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "使用现有模型: $DOWNLOAD_DIR/$MODEL_NAME"
        exit 0
    fi
    echo "删除旧模型..."
    rm -rf "$MODEL_NAME"
fi

# 克隆模型仓库
echo ""
echo "开始下载模型..."
echo "这可能需要较长时间，请耐心等待..."
echo ""

git clone "$MODEL_REPO" "$MODEL_NAME"

echo ""
echo "=========================================="
echo "✓ 下载完成！"
echo "=========================================="
echo "模型路径: $DOWNLOAD_DIR/$MODEL_NAME"
echo ""
echo "使用说明:"
echo "1. 设置环境变量: export MODEL_NAME_OR_PATH=$DOWNLOAD_DIR/$MODEL_NAME"
echo "2. 启动 SoulChat 服务: ./start_soulchat.sh"
echo "=========================================="

