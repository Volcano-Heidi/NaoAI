#!/bin/bash

# 解决 GitHub 同步问题

echo "=========================================="
echo "解决分支分歧问题"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 1. 配置 pull 策略为 merge
echo "1. 配置 pull 策略..."
git config pull.rebase false
echo "✓ 已设置 pull 策略为 merge"
echo ""

# 2. 拉取并合并远程更改
echo "2. 拉取并合并远程更改..."
if git pull origin main --allow-unrelated-histories --no-edit 2>&1; then
    echo "✓ 合并成功"
else
    echo ""
    echo "⚠️  可能有冲突需要解决"
    echo ""
    echo "如果有冲突，请："
    echo "1. 查看冲突文件: git status"
    echo "2. 解决冲突后: git add ."
    echo "3. 完成合并: git commit -m '解决冲突'"
    echo "4. 推送: git push origin main"
    exit 1
fi
echo ""

# 3. 检查状态
echo "3. 检查当前状态..."
git status --short
echo ""

# 4. 推送到 GitHub
echo "4. 推送到 GitHub..."
if git push -u origin main 2>&1; then
    echo ""
    echo "=========================================="
    echo "✅ 成功推送到 GitHub！"
    echo "=========================================="
    echo "仓库地址: https://github.com/Volcano-Heidi/NaoAI"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo ""
    echo "如果仍然失败，可以尝试强制推送（会覆盖远程）："
    echo "  git push -f origin main"
    echo ""
    echo "⚠️  注意：强制推送会覆盖远程的所有更改！"
    echo ""
fi

