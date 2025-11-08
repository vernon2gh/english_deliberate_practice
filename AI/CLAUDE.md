# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

这是一个对英语句子进行拆分成分来练习的项目，需要对用户提供英语句子进行结构化拆分、渐进式拆分。
不是一个代码编程助手，要严格按照下面 Core Processing Logic 与 Key Processing Rules 小节来处理。

## File Structure

- `sentences.txt` - 包含所有输入的英语句子
- `output.txt` - 目标输出文件（将被创建/覆盖）

## Core Processing Logic

- 输入：来自 `sentences.txt` 文件的句子
- 输出：写入 `output.txt` 文件
- 处理模式：
  - 先将整个英语句子练习一次，不用拆分
  - 将英语句子拆分成多个成分（主语、谓语、宾语、定语、状语、连词、冠词等等）
  - 对每一个成分继续拆分成多个单词，渐进式组合起来练习（**单词** -> **短语** -> **更大的短语**）
  - 每一个成分练习后，**一定要**将当前成分和上一个成分组合起来练习。

## Key Processing Rules

1. 逐行处理`sentences.txt`中的每个句子
2. 去除标点符号和翻译（英文句子后的中文文本）
3. 将英语句子拆分和渐进式组合
4. 对于动词变形，在练习动词变形前，需要先练习动词原型（如： eat -> ate）

## Example Pattern

Input: "The weather was a bit cold"
Output:
```
The weather was a bit cold
The
weather
The weather
be
was
The weather was
a
bit
a bit
cold
a bit cold
The weather was a bit cold
```

## User Command

当用户说“go”时，立即处理`sentences.txt`中的句子，并将结构化的细分内容输出到output.txt。
输出应严格遵循上述 Core Processing Logic 与 Key Processing Rules 小节来处理。
