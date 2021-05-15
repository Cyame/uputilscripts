import logging
import os
import shutil
import sys
from time import perf_counter

from ffmpy import FFmpeg
from natsort import natsorted

logger = logging.getLogger(__name__)

def get_runtime_path():
    return os.getcwd()

def get_scripts_path():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    
    #TODO 命令预处理
    #TODO 加VSMOD OR 片头片尾



    '''

    ffmpeg -i input.mp4 -b:v 5000K -vcodec x264_qsv 

    '''


    __ffmpeg = os.path.join(get_scripts_path(),os.pardir,"utils","ffmpeg.exe")
    # print(__ffmpeg)
    __ffprobe = os.path.join(get_scripts_path(),os.pardir,"utils","ffprobe.exe")
    __ffplay = os.path.join(get_scripts_path(),os.pardir,"utils","ffplay.exe")
    # 目标视频
    __target_video = parameter_list[0]
    # 目标ASS
    __target_ass = parameter_list[1]
    # 目标比特率
    __bitrate = parameter_list[2]
    # 输出文件名
    __output = parameter_list[3]
    # 是否启用默认VRF
    __enable_vrf = parameter_list[4]
    command = f'{__ffmpeg} -i -b:v {__bitrate}{__enable_vrf} -vcodec x264_qsv -vr "ass={__target_ass}" {__output}'

    os.system(command)
    #With LOG os.popen