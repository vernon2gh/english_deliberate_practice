# 介绍

这是是一个用于学习英语的 Python 脚本。它提供了将句子拆分成块，过滤块，播放音频，练习句子，
以及使用艾宾浩斯遗忘曲线练习单词的功能。

- 刻意练习: 重复来交互式地练习句子或单词。
- 句子处理: 从文件中读取句子，将其拆分成块，过滤块，播放音频，同时练习句子。
- 单词处理: 从文件中读取单词，过滤，并使用艾宾浩斯遗忘曲线进行练习单词。
- 音频缓存: 预生成音频缓存来提高性能。

# 依赖

在运行脚本之前，请确保安装所需的依赖项：

```bash
(.venv) pip install edge_tts mpv termcolor
```

# 示例

## 练习句子

```bash
$ python english_deliberate_practice.py.py --hear --split
```

## 练习单词

```bash
$ python english_deliberate_practice.py.py --hear --split --word
```

## 支持参数

该脚本支持通过各种命令行参数控制不同行为：

- `--hear` : 听写句子/块/单词
- `--split`: 拆分句子为多个不同块 或者 生成艾宾浩斯规则的单词
- `--cache`: 预生成 mp3 音频缓存
- `--word` : 只练习单词
- `--ffile`: 过滤文件的路径（默认：`./filter.txt`）。
- `--sfile`: 句子文件的路径（默认：`./sentences.txt`）。
- `--wfile`: 单词文件的路径（默认：`./word.txt`）。
