import os
import sys

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目的根目录
root_dir = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path
sys.path.append(root_dir)

from service.testmodule import ttt

t = ttt()
