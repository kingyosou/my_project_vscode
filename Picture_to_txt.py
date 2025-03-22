import os
from PIL import Image
import pytesseract

# Tesseractの実行ファイルのパスを指定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_images(folder_path):
    """
    フォルダ内のすべての画像ファイルに対してOCRを実行し、横書きで失敗した場合は縦書きで再試行する。
    結果をテキストファイルに出力する。
    :param folder_path: 画像ファイルが格納されたフォルダのパス
    """
    for filename in os.listdir(folder_path):
        # 対象が画像ファイルかを確認（拡張子が .png, .jpg, .jpeg, .bmp, .tiff）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            file_path = os.path.join(folder_path, filename)
            print(f"処理中の画像: {filename}")
            
            try:
                # 画像を開いてOCRを実行（横書きモード）
                image = Image.open(file_path)
                print("横書きモードでOCRを実行中...")
                text = pytesseract.image_to_string(image, lang='jpn')
                
                # テキストが空の場合は縦書きモードを試す
                if not text.strip():
                    print("横書きの結果が空です。縦書きモードで再試行します...")
                    # 縦書き用のカスタムオプションを指定
                    text = pytesseract.image_to_string(image, lang='jpn_vert')

                # 出力用テキストファイル名を生成（拡張子を.txtに変更）
                text_file_name = os.path.splitext(filename)[0] + ".txt"
                text_file_path = os.path.join(folder_path, text_file_name)

                # テキストをファイルに保存
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                
                print(f"テキストファイルに保存しました: {text_file_name}")
            
            except Exception as e:
                print(f"エラーが発生しました（{filename}）: {e}")

if __name__ == "__main__":
    # 対象のフォルダを指定
    folder_path = r'C:\Users\masa_\python'
    
    # テキスト抽出を実行
    extract_text_from_images(folder_path)
