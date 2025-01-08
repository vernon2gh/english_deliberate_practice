import os
import re
import argparse
import asyncio
import edge_tts
import mpv
from termcolor import colored

def sentences_read(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

async def sentence_generate_mp3(sentence) -> str:
    cache_dir = ".mp3_cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{sentence}.mp3")

    if not os.path.exists(cache_file):
        communicate = edge_tts.Communicate(sentence, "en-US-AndrewNeural")
        await communicate.save(cache_file)

    return cache_file

def sentence_play(sentence):
    mp3 = asyncio.run(sentence_generate_mp3(sentence))
    player = mpv.MPV()
    player.play(mp3)
    player.wait_for_playback()

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

    filtered_chunks = []
    i = 0
    while i < len(chunks):
        if chunks[i] in filter:
            if i > 0 and i < len(chunks) - 2:
                chunks[i + 2] = chunks[i] + ' ' + chunks[i + 2]
            i += 2 if i < len(chunks) - 2 else 1
            continue
        filtered_chunks.append(chunks[i])
        i += 1

    return filtered_chunks

def chunks_run(chunks, hear=False, cache=False):
    if not isinstance(chunks, list):
        chunks = [chunks]
    for chunk in chunks:
        if cache:
            asyncio.run(sentence_generate_mp3(chunk))
            continue

        while True:
            if not hear:
                print(colored(chunk, 'grey'), end="\r")
            sentence_play(chunk)
            user_input = sentence_raw(input())
            if user_input == chunk:
                break

def do_main(file_path, filter_path, split=False, hear=False, cache=False):
    sentences = sentences_read(file_path)

    for sentence in sentences:
        chunks = sentence_raw(sentence)
        if split:
            chunks = sentence_split(chunks)
            chunks = chunks_filter(filter_path, chunks)
        chunks_run(chunks, hear, cache)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some sentences.')
    parser.add_argument('--hear', action='store_true', help="Hear sentence/chunk/word")
    parser.add_argument('--split', action='store_true', help="Chunk split")
    parser.add_argument('--cache', action='store_true', help="Pre-generate mp3 cache")
    parser.add_argument('--filter', type=str, default='./filter.txt', help="Path to chunk filter file")
    parser.add_argument('--file', type=str, default='./sentences.txt', help="Path to sentences file")
    args = parser.parse_args()

    do_main(args.file, args.filter, args.split, args.hear, args.cache)