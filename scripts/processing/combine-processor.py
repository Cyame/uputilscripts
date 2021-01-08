# 视频合并脚本
#
# 将Bilibili官方分段录像(FLV)合并为一个MP4文件

import logging
import os
import shutil
import sys
from time import perf_counter

from ffmpy import FFmpeg
from natsort import natsorted

logger = logging.getLogger(__name__)


def video_convert(in_path, out_path):
    FFmpeg(inputs={in_path: None}, outputs={
           out_path: '-loglevel quiet -c copy -bsf:v h264_mp4toannexb -f mpegts'}).run()


def del_path(path):
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def flv_dir_to_mp4(in_path_dir, out_path_file):
    """
    将flv文件转换为mp4
    法一:(只显示第一段，有问题)
    ffmpeg -safe 0 -f concat -i filelist.txt -c copy out.mp4
    法二:
    ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
    ffmpeg -i "concat:1.ts|2.ts|...n.ts" -c copy -absf aac_adtstoasc out.mp4
    """

    tsfile_dir = os.path.join(in_path_dir, 'tsfile')
    del_path(out_path_file)
    del_path(tsfile_dir)

    os.mkdir(tsfile_dir)

    out_files = []

    # 生成中间文件ts
    for root, dirs, files in os.walk(in_path_dir):
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1] == '.flv':
                file_path = os.path.join(root, file)
                video_convert(os.path.join(root, file), os.path.join(
                    tsfile_dir, os.path.splitext(file)[0] + '.ts'))

    # 获取列表参数
    for root, dirs, files in os.walk(tsfile_dir):
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1] == '.ts':
                file_path = os.path.join(root, file)
                out_files.append(file_path)

    ff = FFmpeg(inputs={'concat:' + '|'.join(out_files): None},
                outputs={out_path_file: '-loglevel quiet -c copy -absf aac_adtstoasc -movflags faststart'})
    ff.run()


if __name__ == '__main__':
    start = perf_counter()

    print('sys argv', sys.argv)
    if len(sys.argv) == 3:
        flv_dir_to_mp4(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        flv_dir_to_mp4(sys.argv[1], os.path.join(sys.argv[1], 'out.mp4'))
    else:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        flv_dir_to_mp4(root_dir, os.path.join(root_dir, 'out.mp4'))

    end = perf_counter()
    print('Running time: %s Seconds' % (end-start))