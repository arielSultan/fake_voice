import wave
import math
import os

def get_wav_length(wav_file):
    with wave.open(wav_file, 'rb') as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()       
        duration = frames / float(rate)
        rounded_duration = math.ceil(duration)
        return rounded_duration

def combine_files(list_audio, list_text, output_audio, output_text):
    with wave.open(output_audio, 'wb') as output_wav:
        with wave.open(list_audio[0], 'rb') as first_wav:
            output_wav.setparams(first_wav.getparams())
        for wav_file in list_audio:
            with wave.open(wav_file, 'rb') as input_wav:
                output_wav.writeframes(input_wav.readframes(input_wav.getnframes()))
        with open(output_text, 'w', encoding='utf-8') as output_txt:
            for txt_file in list_text:
                with open(txt_file, 'r', encoding='utf-8') as input_txt:
                    output_txt.write(input_txt.read())
                    output_txt.write(' ')

def combine_on_folder(input_audio_folder, input_text_folder, output_audio_folder, output_text_folder):
    audio_files = { os.path.join(input_audio_folder, file) for file in os.listdir(input_audio_folder) if file.endswith('.wav') and os.path.isfile(os.path.join(input_audio_folder, file)) } 
    done=set()
    for audio_path in audio_files.copy():
        base_name = os.path.basename(audio_path)
        name_without_extension = os.path.splitext(base_name)[0]
        split_text = name_without_extension.rsplit('_', 1)
        cont_without_extension = split_text[0] + "_" + str(int(split_text[1]) + 1)
        cont_name = cont_without_extension + ".wav"
        cont = os.path.join(os.path.dirname(audio_path),cont_name)
        if audio_path in done or cont in done:
            continue
        if not os.path.isfile(cont):
            continue 
        if get_wav_length(audio_path)+get_wav_length(cont) > 30:
            continue
        text_first=os.path.join(input_text_folder,name_without_extension+".txt")
        text_second=os.path.join(input_text_folder,cont_without_extension+".txt")
        if not os.path.isfile(text_first) or not os.path.isfile(text_second):
            continue
        list_audio = [audio_path, cont]
        list_text = [text_first, text_second]
        output_audio = os.path.join(output_audio_folder,name_without_extension+cont_without_extension+"combined.wav")
        output_text = os.path.join(output_text_folder,name_without_extension+cont_without_extension+"combined.txt")
        if not (os.path.isfile(output_audio) or os.path.isfile(output_text)):
            combine_files(list_audio,list_text,output_audio,output_text)
        done.add(cont)
        done.add(audio_path)
    
audios = r"C:\dataset_no_music_splitted\year22"
texts = r"C:\dataset_text\year22"
output_audio=r"C:\dataset_no_music_splitted\combined"
output_text=r"C:\dataset_text\combined"
combine_on_folder(audios,texts,output_audio,output_text)
    

