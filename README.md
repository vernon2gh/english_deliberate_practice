# Introduction

This is a Python script for learning English. It provides functionalities to
split sentences into chunks, filter chunks, play audio, practice sentences,
and practice words using the Ebbinghaus forgetting curve.

- deliberate practice: interactively practice sentences or words through repetition.
- sentence processing: read sentences from a file, split them into chunks,
                       filter chunks, play audio, and practice sentences.
- word processing    : read words from a file, filter them, and practice words
                       using the Ebbinghaus forgetting curve.
- audio cache        : pre-generate audio cache to improve performance.

# Dependencies

Before running the script, make sure to install the required dependencies:

```bash
(.venv) pip install edge_tts mpv termcolor
```

# Examples

## Practice sentences

```bash
$ python test.py --hear --split
```

## Practice words

```bash
$ python test.py --hear --split --word
```

## Supported arguments

The script supports various command-line arguments to control different behaviors:

- `--hear` : hear-write sentences/chunks/words
- `--split`: split sentences into multiple chunks or generate words based
             on the Ebbinghaus rule
- `--cache`: pre-generate mp3 audio cache
- `--word` : practice words only
- `--ffile`: path to the filter file (default: `./filter.txt`).
- `--sfile`: path to the sentence file (default: `./sentences.txt`).
- `--wfile`: path to the word file (default: `./word.txt`).
