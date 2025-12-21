#!/bin/bash

# 诊断并修复 GitHub 推送问题

echo "=========================================="
echo "GitHub 仓库诊断和修复"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 1. 检查本地 README
echo "1. 检查本地 README.md..."
if [ -f README.md ]; then
    echo "✓ README.md 存在"
    echo "第一行内容:"
    head -1 README.md
else
    echo "✗ README.md 不存在"
fi
echo ""

# 2. 检查 Git 状态
echo "2. 检查 Git 状态..."
git status
echo ""

# 3. 检查提交历史
echo "3. 检查最近的提交..."
git log --oneline -5
echo ""

# 4. 检查远程仓库
echo "4. 检查远程仓库配置..."
git remote -v
echo ""

# 5. 检查分支
echo "5. 检查分支..."
git branch -a
echo ""

# 6. 确保所有文件已添加
echo "6. 添加所有文件到暂存区..."
git add .
echo "✓ 文件已添加"
echo ""

# 7. 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "7. 提交更改..."
    git commit -m "更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件

- 添加三种性格的心理咨询师（幽默、温柔、专业）
- 集成 SoulChat2.0 模型
- 集成 NAO 动作系统
- 更新 README 和文档
- 清理旧文件和无关代码（删除30+个文件）
- 适配 macOS 环境"
    echo "✓ 更改已提交"
else
    echo "7. 没有需要提交的更改"
fi
echo ""

# 8. 显示将要推送的文件
echo "8. 将要推送的文件列表："
git ls-files | head -30
echo "..."
echo "总计: $(git ls-files | wc -l | tr -d ' ') 个文件"
echo ""

# 9. 强制推送
echo "9. 强制推送到 GitHub..."
echo "⚠️  这将覆盖远程仓库的所有内容"
echo ""
read -p "确认强制推送？(yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo ""
    echo "正在推送..."
    if git push -f origin main 2>&1; then
        echo ""
        echo "=========================================="
        echo "✅ 推送成功！"
        echo "=========================================="
        echo ""
        echo "请访问以下链接查看更新："
        echo "https://github.com/Volcano-Heidi/NaoAI"
        echo ""
        echo "如果页面没有更新，请："
        echo "1. 强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）"
        echo "2. 清除浏览器缓存"
        echo "3. 等待几分钟后再次查看"
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
        echo "请检查错误信息并重试"
        echo ""
    fi
else
    echo "已取消推送"
fi

