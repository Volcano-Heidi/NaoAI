# -*- coding: utf-8 -*-
# 自动查找NAOqi SDK

import os
import sys

def find_naoqi_sdk():
    """自动查找NAOqi SDK"""
    found_paths = []
    
    # 1. 检查环境变量
    sdk_path = os.environ.get('PYNAOQI_PATH')
    if sdk_path and os.path.exists(sdk_path):
        site_packages = os.path.join(sdk_path, 'lib', 'python2.7', 'site-packages')
        if os.path.exists(site_packages):
            found_paths.append(('环境变量PYNAOQI_PATH', site_packages))
    
    # 2. 检查常见路径（根据系统类型）
    import platform
    is_macos = platform.system() == 'Darwin'
    is_linux = platform.system() == 'Linux'
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(project_dir)
    
    if is_linux:
        common_paths = [
            os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327'),
            os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-linux64'),
            '/opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64',
            '/usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-linux64',
            '/home/nao/pynaoqi-python2.7-2.8.6.23-linux64',
            '/root/pynaoqi-python2.7-2.8.6.23-linux64',
            '/opt/aldebaran/pynaoqi-python2.7-2.8.6.23-linux64',
        ]
    elif is_macos:
        common_paths = [
            os.path.join(parent_dir, 'pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4'),
            os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231'),
            os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-mac64'),
            '/opt/naoqi/pynaoqi-python2.7-2.8.6.23-mac64',
            '/usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-mac64',
            os.path.expanduser('~/pynaoqi-python2.7-2.8.6.23-mac64'),
            os.path.expanduser('~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4'),
        ]
    else:
        common_paths = []
    
    for path in common_paths:
        if os.path.exists(path):
            site_packages = os.path.join(path, 'lib', 'python2.7', 'site-packages')
            if os.path.exists(site_packages):
                found_paths.append(('常见路径', site_packages))
    
    # 3. 搜索整个系统（根据系统类型限制搜索范围）
    print("搜索NAOqi SDK文件...")
    import subprocess
    try:
        if is_linux:
            search_paths = ['/root', '/home', '/opt', '/usr/local']
        elif is_macos:
            search_paths = [os.path.expanduser('~'), '/opt', '/usr/local']
        else:
            search_paths = []
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    result = subprocess.check_output(
                        ['find', search_path, '-name', 'ALProxy.py', '-type', 'f', '2>/dev/null'],
                        stderr=subprocess.STDOUT,
                        timeout=10
                    )
                    for line in result.decode('utf-8', errors='ignore').split('\n'):
                        if line and 'ALProxy.py' in line:
                            sdk_dir = os.path.dirname(line)
                            if os.path.exists(sdk_dir):
                                found_paths.append(('自动搜索', sdk_dir))
                                break
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                    continue
    except:
        pass
    
    # 4. 检查Python site-packages
    for path in sys.path:
        if 'site-packages' in path:
            naoqi_path = os.path.join(path, 'naoqi')
            if os.path.exists(naoqi_path):
                found_paths.append(('Python site-packages', path))
    
    return found_paths

if __name__ == '__main__':
    print("=" * 50)
    print("NAOqi SDK 自动查找工具")
    print("=" * 50)
    print("")
    
    paths = find_naoqi_sdk()
    
    if paths:
        print("找到以下NAOqi SDK路径：")
        for i, (source, path) in enumerate(paths, 1):
            print("%d. %s: %s" % (i, source, path))
        
        # 测试第一个路径
        test_path = paths[0][1]
        sys.path.insert(0, test_path)
        
        print("")
        print("测试导入...")
        try:
            from naoqi import ALProxy
            print("✓ 成功导入naoqi模块！")
            print("")
            print("推荐使用路径: %s" % test_path)
            print("")
            print("设置方法:")
            if 'site-packages' in test_path:
                # 提取SDK根目录
                sdk_root = test_path.replace('/lib/python2.7/site-packages', '')
                print("  export PYNAOQI_PATH=%s" % sdk_root)
            else:
                print("  export PYNAOQI_PATH=%s" % test_path)
        except ImportError as e:
            print("✗ 导入失败: %s" % str(e))
    else:
        print("✗ 未找到NAOqi SDK")
        print("")
        print("请手动设置PYNAOQI_PATH环境变量")
        print("或下载NAOqi SDK并解压")

