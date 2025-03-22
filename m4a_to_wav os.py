# Ctrl + Shift + P で、python: select interpriterを選択,python 3.13にして実行する。
# 音声ファイル形式を変換する。
import os
from pydub import AudioSegment

def convert_m4a_to_wav_in_directory(directory):
    try:
        # Get a list of all .m4a files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.m4a')]
        
        if not files:
            print("No .m4a files found in the directory.")
            return
        
        for file in files:
            input_path = os.path.join(directory, file)
            output_path = os.path.join(directory, f"{os.path.splitext(file)[0]}.wav")
            
            # Load the .m4a file
            audio = AudioSegment.from_file(input_path, format="m4a")
            # Export as .wav
            audio.export(output_path, format="wav")
            print(f"Converted {file} to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Directory to process
input_directory = r"C:\Users\masa_\python"  # Replace with your target directory path

convert_m4a_to_wav_in_directory(input_directory)
