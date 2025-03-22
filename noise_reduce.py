# Ctrl + Shift + P で、python: select interpriterを選択,python 3.11にして実行する。
# ノイズを除去できるプログラム。除去強度も調整可能。
import os
import noisereduce as nr
import librosa
import soundfile as sf

def reduce_noise_in_directory(directory, prop_decrease=0.7):
    # 指定したフォルダ内の.wavファイルを処理
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".wav"):  # .wavファイルのみを対象
            input_path = os.path.join(directory, filename)
            output_filename = os.path.splitext(filename)[0] + "_reduced.wav"
            output_path = os.path.join(directory, output_filename)
            
            print(f"Processing {input_path}...")
            
            # 音声ファイルを読み込む
            audio, sr = librosa.load(input_path, sr=None)
            
            # 音声の最初の1秒をノイズサンプルとして使用
            noise_sample = audio[:sr]
            
            # ノイズ除去の強度を調整して処理
            reduced_audio = nr.reduce_noise(
                y=audio,
                sr=sr,
                y_noise=noise_sample,
                prop_decrease=prop_decrease  # ノイズ除去強度（0.0～1.0）
            )
            
            # ノイズ除去後の音声を保存
            sf.write(output_path, reduced_audio, sr)
            print(f"Noise reduced audio saved to {output_path}")

# フォルダを指定
directory = r"C:\Users\masa_\python"

# 実行
reduce_noise_in_directory(directory, prop_decrease=0.4)
