import os
import wave
import math
import re
def get_wav_length(wav_file):
    with wave.open(wav_file, 'rb') as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()       
        duration = frames / float(rate)
        rounded_duration = math.ceil(duration)
        return rounded_duration

def is_length_unsupported(file_path,min_len=10,max_len=17):
    x=get_wav_length(file_path)
    if x < min_len or x > max_len:
        return True
    return False   

def remove_duplicates_letters_in_word(word):
    seen = set()
    result = []
    for letter in word:
        if letter not in seen:
            seen.add(letter)
            result.append(letter)
    return "".join(result)


def is_repeat_letter_in_word_at_sentence(wav_file, max_ok_len=6):
    old_path=r'C:\dataset_no_music_splitted'
    new_path=r'C:\dataset_text'
    new_extension = ".txt"
    new_text=wav_file.replace(old_path,new_path,1)
    new_text=os.path.splitext(new_text)[0]+new_extension
    if not os.path.isfile(new_text):
        return False
    with open(new_text,"r",encoding="utf-8") as file:
        content=file.read()
        words = content.split()
        for word in words:
            unique_letters = remove_duplicates_letters_in_word(word)
            for letter in unique_letters:
                if word.count(letter) > max_ok_len:
                    return True
    return False

def is_text_has_english(wav_file):
    old_path=r'C:\dataset_no_music_splitted'
    new_path=r'C:\dataset_text'
    new_extension = ".txt"
    new_text=wav_file.replace(old_path,new_path,1)
    new_text=os.path.splitext(new_text)[0]+new_extension
    if(not os.path.isfile(new_text)):
        return False
    with open(new_text, "r",encoding='unicode_escape') as file:
        content = file.read()
        if re.search(r'[a-zA-Z]', content):
            with open(r"words.txt","a") as file2:
                english_word_pattern = re.compile(r'[a-zA-Z]+')
                for line in content.splitlines():
                    words = english_word_pattern.findall(line)
                    for word in words:
                        file2.write(f"{word} \n")
                return True
        else:
            return False


def get_bad_files_in_folder(input_folder):
    bad_files=[]
    total_time_of_bad_files=0
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)
            time_of_file=get_wav_length(file_path)
            # if time_of_file>max_len or time_of_file<min_len:
            if is_text_has_english(file_path) or is_length_unsupported(file_path) or is_repeat_letter_in_word_at_sentence(file_path):
                total_time_of_bad_files+=time_of_file
                bad_files.append(file_path)
    return bad_files,total_time_of_bad_files

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


def search_all_bad_length(input_folder):
    bad_files=[]
    total_time_of_bad_files=0
    dirs=get_directory_paths(input_folder)
    new_bad_files,time_of_new_bad_files = get_bad_files_in_folder(input_folder)
    total_time_of_bad_files += time_of_new_bad_files
    bad_files.extend(new_bad_files)
    for i in dirs:
        new_bad_files,time_of_new_bad_files = get_bad_files_in_folder(os.path.join(input_folder,i))
        total_time_of_bad_files += time_of_new_bad_files
        bad_files.extend(new_bad_files)
    return bad_files,total_time_of_bad_files


folder_to_search=r"C:\dataset_no_music_splitted"
files,time = search_all_bad_length(folder_to_search)
print(f"bad length files : {files}")
print(f"wasted time in hours : {time/3600}")



old_path=r'C:\dataset_no_music_splitted'
new_path=r'C:\dataset_text'
new_extension = ".txt" 
text_to_delete=[]
for file_path in files:
    new_text=file_path.replace(old_path,new_path,1)
    new_text=os.path.splitext(new_text)[0]+new_extension
    text_to_delete.extend([new_text])

print(text_to_delete)
# for file_path in files:
#     try:
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#             print(f"Deleted: {file_path}")
#         else:
#             print(f"File not found or not a file: {file_path}")
#     except Exception as e:
#         print(f"Error deleting {file_path}: {e}")


# for file_path in text_to_delete:
#     try:
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#             print(f"Deleted: {file_path}")
#         else:
#             print(f"File not found or not a file: {file_path}")
#     except Exception as e:
#         print(f"Error deleting {file_path}: {e}")