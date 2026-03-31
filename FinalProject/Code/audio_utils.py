import winsound
import os
def play_audio(filename):
    #find filepath for audio files
    wav_file = os.path.join("finalproject", "Audio", "WAV", filename)

    # Check if file exists
    if os.path.isfile(wav_file):
        print("Playing:", wav_file)
        winsound.PlaySound(wav_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        print("File not found:", wav_file)