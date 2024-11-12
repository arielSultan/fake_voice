import numpy as np
from scipy.signal import butter, filtfilt

def butter_bandstop(lowcut, highcut, fs, order=3):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a

def apply_bandstop_filter(data, lowcut, highcut, fs):
    b, a = butter_bandstop(lowcut, highcut, fs)
    y = filtfilt(b, a, data)
    return y

# Function to clean "rrrr" without affecting voice depth
def clean_rrr_automatically(wav_file, output_file, lowcut=1300, highcut=2500):
    import librosa
    import soundfile as sf
    
    # Step 1: Load WAV file
    y, sr = librosa.load(wav_file, sr=None)
    
    # Step 2: Apply bandstop filter to target "rrrr" frequencies (1500-2500 Hz is more targeted)
    filtered_y = apply_bandstop_filter(y, lowcut=lowcut, highcut=highcut, fs=sr)
    
    # Step 3: Save the output WAV file
    sf.write(output_file, filtered_y, sr)

# Example usage    
clean_rrr_automatically(r'C:\program1\my_project\samples\send_to_pini\pini4.wav', 'output_cleaned.wav')
