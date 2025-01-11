# 介绍

这是是一个用于学习英语的 Python 脚本。它提供了将句子拆分成块，过滤块，播放音频，练习句子，
使用艾宾浩斯遗忘曲线练习单词，以及听力模式。

- 刻意练习: 重复来交互式地练习句子或单词。
- 句子处理: 从文件中读取句子，将其拆分成块，过滤块，播放音频，同时练习句子。
- 单词处理: 从文件中读取单词，过滤，并使用艾宾浩斯遗忘曲线进行练习单词。
- 错误本  : 收集用户练习错误的句子/块/单词。
- 听力模式: 以指定时间间隔，重复指定次数，进行精听训练
- 音频缓存: 预生成音频缓存来提高性能。

# 依赖

在运行脚本之前，请确保安装所需的依赖项：

```bash
(.venv) pip install edge_tts mpv termcolor
```

# 示例

## 练习句子

```bash
$ python english_deliberate_practice.py.py --grey --split
```

## 听句子

```bash
$ python english_deliberate_practice.py.py --grey --split --listen
```

## 练习单词

```bash
$ python english_deliberate_practice.py.py --grey --split --word
```

## 听单词

```bash
$ python english_deliberate_practice.py.py --grey --split --word --listen
```

## 支持参数

该脚本支持通过各种命令行参数控制不同行为：

- `--split`     : 拆分句子为多个不同块 或者 生成艾宾浩斯规则的单词
- `--grey`      : 提示句子/块/单词
- `--cache`     : 预生成 mp3 音频缓存
- `--word`      : 只练习单词
- `--listen`    : 听力模式
- `--interval`  : 在听力模块播放音频的间隔时间，单位：秒，默认 1
- `--repeat`    : 在听力模块播放音频的重复次数，默认 3
- `--ffile`     : 过滤文件的路径（默认：`./filter.txt`）
- `--efile`     : 错误笔记的路径（默认：`./errornote.txt`）
- `--sfile`     : 句子文件的路径（默认：`./sentences.txt`）
- `--wfile`     : 单词文件的路径（默认：`./word.txt`）
