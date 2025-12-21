#!/bin/bash

# 同步本地和远程仓库

echo "=========================================="
echo "同步 GitHub 仓库"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 获取远程更改
echo "1. 获取远程更改..."
git fetch origin
echo "✓ 已获取远程更改"
echo ""

# 检查是否有冲突
echo "2. 检查本地和远程的差异..."
LOCAL_COMMITS=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
REMOTE_COMMITS=$(git log HEAD..origin/main --oneline 2>/dev/null | wc -l | tr -d ' ')

echo "  本地新提交: $LOCAL_COMMITS 个"
echo "  远程新提交: $REMOTE_COMMITS 个"
echo ""

if [ "$REMOTE_COMMITS" -gt 0 ]; then
    echo "3. 远程仓库有新的提交，需要先合并..."
    echo ""
    echo "选择合并方式："
    echo "  a) 合并远程更改（推荐）- 保留两边的更改"
    echo "  b) 使用 rebase - 将本地提交放在远程提交之上"
    echo "  c) 强制推送 - 用本地覆盖远程（危险，会丢失远程更改）"
    echo ""
    read -p "请选择 (a/b/c，默认 a): " choice
    choice=${choice:-a}
    
    case $choice in
        a)
            echo ""
            echo "正在合并远程更改..."
            if git pull origin main --allow-unrelated-histories --no-edit 2>&1; then
                echo "✓ 合并成功"
            else
                echo ""
                echo "⚠️  有冲突需要解决"
                echo "请手动解决冲突后，运行："
                echo "  git add ."
                echo "  git commit -m '解决冲突'"
                echo "  git push origin main"
                exit 1
            fi
            ;;
        b)
            echo ""
            echo "正在 rebase..."
            if git pull --rebase origin main 2>&1; then
                echo "✓ Rebase 成功"
            else
                echo ""
                echo "⚠️  有冲突需要解决"
                echo "解决冲突后运行："
                echo "  git add ."
                echo "  git rebase --continue"
                echo "  git push origin main"
                exit 1
            fi
            ;;
        c)
            echo ""
            echo "⚠️  警告：强制推送会覆盖远程更改！"
            read -p "确定要继续吗？(yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                echo "正在强制推送..."
                git push -f origin main
                echo "✓ 强制推送完成"
            else
                echo "已取消"
                exit 0
            fi
            ;;
    esac
else
    echo "3. 远程没有新提交，可以直接推送"
fi

echo ""
echo "4. 推送到 GitHub..."
if git push -u origin main 2>&1; then
    echo ""
    echo "=========================================="
    echo "✅ 成功同步到 GitHub！"
    echo "=========================================="
    echo "仓库地址: https://github.com/Volcano-Heidi/NaoAI"
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
    echo "查看详细指南: cat GITHUB_AUTH_GUIDE.md"
    echo ""
fi

