# GitHub 推送指南

## 当前状态
✅ Git 仓库已初始化  
✅ 所有文件已提交（50 个文件，5270 行代码）  
✅ 远程仓库已配置：`https://github.com/Volcano-Heidi/NaoAI.git`  
✅ 分支已重命名为 `main`  

## 推送方法

### 方法 1：使用提供的脚本（推荐）

```bash
cd /root/NaoAI-Assistant-main
./push_to_github.sh
```

### 方法 2：手动推送

```bash
cd /root/NaoAI-Assistant-main

# 配置远程仓库（使用环境变量中的 token）
# 首先设置环境变量：export GITHUB_TOKEN=your_token_here
git remote set-url origin https://${GITHUB_TOKEN}@github.com/Volcano-Heidi/NaoAI.git

# 推送代码
git push -u origin main
```

### 方法 3：使用 Git Credential Helper（更安全）

```bash
cd /root/NaoAI-Assistant-main

# 配置凭据助手
git config --global credential.helper store

# 设置远程仓库（不包含 token）
git remote set-url origin https://github.com/Volcano-Heidi/NaoAI.git

# 推送时会提示输入凭据
# 用户名：Volcano-Heidi
# 密码：输入你的 Personal Access Token
git push -u origin main
```

### 方法 4：如果网络有问题，使用代理

```bash
# 设置 HTTP 代理（如果有）
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 然后推送
git push -u origin main
```

### 方法 5：使用 GitHub CLI（如果已安装）

```bash
# 使用环境变量或交互式输入 token
gh auth login --with-token <<< "$GITHUB_TOKEN"
# 或者
echo "your_token_here" | gh auth login --with-token
git push -u origin main
```

## 验证推送

推送成功后，访问以下链接查看仓库：
https://github.com/Volcano-Heidi/NaoAI

## 故障排除

### 如果遇到连接超时
1. 检查网络连接：`ping github.com`
2. 检查防火墙设置
3. 尝试使用 VPN 或代理
4. 在本地网络环境较好的地方重试

### 如果遇到认证错误
1. 确认 token 权限包含 `repo` 权限
2. 检查 token 是否过期
3. 重新生成 token：https://github.com/settings/tokens

### 如果遇到权限错误
1. 确认仓库已创建：https://github.com/Volcano-Heidi/NaoAI
2. 确认 token 有推送权限
3. 检查仓库是否为私有（token 需要相应权限）

## 重要提示

⚠️ **安全提醒**：请勿将 token 提交到代码仓库。建议：
1. 删除或修改脚本中的 token
2. 使用 Git Credential Helper 存储凭据
3. 定期轮换 token

## 当前仓库信息

- **远程仓库**：https://github.com/Volcano-Heidi/NaoAI.git
- **分支**：main
- **提交数量**：1 个初始提交
- **文件数量**：50 个文件

