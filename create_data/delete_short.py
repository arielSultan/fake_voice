import os
import wave

# Function to get the duration of a .wav file in seconds
def get_wav_duration(file_path):
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration

# Directory to search in
directory = r"C:\dataset_no_music_splitted_silence"

# Initialize counter for wav files over 20 seconds
count = 0

# Walk through all subdirectories and files
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            content=""
            # with open(file_path,"r",encoding="utf-8") as myfile:
            #     content=myfile.read()

            if get_wav_duration(file_path)<10:
                count += 1
                print(f'{file_path} content : \n {content}')
                # os.remove(file_path)

print(f"Number of wav files over 20 seconds: {count}")
