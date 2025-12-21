#!/bin/bash

# 修复 GitHub 推送问题

echo "=========================================="
echo "修复 GitHub 推送问题"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 1. 确保 git 仓库已初始化
if [ ! -d .git ]; then
    echo "初始化 Git 仓库..."
    git init
    echo "✓ Git 仓库已初始化"
else
    echo "✓ Git 仓库已存在"
fi
echo ""

# 2. 检查当前分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [ -z "$CURRENT_BRANCH" ]; then
    # 检查是否有任何分支
    BRANCHES=$(git branch 2>/dev/null)
    if [ -z "$BRANCHES" ]; then
        echo "创建 main 分支..."
        # 先创建一个初始提交才能创建分支
        git checkout -b main 2>/dev/null || true
    else
        # 使用现有分支
        EXISTING_BRANCH=$(git branch | head -1 | sed 's/^[* ] //')
        echo "使用现有分支: $EXISTING_BRANCH"
        git checkout "$EXISTING_BRANCH" 2>/dev/null || true
    fi
else
    echo "当前分支: $CURRENT_BRANCH"
    # 如果当前分支不是 main，重命名为 main
    if [ "$CURRENT_BRANCH" != "main" ]; then
        echo "重命名分支为 main..."
        git branch -M main
    fi
fi
echo ""

# 3. 添加所有文件
echo "添加文件到暂存区..."
git add .
echo "✓ 文件已添加"
echo ""

# 4. 检查是否有更改需要提交
CHANGES=$(git status --porcelain)
if [ -n "$CHANGES" ] || [ -z "$(git log --oneline -1 2>/dev/null)" ]; then
    echo "提交更改..."
    git commit -m "更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件

- 添加三种性格的心理咨询师（幽默、温柔、专业）
- 集成 SoulChat2.0 模型
- 集成 NAO 动作系统
- 更新 README 和文档
- 清理旧文件和无关代码（删除30+个文件）
- 适配 macOS 环境
- 添加 .gitignore 文件"
    echo "✓ 更改已提交"
else
    echo "✓ 没有需要提交的更改"
fi
echo ""

# 5. 配置远程仓库
echo "配置远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Volcano-Heidi/NaoAI.git
echo "✓ 远程仓库已配置"
echo ""

# 6. 确保在 main 分支
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
if [ "$CURRENT_BRANCH" != "main" ]; then
    git branch -M main
fi

# 7. 显示当前状态
echo "当前 Git 状态:"
echo "  分支: $(git branch --show-current 2>/dev/null || echo 'main')"
echo "  提交: $(git log --oneline -1 2>/dev/null || echo '无提交')"
echo "  远程: $(git remote get-url origin 2>/dev/null || echo '未配置')"
echo ""

# 8. 推送到 GitHub
echo "=========================================="
echo "推送到 GitHub..."
echo "=========================================="
echo ""

# 获取当前分支名
BRANCH_NAME=$(git branch --show-current 2>/dev/null || echo "main")

echo "正在推送到: origin $BRANCH_NAME"
echo ""

if git push -u origin "$BRANCH_NAME" 2>&1; then
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
    echo "如果推送失败，请尝试："
    echo ""
    echo "1. 使用 Personal Access Token:"
    echo "   git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git"
    echo "   git push -u origin $BRANCH_NAME"
    echo ""
    echo "2. 或手动推送:"
    echo "   git push -u origin $BRANCH_NAME"
    echo ""
    echo "3. 如果远程仓库是空的，可能需要先拉取:"
    echo "   git pull origin $BRANCH_NAME --allow-unrelated-histories"
    echo "   git push -u origin $BRANCH_NAME"
    echo ""
fi

