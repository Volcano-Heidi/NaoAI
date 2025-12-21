#!/bin/bash
# GitHub 推送脚本
# 使用前请先设置 GITHUB_TOKEN 环境变量或在推送时手动输入凭据

echo "正在配置 Git 远程仓库..."
# 如果设置了 GITHUB_TOKEN 环境变量，使用它；否则使用默认 URL
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin https://${GITHUB_TOKEN}@github.com/Volcano-Heidi/NaoAI.git
else
    git remote set-url origin https://github.com/Volcano-Heidi/NaoAI.git
fi

echo "正在推送代码到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码已成功推送到 GitHub！"
    echo "访问 https://github.com/Volcano-Heidi/NaoAI 查看仓库"
else
    echo "❌ 推送失败，请检查网络连接或 token 权限"
fi

