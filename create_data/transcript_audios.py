import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

SAMPLING_RATE = 16000
BATCH_SIZE = 4  # Number of files to process in a batch
NUM_BEAMS = 1    # Reduce beam search size for faster inference

has_cuda = torch.cuda.is_available()
device = 'cuda:0' if has_cuda else 'cpu'
model_path = 'ivrit-ai/whisper-v2-d3-e3'
model = WhisperForConditionalGeneration.from_pretrained(model_path)
processor = WhisperProcessor.from_pretrained(model_path)
if has_cuda:
    model.to(device)
    # Remove mixed precision usage to avoid type mismatch errors
    # model.half()  # Commented out

def process_audio_file(audio_path):
    try:
        audio_array, orig_sr = librosa.load(audio_path, sr=None)
        audio_resample = librosa.resample(audio_array, orig_sr=orig_sr, target_sr=SAMPLING_RATE)
        input_features = processor(audio_resample, sampling_rate=SAMPLING_RATE, return_tensors="pt", padding=True).input_features
        if has_cuda:
            input_features = input_features.to(device)
        predicted_ids = model.generate(input_features, language='he', num_beams=NUM_BEAMS)
        transcript = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        print(f'{audio_path} current file')
        return transcript[0]
    except Exception as e:
        print(f"Error processing file {audio_path}: {e}")
        return None

def transcript_dir(dir_path, output_dir):
    print(f'--------------------------------------{dir_path} current folder--------------------------------------')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    files = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, filename))]
    def process_batch(batch):
        for audio_path in batch:
            output_file_name = os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
            output_file_path = os.path.join(output_dir, output_file_name)
            if(os.path.isfile(output_file_path)):
                print(output_file_name+" already transcripted")
                continue
            
            transcript = process_audio_file(audio_path)
            if transcript:
                with open(output_file_path, 'w') as file:
                    file.write(transcript)
            print(f"Processed file: {os.path.basename(audio_path)}")
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your CPU capabilities
        for i in range(0, len(files), BATCH_SIZE):
            batch = files[i:i+BATCH_SIZE]
            executor.submit(process_batch, batch)

def get_directory_paths(root_dir):
    result = []

    def walk_directory(current_dir, current_path):
        # List all items in the current directory
        items = os.listdir(current_dir)
        
        for item in items:
            # Create the full path of the item
            full_path = os.path.join(current_dir, item)
            
            # Check if the item is a directory
            if os.path.isdir(full_path):
                # Build the path string for the directory
                path_str = current_path + item
                result.append(path_str)
                
                # Recursively walk through the subdirectory
                walk_directory(full_path, path_str + '\\')

    # Start walking from the root directory
    walk_directory(root_dir, '')
    return result

def dup_folder_transcript(input_folder,output_folder):
    dirs=get_directory_paths(input_folder)
    transcript_dir(input_folder,output_folder)
    for i in dirs:
        transcript_dir(os.path.join(input_folder,i),os.path.join(output_folder,i))
    
input_folder = r"C:\dataset_no_music_splitted\others"
output_directory = r"C:\dataset_text\others" 
dup_folder_transcript(input_folder,output_directory)