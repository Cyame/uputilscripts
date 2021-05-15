# 查找/修正时轴错误

import os
import sys

script_description = '''
时轴规范检测脚本 v0.1
BY 茶目

用于帮助批量修改时轴上的错误，如闪轴/长轴/叠轴等问题。
简化字幕规范化流程。
'''

script_paralist = '''
kanji-manager: [-f|-c|-s] <your-rule-groups> <your-ass-path> [<your-target-output-path>]

-- options --
-f: force mode - Overwrite the origin ass with modification
-c: check mode - Do no modification, just checkout the potential problems
-s: standard mode(Recommended/Default) - Generate a modified copy in your current path (You can name it by using the third parameter, or otherwise the file name will be "km-mod-output[time].ass" acquiescently)
'''

def get_runtime_path():
    return os.getcwd()

def get_scripts_path():
    return os.path.abspath(__file__)