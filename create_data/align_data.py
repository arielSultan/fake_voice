import os

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

def align_wav_txt_files(wav_folder_path,txt_folder_path,output_file_path):
    with open(output_file_path, "a", encoding="utf-8") as output:
        for file in os.listdir(wav_folder_path):
            if file.endswith(".wav"):
                file_name=os.path.splitext(file)[0]
                text_path=os.path.join(txt_folder_path,file_name+".txt")
                sound_path = os.path.join(wav_folder_path, file)
            try:
                    if( not os.path.isfile(text_path)):
                        print(f'{text_path} not exist')
                        continue
                    with open(text_path, "r", encoding="utf-8") as text_file:
                        content = text_file.read()
                        
                        output.write(f"{sound_path}|{content} \n")
            except:
                print(f'error with this file {sound_path} {text_path}')
            


text_files=r'C:\dataset_text_english\year23'
sound_files=r'C:\dataset_no_music_splitted_silence\year23'
output=r'C:\program1\my_project\data.txt'
align_wav_txt_files(sound_files,text_files,output)