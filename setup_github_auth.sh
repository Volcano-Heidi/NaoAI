#!/bin/bash

# GitHub 认证设置脚本

echo "=========================================="
echo "GitHub 认证设置"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

echo "GitHub 不再支持密码认证，需要使用 Personal Access Token 或 SSH 密钥。"
echo ""

# 方法 1: 使用 Personal Access Token
echo "方法 1: 使用 Personal Access Token（推荐）"
echo "----------------------------------------"
echo ""
echo "步骤："
echo "1. 访问 https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 选择 'repo' 权限"
echo "4. 复制生成的 token"
echo ""
read -p "请输入您的 Personal Access Token: " TOKEN

if [ -n "$TOKEN" ]; then
    echo ""
    echo "配置远程仓库 URL（包含 token）..."
    git remote set-url origin https://${TOKEN}@github.com/Volcano-Heidi/NaoAI.git
    echo "✓ 已配置 token"
    echo ""
    echo "现在可以推送了："
    echo "  git push -u origin main"
    echo ""
else
    echo "未输入 token，跳过配置"
fi

echo ""
echo "----------------------------------------"
echo "方法 2: 使用 SSH（如果已配置 SSH 密钥）"
echo "----------------------------------------"
echo ""
echo "如果已配置 SSH 密钥，可以使用："
echo "  git remote set-url origin git@github.com:Volcano-Heidi/NaoAI.git"
echo "  git push -u origin main"
echo ""

echo "----------------------------------------"
echo "方法 3: 使用 GitHub CLI（如果已安装）"
echo "----------------------------------------"
echo ""
echo "如果已安装 gh CLI："
echo "  gh auth login"
echo "  git push -u origin main"
echo ""

