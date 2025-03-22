# Ctrl + Shift + P で、python: select interpriterを選択,python 3.13にして実行する。
# C:\Users\masa_\python の配下にある動画から音声を抽出し、1分以内にファイル分割する
# 前提として、音声ファイル全部を探すので不要な動画はどかしておく必要あり
import os
from moviepy import VideoFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence
from datetime import datetime

def extract_audio_from_videos(directory):
    # 動画ファイルを処理
    for filename in sorted(os.listdir(directory)):
        if filename.endswith((".mp4", ".mkv", ".avi")):  # 対応する動画形式を指定
            video_path = os.path.join(directory, filename)
            output_audio_path = os.path.join(
                directory, os.path.splitext(filename)[0] + ".wav"
            )
            print(f"Extracting audio from {video_path}...")
            try:
                video = VideoFileClip(video_path)
                video.audio.write_audiofile(output_audio_path)
                print(f"Audio extracted to {output_audio_path}")
            except Exception as e:
                print(f"Failed to extract audio from {filename}: {e}")

def split_audio_by_silence(directory, segment_length=30 * 1000):
    # 音声ファイルを処理
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            
            # 日時情報を取得
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            base_name = os.path.splitext(filename)[0]
            
            # 音声を読み込む
            audio = AudioSegment.from_file(file_path)
            total_length = len(audio)  # 音声全体の長さ（ミリ秒）
            
            # 30秒単位で分割
            for i in range(0, total_length, segment_length):
                start = i
                end = min(i + segment_length, total_length)
                chunk = audio[start:end]
                
                # ファイル名を生成して保存
                chunk_filename = f"{base_name}_{current_time}_{i // segment_length + 1:04}.wav"
                chunk_path = os.path.join(directory, chunk_filename)
                chunk.export(chunk_path, format="wav")
                print(f"Saved {chunk_path}")

if __name__ == "__main__":
    audio_directory = r"C:\Users\masa_\python"
    
    # ステップ1: 動画ファイルから音声を抽出
    extract_audio_from_videos(audio_directory)
    
    # ステップ2: 音声ファイルを無音部分で分割
    split_audio_by_silence(audio_directory)
