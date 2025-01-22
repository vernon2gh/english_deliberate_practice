import sys
import os
import re
import argparse
import asyncio
import time
import edge_tts
import mpv
import threading
import spacy
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

def chunk_play(chunk, interval, repeat, stop_event=None):
    mp3 = asyncio.run(chunk_generate_mp3(chunk))
    player = mpv.MPV()
    for _ in range(repeat):
        player.play(mp3)
        if not stop_event:
            player.wait_for_playback()
            time.sleep(interval)
            continue

        while player.duration is None:
            time.sleep(0.1)
        for _ in range(int((player.duration + interval) / 0.1)):
            if stop_event.is_set():
                if player.time_pos is not None and player.duration is not None and \
                   player.time_pos < player.duration:
                    player.stop()
                return
            time.sleep(0.1)

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
    chunks[-1] = chunk_to_raw(sentence)
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

def chunks_prototype(chunks):
    nlp = spacy.load("en_core_web_sm")
    previous_chunk = None
    result = []
    for chunk in chunks:
        if ' ' in chunk:
            sub_chunks = chunk.split()
            if previous_chunk in sub_chunks:
                result.append(chunk)
                continue
            for sub_chunk in sub_chunks:
                doc = nlp(sub_chunk)
                lemma = doc[0].lemma_
                if sub_chunk != lemma:
                    result.append(lemma)
                    result.append(sub_chunk)
                    previous_chunk = sub_chunk
            result.append(chunk)
            continue
        doc = nlp(chunk)
        lemma = doc[0].lemma_
        if chunk != lemma:
            result.append(lemma)
            previous_chunk = chunk
        result.append(chunk)
    return result

def chunk_colored(user_input, chunk):
    if user_input == chunk_to_raw(chunk):
        return colored(chunk, 'grey')

    result = []
    for i, char in enumerate(chunk):
        if re.match(r'[\u4e00-\u9fff]', char) or re.match(r'[^\w\s]', char):
            result.append(colored(char, 'grey'))
        elif i < len(user_input) and char.lower() == user_input[i].lower():
            result.append(colored(char, 'grey'))
        else:
            result.append(colored(char, 'light_red'))
    return ''.join(result)

def chunks_run(chunks, listen, interval, repeat, prompt, cache, error_path):
    if not isinstance(chunks, list):
        chunks = [chunks]
    for chunk in chunks:
        chunk_raw = chunk_to_raw(chunk)
        user_input = chunk_raw
        if cache:
            asyncio.run(chunk_generate_mp3(chunk_raw))
            continue
        if listen:
            if prompt:
                print(chunk_colored(user_input, chunk), end="\r")
            chunk_play(chunk_raw, interval, repeat)
            if prompt:
                # Clear the contents.
                print("\033[K", end="")
                sys.stdout.flush()
            continue

        error_count = 0
        while True:
            if prompt:
                print(chunk_colored(user_input, chunk), end="\r")
            stop_event = threading.Event()
            play_thread = threading.Thread(target=chunk_play, args=(chunk_raw, interval, repeat, stop_event))
            play_thread.start()
            user_input = chunk_to_raw(input())
            stop_event.set()
            play_thread.join()
            # Go back to the beginning of the previous line
            # and clear the contents.
            print("\033[F\033[K", end="")
            sys.stdout.flush()
            if user_input == chunk_raw:
                break

            error_count += 1
            if error_count % 3 != 0:
                continue
            with open(error_path, "a") as error_file:
                error_file.write(chunk + "\n")
            print(chunk_colored(user_input, chunk), end="\r")

def sentence_main(sentence_path, filter_path, error_path, split, listen, interval, repeat, prompt, cache):
    sentences = data_read(sentence_path)

    for sentence in sentences:
        chunks = sentence
        if split:
            chunks = sentence_split(chunks)
            chunks = chunks_filter(filter_path, chunks)
            chunks = chunks_prototype(chunks)
            chunks.insert(0, sentence)
        chunks_run(chunks, listen, interval, repeat, prompt, cache, error_path)

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

def word_main(word_path, filter_path, error_path, split, listen, interval, repeat, prompt, cache):
    words = data_read(word_path)

    chunks = word_filter(filter_path, words)
    if split:
            chunks = words_ebbinghaus(chunks)
    chunks_run(chunks, listen, interval, repeat, prompt, cache, error_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='English deliberate practice')
    parser.add_argument('--split', action='store_true', help="split sentence to chunks or generate word based on the Ebbinghaus rule")
    parser.add_argument('--word',  action='store_true', help="practice the words only")
    parser.add_argument('--prompt',  action='store_true', help="prompt sentence/chunk/word")
    parser.add_argument('--cache', action='store_true', help="pre-generate audio cache")
    parser.add_argument('--interval', type=int, default=1, help="interval in seconds for playback audio, default 1")
    parser.add_argument('--repeat', type=int, default=1, help="number of times to repeat for playback audio, default 1")
    parser.add_argument('--listen',  action='store_true', help="listen mode")
    parser.add_argument('--ffile', type=str, default='./filter.txt', help="path to filter file")
    parser.add_argument('--efile', type=str, default='./errornote.txt', help="path to error note file")
    parser.add_argument('--sfile', type=str, default='./sentences.txt', help="path to sentences file")
    parser.add_argument('--wfile', type=str, default='./word.txt', help="path to word file")
    args = parser.parse_args()

    if args.word:
        word_main(args.wfile, args.ffile, args.efile, args.split, args.listen,
                  args.interval, args.repeat, args.prompt, args.cache)
    else:
        sentence_main(args.sfile, args.ffile, args.efile, args.split, args.listen,
                      args.interval, args.repeat, args.prompt, args.cache)
