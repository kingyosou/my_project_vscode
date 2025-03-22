import os
from PIL import Image
import pytesseract

# Tesseractの実行ファイルのパスを指定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# TESSDATA_PREFIXを明示的に設定
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

def extract_text_from_images(folder_path):
    """
    フォルダ内のすべての画像ファイルに対して縦書きモードでOCRを実行し、結果をテキストファイルに出力する。
    :param folder_path: 画像ファイルが格納されたフォルダのパス
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            file_path = os.path.join(folder_path, filename)
            print(f"処理中の画像: {filename}")
            try:
                # OCRを実行
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='jpn_vert')
                print(f"OCR結果:\n{text}")
            except pytesseract.TesseractError as e:
                print(f"TesseractError: {e}")
            except Exception as ex:
                print(f"エラー: {ex}")

if __name__ == "__main__":
    folder_path = r'C:\Users\masa_\python'
    print(f"Tesseract実行ファイルパス: {pytesseract.pytesseract.tesseract_cmd}")
    print(f"TESSDATA_PREFIX: {os.environ.get('TESSDATA_PREFIX')}")
    extract_text_from_images(folder_path)
