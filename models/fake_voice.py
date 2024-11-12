from huggingface_hub import login
import torch
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from transformers import SpeechT5ForTextToSpeech
from IPython.display import Audio
import soundfile as sf
from transformers import SpeechT5HifiGan
import torch
from transformers import SpeechT5Processor



## general vars
#---------------------------------------------
SAMPLING_RATE = 16000
NUM_BEAMS = 1
#---------------------------------------------


# models vars
#---------------------------------------------
__has_cuda__ = None
__model_STT__ = None
__processor_STT__ = None
__device__ = None
__processor_TTS__ = None
__model_TTS__ = None
__speaker_embeddings__ = None
__vocoder__ = None
#---------------------------------------------

def init(path_to_var=r'C:\program1\my_project\models\var.txt'):
    global __has_cuda__, __model_STT__, __processor_STT__, __device__,__processor_TTS__,__model_TTS__,__speaker_embeddings__,__vocoder__
    login(token="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")
    __has_cuda__ = torch.cuda.is_available()
    __device__ = 'cuda:0' if __has_cuda__ else 'cpu'
    model_path = 'ivrit-ai/whisper-v2-d3-e3'
    __model_STT__ = WhisperForConditionalGeneration.from_pretrained(model_path)
    __processor_STT__ = WhisperProcessor.from_pretrained(model_path)
    if __has_cuda__:
        __model_STT__.to(__device__)
    checkpoint ="microsoft/speecht5_tts"
    __processor_TTS__ = SpeechT5Processor.from_pretrained(checkpoint)
    __model_TTS__ = SpeechT5ForTextToSpeech.from_pretrained(
    "arielSultan/final_project_70000"
    )
    with open(path_to_var, 'r') as file:
        content = file.read()
        example = eval(content)
    __speaker_embeddings__ = torch.tensor(example).unsqueeze(0)
    __vocoder__ = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")



def audio_to_text(audio_path):
    try:
        audio_array, orig_sr = librosa.load(audio_path, sr=None)
        audio_resample = librosa.resample(audio_array, orig_sr=orig_sr, target_sr=SAMPLING_RATE)
        input_features = __processor_STT__(audio_resample, sampling_rate=SAMPLING_RATE, return_tensors="pt", padding=True).input_features
        if __has_cuda__:
            input_features = input_features.to(__device__)
        predicted_ids = __model_STT__.generate(input_features, language='he', num_beams=NUM_BEAMS)  
        transcript = __processor_STT__.batch_decode(predicted_ids, skip_special_tokens=True)
        print(f"Transcript for {audio_path}: {transcript[0]}")
        return transcript[0]
    except Exception as e:
        print(f"Error processing file {audio_path}: {e}")
        return None
    


def hebrew_english_text_to_audio(text,output_path):
    inputs = __processor_TTS__(text=text, return_tensors="pt")
    speech = __model_TTS__.generate_speech(inputs["input_ids"], __speaker_embeddings__, vocoder=__vocoder__)
    Audio(speech.numpy(), rate=16000)
    sf.write(output_path, speech.numpy(), 16000)

init()
text='yofiy shel savlanoot mool bdey hhayeled shemfasepes kan legamerey bahhaganahh , aniy rotsehh lehhazkiyr , hhahhaganahh hhahiy halashahh baliygahh , hhahhaganahh shel sekermaneto . kan daniy im yofiy shel hhaganahh al badey hhayeled aharey hhefiyk ened rol , im hhakoneteset , sholeah oto smolahh velo leyad hhaymiyniyt shelo , veaz im hhakoneteset al hhayad hhaymiyniyt , zriykahh kashahh , gam im. '
output=r'C:\program1\my_project\samples\send_to_pini\tmp.wav'
hebrew_english_text_to_audio(text,output)