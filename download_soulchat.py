#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SoulChat2.0 模型下载脚本
从 ModelScope 下载 SoulChat2.0-Llama-3.1-8B 模型到本地
"""

import os
import sys

def download_soulchat_model():
    """使用 ModelScope 下载 SoulChat2.0 模型"""
    try:
        from modelscope import snapshot_download
    except ImportError:
        print("错误: 未安装 modelscope 库")
        print("请先安装: pip install modelscope")
        print("或者: pip3 install modelscope")
        sys.exit(1)
    
    # 模型 ID
    model_id = 'YIRONGCHEN/SoulChat2.0-Llama-3.1-8B'
    
    # 默认下载路径（可以修改）
    default_download_dir = os.path.expanduser('~/models')
    
    # 检查是否指定了下载路径
    if len(sys.argv) > 1:
        download_dir = sys.argv[1]
    else:
        download_dir = default_download_dir
    
    # 创建下载目录
    os.makedirs(download_dir, exist_ok=True)
    
    print("=" * 60)
    print("SoulChat2.0 模型下载")
    print("=" * 60)
    print(f"模型: {model_id}")
    print(f"下载路径: {download_dir}")
    print("=" * 60)
    print("\n开始下载，这可能需要一些时间...")
    print("模型大小约为 16GB，请确保有足够的磁盘空间和网络带宽\n")
    
    try:
        # 下载模型
        model_dir = snapshot_download(
            model_id,
            cache_dir=download_dir,
            local_files_only=False
        )
        
        print("\n" + "=" * 60)
        print("✓ 下载完成！")
        print("=" * 60)
        print(f"模型路径: {model_dir}")
        print("\n使用说明:")
        print(f"1. 设置环境变量: export MODEL_NAME_OR_PATH={model_dir}")
        print("2. 启动 SoulChat 服务: ./start_soulchat.sh")
        print("=" * 60)
        
        return model_dir
        
    except Exception as e:
        print(f"\n错误: 下载失败 - {str(e)}")
        print("\n可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 确保有足够的磁盘空间")
        print("3. 尝试使用其他下载方法（见 SOULCHAT_INTEGRATION.md）")
        sys.exit(1)

if __name__ == '__main__':
    download_soulchat_model()

