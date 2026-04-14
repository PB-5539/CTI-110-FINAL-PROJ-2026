import winsound
import os
import threading as th

# Thread-safe print lock for audio_utils
_audio_print_lock = th.Lock()

def play_audio(filename):
    """Play audio file asynchronously without blocking."""
    #find filepath for audio files
    wav_file = os.path.join("finalproject", "Audio", "WAV", filename)

    # Check if file exists
    if os.path.isfile(wav_file):
        with _audio_print_lock:
            print("Playing:", wav_file)
        winsound.PlaySound(wav_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        with _audio_print_lock:
            print("File not found:", wav_file)