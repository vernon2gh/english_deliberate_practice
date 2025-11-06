# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a language learning text processing project that generates vocabulary and phrase breakdown exercises from input sentences. The system takes English sentences and produces structured output showing word-by-word breakdowns, phrase combinations, and progressive sentence building.

## Core Processing Logic

- **Input**: Sentences from `sentences.txt` file
- **Output**: Structured language learning exercises written to `output.txt`
- **Processing Pattern**:
  - Break sentences into individual words
  - Show progressive phrase building (word → phrase → larger phrase)
  - Include verb conjugations (e.g., "eat" → "ate")
  - For multi-word phrases like "a bit cold", show the individual phrase practice before combining with the full sentence

## File Structure

- `sentences.txt` - Contains input sentences to process
- `README.md` - Contains example input/output format and processing rules
- `output.txt` - Target output file (will be created/overwritten)

## Key Processing Rules

1. Process each sentence from `sentences.txt` line by line
2. Remove punctuation and translations (Chinese text after English sentences)
3. Break sentences into words and show progressive combinations
4. For phrases like "a bit cold", show individual phrase practice before full sentence combination
5. Include verb forms (infinitive → conjugated) where applicable

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
