# GitHub 仓库更新指南

## 快速更新

### 方法 1：使用更新脚本（推荐）

```bash
cd /Users/heidi/Downloads/NaoAI-main
./update_github.sh
```

### 方法 2：手动更新

#### 步骤 1：初始化 Git 仓库（如果还没有）

```bash
cd /Users/heidi/Downloads/NaoAI-main

# 检查是否已有 git 仓库
if [ ! -d .git ]; then
    git init
    git branch -M main
fi
```

#### 步骤 2：配置远程仓库

```bash
# 添加远程仓库（如果还没有）
git remote add origin https://github.com/Volcano-Heidi/NaoAI.git

# 或更新远程仓库 URL
git remote set-url origin https://github.com/Volcano-Heidi/NaoAI.git

# 验证远程仓库
git remote -v
```

#### 步骤 3：添加和提交更改

```bash
# 添加所有文件
git add .

# 查看更改状态
git status

# 提交更改
git commit -m "更新项目：添加性格选择功能，集成SoulChat2.0，清理无关文件

- 添加三种性格的心理咨询师（幽默、温柔、专业）
- 集成 SoulChat2.0 模型
- 集成 NAO 动作系统
- 更新 README 和文档
- 清理旧文件和无关代码
- 适配 macOS 环境"
```

#### 步骤 4：推送到 GitHub

```bash
# 推送到 main 分支
git push -u origin main
```

如果遇到认证问题，可以使用以下方法：

**使用 Personal Access Token：**

```bash
# 设置包含 token 的远程 URL
git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git

# 推送
git push -u origin main
```

**使用 SSH（如果已配置 SSH 密钥）：**

```bash
# 设置 SSH URL
git remote set-url origin git@github.com:Volcano-Heidi/NaoAI.git

# 推送
git push -u origin main
```

## 当前项目文件列表

项目现在包含以下文件：

### 核心程序
- `personality_counselor.py` - 主程序
- `personality_config.py` - 性格配置
- `nao_motions.py` - NAO 动作库
- `nao_sdk_helper.py` - SDK 辅助工具
- `gpt3_code.py` - LLM 调用
- `nao_tts_code.py` - TTS 模块

### 视觉功能
- `emo_detection.py` - 情感检测
- `face_detect.py` - 人脸检测
- `take_img.py` - 图像采集
- `nao_emo_tts.py` - 带情感检测的 TTS

### 工具脚本
- `check_nao_sdk.py`
- `find_naoqi_sdk.py`
- `diagnose_nao_connection.py`
- `install_dependencies.sh`
- `setup_nao_sdk.sh`
- `activate_nao_env.sh`
- `start_personality_counselor.sh`
- `update_github.sh`

### 模型下载
- `download_soulchat.py`
- `download_soulchat.sh`

### 文档
- `README.md` - 主文档
- `PERSONALITY_COUNSELOR_README.md`
- `PROMPT_INTEGRATION_SUMMARY.md`
- `SOULCHAT_SETUP.md`
- `SOULCHAT_INTEGRATION.md`
- `NAO_SDK_SETUP.md`
- `MACOS_MIGRATION.md`
- `SETUP_MACOS.md`
- `NAO_MOTIONS_README.md`
- `CLEANUP_SUMMARY.md`
- `GITHUB_PUSH_GUIDE.md`
- `GITHUB_UPDATE_GUIDE.md`（本文件）

### GitHub 相关
- `push_to_github.sh`
- `GITHUB_PUSH_GUIDE.md`

## 故障排除

### 问题 1：认证失败

**解决方案：**
1. 创建 Personal Access Token：
   - 访问：https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 选择 `repo` 权限
   - 复制生成的 token

2. 使用 token 推送：
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/Volcano-Heidi/NaoAI.git
   git push -u origin main
   ```

### 问题 2：远程仓库不存在

**解决方案：**
1. 在 GitHub 上创建仓库：https://github.com/new
   - 仓库名：NaoAI
   - 选择 Public 或 Private
   - 不要初始化 README、.gitignore 或 license

2. 然后按照上面的步骤推送

### 问题 3：推送被拒绝

**解决方案：**
```bash
# 如果远程有更改，先拉取
git pull origin main --allow-unrelated-histories

# 解决冲突后，再推送
git push -u origin main
```

### 问题 4：网络连接问题

**解决方案：**
1. 检查网络：`ping github.com`
2. 使用代理（如果有）：
   ```bash
   git config --global http.proxy http://proxy.example.com:8080
   git config --global https.proxy https://proxy.example.com:8080
   ```

## 验证推送

推送成功后，访问以下链接查看仓库：
https://github.com/Volcano-Heidi/NaoAI

## 后续更新

以后更新代码时，只需：

```bash
git add .
git commit -m "更新说明"
git push origin main
```

