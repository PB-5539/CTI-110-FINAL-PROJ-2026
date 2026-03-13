import winsound
import os

#find filepath for audio files
wav_file = os.path.join("finalproject", "Audio", "WAV", "MainMenu.wav")

# Check if file exists
if os.path.isfile(wav_file):
    print("Playing:", wav_file)
    winsound.PlaySound(wav_file, winsound.SND_FILENAME)
else:
    print("File not found:", wav_file)