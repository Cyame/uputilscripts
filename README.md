# uputilscripts | UP主实用脚本合集

A collection of some useful scripts for video uploaders, basically in Python.

一些UP主和搬运主可能会常用的PY脚本，大部分将用于视频压制或批处理。不定时更新。

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

