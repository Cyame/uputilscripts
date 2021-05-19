

<p align="center"><a href="https://space.bilibili.com/2265912"><img src="https://i.loli.net/2021/05/19/97rzoRaixOjsB5E.png" width="200" height="200" alt="UpUtilScripts"/></a></p>


<div align=“center”>

# uputilscripts | UP主实用脚本合集

A collection of some useful scripts for video uploaders, basically in Python

一些UP主和搬运主可能会常用的PY脚本 大部分可用于视频投稿相关的批处理 不定时更新

</div>

<p align="center">

<a href="https://www.python.org/"><img src="https://img.shields.io/static/v1?label=Python&message=3.7&color=blue&style=flat-square" alt="Python 3.7"></a>
<a href="https://github.com/Cyame/uputilscripts/blob/v3/LICENSE"><img src="https://img.shields.io/static/v1?label=LICENSE&message=MIT&color=red&style=flat-square" alt="MIT License"></a>
<a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/static/v1?label=commitzen&message=friendly&color=brightgreen&style=flat-square" alt="CommitZen Friendly"></a>

</p>
## Get Started | 开始

### 安装

1. **几乎所有脚本都需要使用到FFMPEG，请确保其正确安装并配置系统环境变量。**
   *推荐使用Build版 (对于Windows系统而言应有**ffmpeg.exe**存在于系统环境变量中)*

2. 安装NodeJS环境（推荐安装LTS版本）

3. (Windows)运行
    ```
    $ pip install -r requirements.txt
    ```
    
    (Linux/Unix)运行
    ```
    $ pip3 install -r requirements.txt
    ```

    以在你的默认Python运行环境中安装依赖包。

## Usage | 使用

本脚本集合均基于配置文件+Simply运行的模式，对于不同类处理不冲突（视频/时轴）。具体操作方法参见`script/*`各脚本文件夹内README说明。

```
$ python <script-name> <workload-folder/target-file>
```

## Dev Plan | 开发计划

#### 压制

1. 正常挂载VSF的ass压制
2. 含字幕的大小限制压制
3. 含字幕的码率限制压制
4. vfr2cfr转换
5. 源轨音频提取

#### 特效/滤镜

1. 挂载VSMOD压制
2. 片头片尾压制

#### 整合（暂缓）

1. 工具整合

#### 投稿

1. 封面模板
2. 投稿简介生成
3. 录制脚本
4. 防撞车脚本