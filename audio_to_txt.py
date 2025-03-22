import os
import speech_recognition as sr
from datetime import datetime

def transcribe_audio_files(directory, output_text_path):
    recognizer = sr.Recognizer()
    unprocessed_files = []  # テキスト化できなかったファイルを記録するリスト

    with open(output_text_path, "w", encoding="utf-8") as output_file:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".wav"):
                file_path = os.path.join(directory, filename)
                print(f"Processing {file_path}...")
                with sr.AudioFile(file_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio_data, language="ja-JP")
                        output_file.write(text + "\n")
                        print(f"Transcribed {filename} successfully.")
                    except sr.UnknownValueError:
                        print(f"Could not understand audio in {filename}.")
                        unprocessed_files.append(filename)  # リストに追加
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")

    return unprocessed_files  # テキスト化できなかったファイル名を返す

if __name__ == "__main__":
    # 音声ファイルが保存されているディレクトリ
    audio_directory = r"C:\Users\masa_\python"

    # 現在の年月日時分秒を取得してファイル名に付与
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    output_text_file = os.path.join(audio_directory, f"transcription_{current_time}.txt")

    # 処理開始
    unprocessed_files = transcribe_audio_files(audio_directory, output_text_file)

    # テキスト化できなかったファイルのリストを出力
    if unprocessed_files:
        error_log_file = os.path.join(audio_directory, f"error_log_{current_time}.txt")
        with open(error_log_file, "w", encoding="utf-8") as log_file:
            log_file.write("Could not process the following files:\n")
            log_file.write("\n".join(unprocessed_files))

        print(f"The following files could not be transcribed: {', '.join(unprocessed_files)}")
        print(f"Error log saved to {error_log_file}")
    else:
        print("All files were successfully transcribed.")
