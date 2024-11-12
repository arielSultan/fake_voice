from pydub import AudioSegment
from pydub.silence import detect_silence
import numpy as np

def remove_silence(input_file, output_file, silence_thresh=-50, min_silence_len=1500):
    audio = AudioSegment.from_wav(input_file)
    silence_ranges = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    silence_ranges = [(start, end) for start, end in silence_ranges if (end - start) > min_silence_len]
    segments = []
    prev_end = 0
    for start, end in silence_ranges:
        if start > prev_end:
            segments.append(audio[prev_end:start])
        prev_end = end
    if prev_end < len(audio):
        segments.append(audio[prev_end:])
    cleaned_audio = sum(segments)
    cleaned_audio.export(output_file, format="wav")

# Example usage
input_file = r"C:\Users\ariel\project\my.wav"
output_file = r"output_cleaned.wav"
remove_silence(input_file, output_file)
#