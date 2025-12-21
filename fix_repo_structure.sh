#!/bin/bash

# 修复仓库结构，确保文件在根目录

echo "=========================================="
echo "修复 GitHub 仓库结构"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 检查当前目录
CURRENT_DIR=$(pwd)
echo "当前目录: $CURRENT_DIR"
echo ""

# 检查 Git 仓库根目录
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$GIT_ROOT" ]; then
    echo "Git 仓库根目录: $GIT_ROOT"
    echo ""
    
    # 如果 Git 根目录不是当前目录，需要切换到根目录
    if [ "$GIT_ROOT" != "$CURRENT_DIR" ]; then
        echo "⚠️  警告：Git 仓库根目录不是当前目录！"
        echo "Git 根目录: $GIT_ROOT"
        echo "当前目录: $CURRENT_DIR"
        echo ""
        echo "这可能是问题所在。"
        echo "建议在 Git 根目录执行此脚本。"
        echo ""
        read -p "是否继续？(yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            exit 0
        fi
    fi
else
    echo "当前目录不是 Git 仓库，初始化..."
    git init
    GIT_ROOT=$(pwd)
fi

# 检查是否有 Downloads/NaoAI-main 路径的文件
echo "检查文件路径..."
WRONG_PATH_FILES=$(git ls-files 2>/dev/null | grep "^Downloads/NaoAI-main/" | head -5)
if [ -n "$WRONG_PATH_FILES" ]; then
    echo "⚠️  发现文件在错误的路径: Downloads/NaoAI-main/"
    echo "这些文件需要移动到根目录"
    echo ""
fi

# 确保在正确的目录
cd "$GIT_ROOT"

# 添加所有文件（确保在根目录）
echo "添加所有文件到暂存区..."
git add .
echo "✓ 文件已添加"
echo ""

# 显示将要提交的文件
echo "将要提交的文件（前20个）："
git status --short | head -20
echo "..."

# 检查 README.md 位置
if [ -f "README.md" ]; then
    echo ""
    echo "✓ README.md 在根目录"
    echo "第一行: $(head -1 README.md)"
else
    echo ""
    echo "✗ README.md 不在根目录！"
fi

# 提交
echo ""
echo "提交更改..."
git commit -m "修复仓库结构：将所有文件移到根目录

- 移除错误的 Downloads/NaoAI-main/ 路径
- 更新 README 和所有文档
- 清理旧文件和无关代码
- 添加性格选择功能
- 集成 SoulChat2.0 模型" || echo "没有需要提交的更改"

echo ""

# 配置远程
echo "配置远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Volcano-Heidi/NaoAI.git
echo "✓ 远程仓库已配置"
echo ""

# 确保在 main 分支
git branch -M main 2>/dev/null || true

# 强制推送
echo "=========================================="
echo "强制推送到 GitHub（覆盖所有内容）"
echo "=========================================="
echo ""
echo "⚠️  这将完全覆盖远程仓库！"
echo ""
read -p "确认推送？(yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo ""
    echo "正在推送..."
    if git push -f origin main 2>&1; then
        echo ""
        echo "=========================================="
        echo "✅ 推送成功！"
        echo "=========================================="
        echo ""
        echo "请访问以下链接查看："
        echo "https://github.com/Volcano-Heidi/NaoAI"
        echo ""
        echo "如果页面没有更新，请："
        echo "1. 强制刷新浏览器（Cmd+Shift+R）"
        echo "2. 等待几分钟"
        echo ""
    else
        echo ""
        echo "推送失败，请检查错误信息"
        echo ""
    fi
else
    echo "已取消"
fi

