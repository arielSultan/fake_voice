from pydub import AudioSegment

def speed_up_audio(input_wav, output_wav, speed_factor=1.1):
    # Load the audio file
    sound = AudioSegment.from_wav(input_wav)

    # Speed up the audio
    sound_with_speed = sound.speedup(playback_speed=speed_factor)

    # Export the modified audio
    sound_with_speed.export(output_wav, format="wav")

# Example usage
input_wav = r'C:\program1\my_project\samples\output70000.wav'  # Replace with your input file path
output_wav = 'output.wav'  # Replace with your desired output file path
speed_up_audio(input_wav, output_wav, speed_factor=1.3)


