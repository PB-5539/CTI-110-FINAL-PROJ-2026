# finalproject_audio_converter.py
import os
import subprocess
import shutil
import sys

# Folder containing your audio files
project_audio_folder = os.path.join("FinalProject", "Audio")
output_folder = os.path.join(project_audio_folder, "WAV")
os.makedirs(output_folder, exist_ok=True)

# Try to find ffmpeg in PATH
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path is None:
    print("ERROR: FFmpeg not found! Please install FFmpeg and make sure it is in your PATH.")
    sys.exit(1)

# Loop over all audio files
for filename in os.listdir(project_audio_folder):
    file_path = os.path.join(project_audio_folder, filename)

    # Skip non-audio files
    if not filename.lower().endswith((".mp3", ".wav")):
        continue

    # Determine output path
    wav_filename = os.path.splitext(filename)[0] + ".wav"
    wav_path = os.path.join(output_folder, wav_filename)

    # Skip if already converted
    if os.path.isfile(wav_path):
        print(f"Skipping {filename}, WAV already exists.")
        continue

    print(f"Converting {filename} → {wav_filename}")
    try:
        # Re-encode all files to 16-bit PCM WAV
        subprocess.run([
            ffmpeg_path,
            "-y",                  # overwrite if exists
            "-i", file_path,       # input file
            "-acodec", "pcm_s16le", # 16-bit PCM
            "-ar", "44100",        # 44.1 kHz
            wav_path
        ], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to convert {filename}. Skipping.")

print("All audio files processed. WAVs are ready in the WAV folder!")