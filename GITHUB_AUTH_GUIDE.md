# GitHub 认证问题解决方案

## 问题

错误信息：`Authentication failed for 'https://github.com/Volcano-Heidi/NaoAI.git/'`

**原因**：GitHub 从 2021 年 8 月起不再支持密码认证，必须使用 Personal Access Token 或 SSH 密钥。

## 解决方案

### 方法 1：使用 Personal Access Token（推荐）

#### 步骤 1：创建 Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 填写信息：
   - **Note**: 例如 "NaoAI Project"
   - **Expiration**: 选择过期时间（建议 90 天或 No expiration）
   - **Select scopes**: 勾选 `repo` 权限（这会自动勾选所有 repo 相关权限）
4. 点击 **"Generate token"**
5. **重要**：立即复制生成的 token（只显示一次！）

#### 步骤 2：使用 Token 配置 Git

```bash
cd /Users/heidi/Downloads/NaoAI-main

# 使用 token 配置远程仓库 URL
git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git

# 替换 YOUR_TOKEN 为您的实际 token
# 例如：git remote set-url origin https://ghp_xxxxxxxxxxxx@github.com/Volcano-Heidi/NaoAI.git
```

#### 步骤 3：推送代码

```bash
# 确保文件已添加和提交
git add .
git commit -m "更新项目"

# 推送
git push -u origin main
```

推送时：
- **用户名**：输入您的 GitHub 用户名（Volcano-Heidi）
- **密码**：输入您的 Personal Access Token（不是 GitHub 密码）

### 方法 2：使用 SSH 密钥（更安全，推荐长期使用）

#### 步骤 1：检查是否已有 SSH 密钥

```bash
ls -al ~/.ssh
```

如果看到 `id_rsa.pub` 或 `id_ed25519.pub`，说明已有 SSH 密钥。

#### 步骤 2：如果没有 SSH 密钥，创建一个

```bash
# 生成新的 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 按 Enter 使用默认路径
# 设置密码（可选，但推荐）
```

#### 步骤 3：添加 SSH 密钥到 GitHub

```bash
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 或
cat ~/.ssh/id_rsa.pub
```

然后：
1. 访问：https://github.com/settings/keys
2. 点击 **"New SSH key"**
3. **Title**: 例如 "MacBook Air"
4. **Key**: 粘贴刚才复制的公钥内容
5. 点击 **"Add SSH key"**

#### 步骤 4：使用 SSH URL

```bash
cd /Users/heidi/Downloads/NaoAI-main

# 更改远程仓库 URL 为 SSH
git remote set-url origin git@github.com:Volcano-Heidi/NaoAI.git

# 推送
git push -u origin main
```

### 方法 3：使用 GitHub CLI（如果已安装）

```bash
# 安装 GitHub CLI（如果还没有）
# macOS: brew install gh

# 登录
gh auth login

# 选择 GitHub.com
# 选择 HTTPS 或 SSH
# 按照提示完成认证

# 然后推送
git push -u origin main
```

### 方法 4：使用 Git Credential Helper（临时方案）

```bash
# 配置凭据助手
git config --global credential.helper osxkeychain  # macOS
# 或
git config --global credential.helper store      # Linux

# 设置远程仓库（不包含 token）
git remote set-url origin https://github.com/Volcano-Heidi/NaoAI.git

# 推送时会提示输入凭据
git push -u origin main
# 用户名：Volcano-Heidi
# 密码：输入 Personal Access Token
```

## 快速修复脚本

已创建 `setup_github_auth.sh` 脚本，运行：

```bash
./setup_github_auth.sh
```

## 验证配置

```bash
# 检查远程仓库 URL
git remote -v

# 应该显示：
# origin  https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git (fetch)
# origin  https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git (push)
# 或
# origin  git@github.com:Volcano-Heidi/NaoAI.git (fetch)
# origin  git@github.com:Volcano-Heidi/NaoAI.git (push)
```

## 安全提示

⚠️ **重要安全提醒**：

1. **不要将 token 提交到代码仓库**
2. **不要分享您的 token**
3. **定期轮换 token**（建议每 90 天）
4. **如果 token 泄露，立即撤销**：https://github.com/settings/tokens
5. **使用 SSH 密钥更安全**（推荐长期使用）

## 完整推送流程

```bash
cd /Users/heidi/Downloads/NaoAI-main

# 1. 添加文件
git add .

# 2. 提交
git commit -m "更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件"

# 3. 配置认证（选择一种方法）
# 方法 A: 使用 token
git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git

# 方法 B: 使用 SSH
# git remote set-url origin git@github.com:Volcano-Heidi/NaoAI.git

# 4. 推送
git push -u origin main
```

## 故障排除

### 问题：仍然提示认证失败

**解决方案**：
1. 确认 token 有 `repo` 权限
2. 确认 token 未过期
3. 检查远程 URL 是否正确：`git remote -v`
4. 尝试重新生成 token

### 问题：SSH 连接失败

**解决方案**：
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 如果失败，检查 SSH 密钥是否已添加到 GitHub
# 或重新生成 SSH 密钥
```

### 问题：忘记 token

**解决方案**：
1. 访问 https://github.com/settings/tokens
2. 撤销旧 token
3. 创建新 token
4. 更新远程 URL

