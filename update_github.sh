#!/bin/bash

# 更新 GitHub 仓库脚本

echo "=========================================="
echo "更新 GitHub 仓库"
echo "=========================================="
echo ""

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查是否在 git 仓库中
if [ ! -d .git ]; then
    echo "初始化 Git 仓库..."
    git init
    echo "✓ Git 仓库已初始化"
    echo ""
fi

# 检查远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE_URL" ]; then
    echo "配置远程仓库..."
    git remote add origin https://github.com/Volcano-Heidi/NaoAI.git 2>/dev/null || \
    git remote set-url origin https://github.com/Volcano-Heidi/NaoAI.git
    echo "✓ 远程仓库已配置: https://github.com/Volcano-Heidi/NaoAI.git"
    echo ""
fi

# 添加所有更改
echo "添加文件到暂存区..."
git add .
echo "✓ 文件已添加到暂存区"
echo ""

# 显示更改状态
echo "当前更改状态:"
git status --short
echo ""

# 提交更改
COMMIT_MSG="更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件

- 添加三种性格的心理咨询师（幽默、温柔、专业）
- 集成 SoulChat2.0 模型
- 集成 NAO 动作系统
- 更新 README 和文档
- 清理旧文件和无关代码
- 适配 macOS 环境"

echo "提交更改..."
git commit -m "$COMMIT_MSG"
echo ""

# 检查分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
if [ -z "$CURRENT_BRANCH" ]; then
    git checkout -b main 2>/dev/null || git branch -M main
    CURRENT_BRANCH="main"
fi

echo "当前分支: $CURRENT_BRANCH"
echo ""

# 推送到 GitHub
echo "推送到 GitHub..."
echo "提示: 如果需要认证，请输入您的 GitHub 用户名和 Personal Access Token"
echo ""

# 尝试推送
if git push -u origin "$CURRENT_BRANCH" 2>&1; then
    echo ""
    echo "=========================================="
    echo "✅ 成功推送到 GitHub！"
    echo "=========================================="
    echo "仓库地址: https://github.com/Volcano-Heidi/NaoAI"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠️  推送可能需要认证"
    echo "=========================================="
    echo ""
    echo "如果推送失败，请尝试以下方法："
    echo ""
    echo "1. 使用 Personal Access Token:"
    echo "   git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git"
    echo "   git push -u origin $CURRENT_BRANCH"
    echo ""
    echo "2. 或使用 SSH:"
    echo "   git remote set-url origin git@github.com:Volcano-Heidi/NaoAI.git"
    echo "   git push -u origin $CURRENT_BRANCH"
    echo ""
    echo "3. 或手动推送:"
    echo "   git push -u origin $CURRENT_BRANCH"
    echo ""
fi

