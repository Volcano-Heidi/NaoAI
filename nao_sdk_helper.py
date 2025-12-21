# -*- coding: utf-8 -*-
# NAOqi SDK路径辅助函数

import os
import sys
import platform

def setup_naoqi_sdk():
    """设置NAOqi SDK路径"""
    is_macos = platform.system() == 'Darwin'
    is_linux = platform.system() == 'Linux'
    
    # 1. 从环境变量获取
    sdk_path = os.environ.get('PYNAOQI_PATH')
    
    # 2. 如果未设置，尝试常见路径（根据系统类型）
    if not sdk_path or not os.path.exists(sdk_path):
        if is_linux:
            # 获取项目目录
            project_dir = os.path.dirname(os.path.abspath(__file__))
            common_paths = [
                # 项目目录中的SDK（优先）
                os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327'),
                os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-linux64'),
                # 系统常见路径
                '/opt/naoqi/pynaoqi-python2.7-2.8.6.23-linux64',
                '/usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-linux64',
                '/home/nao/pynaoqi-python2.7-2.8.6.23-linux64',
                '/root/pynaoqi-python2.7-2.8.6.23-linux64',
                '/opt/aldebaran/pynaoqi-python2.7-2.8.6.23-linux64',
            ]
        elif is_macos:
            # 获取项目目录
            project_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取项目父目录（Downloads目录）
            parent_dir = os.path.dirname(project_dir)
            common_paths = [
                # 项目父目录中的 pynaoqi（用户添加的）
                os.path.join(parent_dir, 'pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4'),
                # 项目目录中的SDK（如果存在）
                os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231'),
                os.path.join(project_dir, 'pynaoqi-python2.7-2.8.6.23-mac64'),
                # 系统常见路径
                '/opt/naoqi/pynaoqi-python2.7-2.8.6.23-mac64',
                '/usr/local/naoqi/pynaoqi-python2.7-2.8.6.23-mac64',
                os.path.expanduser('~/pynaoqi-python2.7-2.8.6.23-mac64'),
                os.path.expanduser('~/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231 4'),
            ]
        else:
            common_paths = []
        
        for path in common_paths:
            if os.path.exists(path):
                sdk_path = path
                break
    
    # 3. 如果找到标准SDK路径
    if sdk_path and os.path.exists(sdk_path):
        site_packages = os.path.join(sdk_path, 'lib', 'python2.7', 'site-packages')
        if os.path.exists(site_packages):
            sys.path.insert(0, site_packages)
            return True
    
    # 4. 尝试使用项目目录中的qi和naoqi模块
    project_dir = os.path.dirname(os.path.abspath(__file__))
    qi_dir = os.path.join(project_dir, 'qi')
    
    if os.path.exists(qi_dir):
        # 检查_qi.so文件格式是否匹配当前系统
        qi_so_path = os.path.join(qi_dir, '_qi.so')
        if os.path.exists(qi_so_path):
            # 在macOS上，可以使用项目目录中的qi包
            if is_macos:
                sys.path.insert(0, project_dir)
                return True
            elif is_linux:
                # 在Linux上，检查是否是Linux格式
                try:
                    import subprocess
                    result = subprocess.check_output(['file', qi_so_path], stderr=subprocess.STDOUT)
                    if 'ELF' in result:
                        # Linux格式，可以使用
                        sys.path.insert(0, project_dir)
                        return True
                    elif 'Mach-O' in result:
                        # macOS格式，不能在Linux上使用
                        pass
                except:
                    pass
    
    return False

def get_nao_proxy_safe(service_name, nao_ip, nao_port):
    """安全地获取NAO代理"""
    if not setup_naoqi_sdk():
        return None
    
    try:
        # 尝试从naoqi导入
        try:
            from naoqi import ALProxy
        except ImportError:
            # 如果失败，尝试从qi.naoqi导入（适用于项目目录中的qi包）
            from qi import naoqi
            ALProxy = naoqi.ALProxy
        
        return ALProxy(service_name, nao_ip, nao_port)
    except Exception as e:
        print("Error creating %s proxy: %s" % (service_name, e))
        return None

def get_sdk_path():
    """获取SDK路径（用于兼容性）"""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if setup_naoqi_sdk():
        return project_dir
    return None

def ALProxy(service_name, nao_ip, nao_port=9559):
    """便捷函数：获取ALProxy实例"""
    if not setup_naoqi_sdk():
        raise ImportError("NAOqi SDK not found")
    
    try:
        from naoqi import ALProxy as _ALProxy
    except ImportError:
        from qi import naoqi
        _ALProxy = naoqi.ALProxy
    
    return _ALProxy(service_name, nao_ip, nao_port)
