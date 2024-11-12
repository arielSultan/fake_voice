import os
import shutil
from pydub import AudioSegment

# Duration of silence to add (in milliseconds)
SILENCE_DURATION = 200  # 200 ms

def add_silence(input_wav_path, output_wav_path):
    """Adds silence to the beginning and end of the wav file."""
    # Load the input audio file
    audio = AudioSegment.from_wav(input_wav_path)
    
    # Create silence audio segment
    silence = AudioSegment.silent(duration=SILENCE_DURATION)
    
    # Add silence to the beginning and end
    new_audio = silence + audio + silence
    
    # Export the new audio file
    new_audio.export(output_wav_path, format="wav")

def duplicate_structure_with_silence(src_folder, dest_folder):
    """Duplicates the directory structure and wav files with added silence."""
    for dirpath, dirnames, filenames in os.walk(src_folder):
        # Create corresponding destination directory
        relative_path = os.path.relpath(dirpath, src_folder)
        new_dir = os.path.join(dest_folder, relative_path)
        os.makedirs(new_dir, exist_ok=True)

        for file in filenames:
            if file.endswith('.wav'):
                # Full paths for the source and destination wav files
                src_wav_path = os.path.join(dirpath, file)
                dest_wav_path = os.path.join(new_dir, file)

                # Add silence to the wav file and save it in the destination folder
                add_silence(src_wav_path, dest_wav_path)
            else:
                # Copy other files as-is
                src_file_path = os.path.join(dirpath, file)
                dest_file_path = os.path.join(new_dir, file)
                shutil.copy2(src_file_path, dest_file_path)

if __name__ == "__main__":
    src_folder =r"C:\dataset_no_music_splitted"
    dest_folder =r"C:\dataset_no_music_splitted_silence"

    duplicate_structure_with_silence(src_folder, dest_folder)
