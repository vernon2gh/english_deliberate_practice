import sys
import os
import re
import argparse
import asyncio
import edge_tts
import mpv
from termcolor import colored

def data_read(file_path):
    with open(file_path, 'r') as file:
        tmp = file.readlines()
    return [data.strip() for data in tmp]

async def chunk_generate_mp3(chunk) -> str:
    cache_dir = ".mp3_cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{chunk}.mp3")

    if not os.path.exists(cache_file):
        communicate = edge_tts.Communicate(chunk, "en-US-AndrewNeural")
        await communicate.save(cache_file)

    return cache_file

def chunk_play(chunk):
    mp3 = asyncio.run(chunk_generate_mp3(chunk))
    player = mpv.MPV()
    player.play(mp3)
    player.wait_for_playback()

# Remove punctuation, Chinese characters, and convert to lowercase
def chunk_to_raw(chunk):
    chunk = re.sub(r'[^\w\s]', '', chunk)
    chunk = re.sub(r'[\u4e00-\u9fff]', '', chunk)
    return chunk.strip().lower()

def sentence_split(sentence):
    words = chunk_to_raw(sentence).split()
    chunks = []
    for i in range(len(words)):
        chunks.append(words[i])
        if i > 0:
            chunks.append(' '.join(words[:i+1]))
    chunks[-1] = sentence
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
        chunk_raw = chunk_to_raw(chunk)
        if cache:
            asyncio.run(chunk_generate_mp3(chunk_raw))
            continue

        while True:
            if not hear:
                print(colored(chunk, 'grey'), end="\r")
            chunk_play(chunk_raw)
            user_input = chunk_to_raw(input())
            # Go back to the beginning of the previous line
            # and clear the contents.
            print("\033[F\033[K", end="")
            sys.stdout.flush()
            if user_input == chunk_raw:
                break

def sentence_main(sentence_path, filter_path, split=False, hear=False, cache=False):
    sentences = data_read(sentence_path)

    for sentence in sentences:
        chunks = sentence
        if split:
            chunks = sentence_split(chunks)
            chunks = chunks_filter(filter_path, chunks)
        chunks_run(chunks, hear, cache)

def word_filter(filter_path, words):
    if not os.path.exists(filter_path):
        return words
    with open(filter_path, 'r') as file:
        filter = [line.strip().lower() for line in file]
    return [part for part in words if part not in filter]

def words_ebbinghaus(chunks):
    intervals = [1, 2, 4, 7, 15]
    ebbinghaus_chunks = []
    chunk_groups = [chunks[i:i + 20] for i in range(0, len(chunks), 20)]

    for group in chunk_groups:
        chunks_day = [[] for _ in range(35)]
        for i, chunk in enumerate(group):
            chunks_day[i].append(chunk)

        for i, chunk in enumerate(group):
            for interval in intervals:
                chunks_day[i + interval].append(chunk)

        ebbinghaus_chunks.extend([item for sublist in chunks_day for item in sublist])

    return ebbinghaus_chunks

def word_main(word_path, filter_path, split=False, hear=False, cache=False):
    words = data_read(word_path)

    chunks = word_filter(filter_path, words)
    if split:
            chunks = words_ebbinghaus(chunks)
    chunks_run(chunks, hear, cache)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some sentences.')
    parser.add_argument('--hear',  action='store_true', help="hear-write sentence/chunk/word")
    parser.add_argument('--split', action='store_true', help="split sentence to chunks or generate word based on the Ebbinghaus rule")
    parser.add_argument('--cache', action='store_true', help="pre-generate mp3 audio cache")
    parser.add_argument('--word',  action='store_true', help="practice the words only")
    parser.add_argument('--ffile', type=str, default='./filter.txt', help="path to filter file")
    parser.add_argument('--sfile', type=str, default='./sentences.txt', help="path to sentences file")
    parser.add_argument('--wfile', type=str, default='./word.txt', help="path to word file")
    args = parser.parse_args()

    if args.word:
        word_main(args.wfile, args.ffile, args.split, args.hear, args.cache)
    else:
        sentence_main(args.sfile, args.ffile, args.split, args.hear, args.cache)