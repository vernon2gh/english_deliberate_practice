# Introduction

This is a Python script for learning English. It provides functionalities to
split sentences into chunks, filter chunks, play audio, practice sentences,
practice words using the Ebbinghaus forgetting curve, and listen mode.

- deliberate practice: interactively practice sentences or words through repetition.
- sentence processing: read sentences from a file, split them into chunks,
                       filter chunks, play audio, and practice sentences.
- word processing    : read words from a file, filter them, and practice words
                       using the Ebbinghaus forgetting curve.
- error note         : collect sentences/blocks/words that users practice incorrectly.
- listen mode        : repeat a specified number of times at specified intervals
                       for intensive listening training
- audio cache        : pre-generate audio cache to improve performance.

# Dependencies

Before running the script, make sure to install the required dependencies:

```bash
(.venv) pip install edge_tts mpv termcolor
```

# Examples

## Practice sentences

```bash
$ python english_deliberate_practice.py.py --prompt --split
```

## Listen sentences

```bash
$ python english_deliberate_practice.py.py --prompt --split --listen
```

## Practice words

```bash
$ python english_deliberate_practice.py.py --prompt --split --word
```

## Listen words

```bash
$ python english_deliberate_practice.py.py --prompt --split --word --listen
```

## Supported arguments

The script supports various command-line arguments to control different behaviors:

- `--split`     : split sentences into multiple chunks or generate words based
                  on the Ebbinghaus rule
- `--word`      : practice words only
- `--prompt`    : prompt sentences/chunks/words
- `--cache`     : pre-generate mp3 audio cache
- `--interval`  : interval in seconds for listen mode, default 1
- `--repeat`    : number of times to repeat for listen mode, default 1
- `--listen`    : listen mode
- `--ffile`     : path to the filter file (default: `./filter.txt`)
- `--efile`     : path to error note file (default: `./errornote.txt`)
- `--sfile`     : path to the sentence file (default: `./sentences.txt`)
- `--wfile`     : path to the word file (default: `./word.txt`)
