import os
from pydub import AudioSegment
from pydub.silence import detect_silence
import bisect
import time

def split_audio(input_file, output_dir, silence_thresh=-35, min_silence_len_between_sentences=200,len_of_sample=10):
    print(f'{input_file} current file')
    input_file_name = os.path.splitext(os.path.basename(input_file))[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audio = AudioSegment.from_wav(input_file)
    silence_ranges = detect_silence(audio, min_silence_len=min_silence_len_between_sentences, silence_thresh=silence_thresh)
    silence_ranges = [(start+end)/2 for start, end in silence_ranges if (end - start) > min_silence_len_between_sentences]
    pointer = 0 
    prevPointer = 0
    len_of_audio = len(audio)
    rounds = 0
    
    while pointer < len_of_audio:
        pointer += len_of_sample*1000
        pointer = find_closest_from_above(silence_ranges, pointer)
        if pointer is None or pointer >= len_of_audio:
            pointer = len_of_audio
        if pointer-prevPointer < len_of_sample*1000:
            break
        extracted_audio = audio[prevPointer:pointer]
        file_name = os.path.join(output_dir, f"{input_file_name}_{rounds}.wav")
        extracted_audio.export(file_name, format="wav")
        rounds += 1
        prevPointer = pointer

def find_closest_from_above(sorted_list, x):
    index = bisect.bisect_left(sorted_list, x)
    if index < len(sorted_list):
        return sorted_list[index]
    else:
        return None

def split_folder(input_folder,output_folder):
    print(f'-------------------------------------{input_folder} current folder-------------------------------------')
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)
            split_audio(file_path,output_folder)

def get_directory_paths(root_dir):
    result = []
    def walk_directory(current_dir, current_path):
        items = os.listdir(current_dir)
        for item in items:
            full_path = os.path.join(current_dir, item)
            if os.path.isdir(full_path):
                path_str = current_path + item
                result.append(path_str)
                walk_directory(full_path, path_str + '\\')
    walk_directory(root_dir, '')
    return result

def dup_folder_splited(input_folder,output_folder):
    dirs=get_directory_paths(input_folder)
    split_folder(input_folder,output_folder)
    for i in dirs:
        split_folder(os.path.join(input_folder,i),os.path.join(output_folder,i))




input_folder = r"C:\dataset_no_music_splitted\cut"
output_directory = r"C:\dataset_no_music_splitted\long_splitted"
dup_folder_splited(input_folder, output_directory)
