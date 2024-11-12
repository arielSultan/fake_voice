import os
import subprocess
import shutil
import gc
import wave
import math

def get_wav_length(wav_file):
    with wave.open(wav_file, 'rb') as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()       
        duration = frames / float(rate)
        rounded_duration = math.ceil(duration)
        return rounded_duration
    
def separate_vocals(input_wav_path, output_dir,max_len=40):
    file_name = os.path.basename(input_wav_path)
    output_file = os.path.join(output_dir, file_name)
    if os.path.isfile(output_file): 
        print(f"{output_file} already cleaned")
        return output_file
    len_of_audio=get_wav_length(input_wav_path)
    if(len_of_audio/60 > max_len):
        print(f"{input_wav_path} too long , skipped")
        return ""
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run Demucs model on the input file to separate vocals
    command = [
        'demucs',
        '--two-stems', 'vocals',  # Only separate vocals from the rest
        '-o', output_dir,         # Output directory for separated files
        input_wav_path
    ]
    
    subprocess.run(command, check=True)

    demucs_output_dir = os.path.join(output_dir, 'htdemucs', os.path.splitext(os.path.basename(input_wav_path))[0])
    vocal_file = os.path.join(demucs_output_dir, 'vocals.wav')

    # Rename the vocal file to match the input file name (keeping .wav extension)
    final_vocal_file = os.path.join(output_dir, os.path.basename(input_wav_path))
    shutil.move(vocal_file, final_vocal_file)

    # Clean up unnecessary directories and files
    shutil.rmtree(demucs_output_dir)
    demucs_main_dir = os.path.join(output_dir, 'htdemucs')
    if os.path.exists(demucs_main_dir):
        shutil.rmtree(demucs_main_dir)

    print(f'{input_wav_path} cleaned')
    return final_vocal_file

def remove_music_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)
            separate_vocals(file_path, output_folder)
            gc.collect()  # Explicitly free memory after each file is processed

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
            
def dup_folder_remove_music(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    dirs = get_directory_paths(input_folder)
    remove_music_folder(input_folder, output_folder)
    
    for i in dirs:
        remove_music_folder(os.path.join(input_folder, i), os.path.join(output_folder, i))
        gc.collect()  # Free memory after each folder is processed

input_folder = r"C:\dataset_original"
output_directory = r"C:\dataset_no_music" 

dup_folder_remove_music(input_folder, output_directory)
