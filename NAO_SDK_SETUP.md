# NAOqi SDK 配置说明

## 问题

如果遇到 "NAOqi SDK not found" 或 "无法导入NAOqi" 错误，需要配置NAOqi SDK路径。

## 解决方案

### 方法1：设置环境变量（推荐）

```bash
# 下载并解压NAOqi SDK后，设置路径
export PYNAOQI_PATH=/path/to/pynaoqi-python2.7-2.8.6.23-linux64

# 永久设置（添加到 ~/.bashrc）
echo 'export PYNAOQI_PATH=/path/to/pynaoqi-python2.7-2.8.6.23-linux64' >> ~/.bashrc
source ~/.bashrc
```

### 方法2：将SDK放到常见路径

代码会自动检测以下路径：
- `/opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64`
- `/usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-linux64`
- `/home/nao/pynaoqi-python2.7-2.8.6.23-linux64`
- `/root/pynaoqi-python2.7-2.8.6.23-linux64`
- `/opt/aldebaran/pynaoqi-python2.7-2.8.6.23-linux64`

将SDK解压到以上任一位置即可。

### 方法3：下载NAOqi SDK

1. 访问 Aldebaran 官网或 NAO 开发者资源
2. 下载对应版本的 NAOqi SDK (Linux 64位)
3. 解压到指定目录
4. 设置 PYNAOQI_PATH 环境变量

## 验证配置

运行检查脚本：

```bash
cd /root/NaoAI-Assistant-main
source /root/miniconda3/etc/profile.d/conda.sh
conda activate nao_env
python check_nao_sdk.py
```

## 注意事项

- NAOqi SDK 需要与 Python 2.7 兼容
- 确保下载的是 Linux 版本（不是 Mac 版本）
- SDK路径必须包含 `lib/python2.7/site-packages` 目录

