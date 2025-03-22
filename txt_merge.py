# Ctrl + Shift + P で、python: select interpriterを選択,python 3.13にして実行する。
# C:\Users\masa_\python の配下にある.txtをマージするプログラム
# 前提として、名前の順にソートして全部を結合するため不要なファイルはどかしておく必要あり
import os

def merge_text_files(directory, output_file):
    # ディレクトリ内のテキストファイルを取得して名前順にソート
    text_files = sorted([f for f in os.listdir(directory) if f.endswith(".txt")])

    with open(output_file, "w", encoding="utf-8") as merged_file:
        for text_file in text_files:
            file_path = os.path.join(directory, text_file)
            print(f"Merging {file_path}...")
            with open(file_path, "r", encoding="utf-8") as file:
                # ファイルの内容をマージ
                merged_file.write(file.read() + "\n")
    print(f"All text files merged into {output_file}")

if __name__ == "__main__":
    # テキストファイルが保存されているディレクトリ
    text_directory = r"C:\Users\masa_\python"
    # マージ後のファイル名
    output_merged_file = os.path.join(text_directory, "merged_text_file.txt")
    
    # マージ処理を実行
    merge_text_files(text_directory, output_merged_file)
