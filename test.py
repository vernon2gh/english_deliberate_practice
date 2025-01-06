import sys
import os
import re
import argparse
import pyttsx3
from termcolor import colored

def sentences_read(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

def sentence_play(sentence):
    engine = pyttsx3.init()
    engine.say(sentence)
    engine.runAndWait()

# Remove punctuation, Chinese characters, and convert to lowercase
def sentence_raw(sentence):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = re.sub(r'[\u4e00-\u9fff]', '', sentence)
    return sentence.strip().lower()

def sentence_split(sentence):
    words = sentence.split()
    chunks = []
    for i in range(len(words)):
        chunks.append(words[i])
        if i > 0:
            chunks.append(' '.join(words[:i+1]))
    return chunks

def chunks_filter(filter_path, chunks):
    if not os.path.exists(filter_path):
        return chunks
    with open(filter_path, 'r') as file:
        filter = [line.strip().lower() for line in file]
    return [part for part in chunks if part not in filter]

def chunks_run(chunks, hear=False):
    if not isinstance(chunks, list):
        chunks = [chunks]
    for chunk in chunks:
        while True:
            if not hear:
                print(colored(chunk, 'grey'), end="\r")
            sentence_play(chunk)
            user_input = sentence_raw(input())
            if user_input == chunk:
                break

def do_main(file_path, filter_path, split=False, hear=False):
    sentences = sentences_read(file_path)

    for sentence in sentences:
        chunks = sentence_raw(sentence)
        if split:
            chunks = sentence_split(chunks)
            chunks = chunks_filter(filter_path, chunks)
        chunks_run(chunks, hear)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some sentences.')
    parser.add_argument('--hear', action='store_true', help="Hear sentence/chunk/word")
    parser.add_argument('--split', action='store_true', help="Chunk split")
    parser.add_argument('--filter', type=str, default='./filter.txt', help="Path to chunk filter file")
    parser.add_argument('--file', type=str, default='./sentences.txt', help="Path to sentences file")
    args = parser.parse_args()

    do_main(args.file, args.filter, args.split, args.hear)