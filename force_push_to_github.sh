#!/bin/bash

# 强制推送，用本地内容覆盖远程

echo "=========================================="
echo "强制推送到 GitHub（覆盖远程内容）"
echo "=========================================="
echo ""
echo "⚠️  警告：此操作会用本地内容完全覆盖远程仓库！"
echo "⚠️  远程的所有更改将被永久删除！"
echo ""
read -p "确定要继续吗？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "已取消操作"
    exit 0
fi

cd "$(dirname "$0")"

# 确保所有本地更改已提交
echo ""
echo "检查本地更改..."
if [ -n "$(git status --porcelain)" ]; then
    echo "发现未提交的更改，正在添加..."
    git add .
    git commit -m "更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件" || true
fi

echo ""
echo "当前本地文件列表："
git ls-files | head -20
echo "..."

echo ""
echo "正在强制推送到 GitHub..."
if git push -f origin main 2>&1; then
    echo ""
    echo "=========================================="
    echo "✅ 成功！本地内容已覆盖远程仓库"
    echo "=========================================="
    echo "仓库地址: https://github.com/Volcano-Heidi/NaoAI"
    echo ""
    echo "远程仓库现在包含以下文件："
    git ls-files | wc -l
    echo "个文件"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo ""
    echo "可能的原因："
    echo "1. 认证失败 - 请检查 token 或 SSH 配置"
    echo "2. 网络问题 - 请检查网络连接"
    echo "3. 权限问题 - 请确认有推送权限"
    echo ""
fi

