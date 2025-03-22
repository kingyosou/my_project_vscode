from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

# 商品ページのURL
product_url = 'https://joshinweb.jp/kitchen/390/4974305212887.html?item_list_name=%93%FA%91%D6%82%ED%82%E8%83Z%81[%83%8B%203/15&item_list_id=0'

# セール開始時間
sale_start_time = datetime.strptime('2025-03-16 10:21:00', '%Y-%m-%d %H:%M:%S')

# ChromeOptionsの設定
options = Options()
options.add_argument('--user-data-dir=C:\\Users\\masa_\\AppData\\Local\\Google\\Chrome\\User Data')  # プロファイルの保存先ディレクトリ
options.add_argument('--profile-directory=Profile 1')  # 使用したいプロファイル名
options.add_argument('--no-sandbox')  # サンドボックスを無効化
options.add_argument('--disable-dev-shm-usage')  # /dev/shm の使用を無効化
options.add_argument('--headless')  # ヘッドレスモードで起動（必要に応じて）

# ChromeDriverのパスを指定
service = Service(ChromeDriverManager().install())

# WebDriverの起動
driver = webdriver.Chrome(service=service, options=options)

# セール開始時間まで待機
time_to_wait = (sale_start_time - datetime.now()).total_seconds()
if time_to_wait > 0:
    time.sleep(time_to_wait)

# 商品ページにアクセス
driver.get(product_url)

try:
    # カートに入れるボタンが表示されるまで待機
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'add_to_cart_button_id'))
    )
    # カートに入れるボタンをクリック
    add_to_cart_button.click()
    print('商品をカートに追加しました。')
except Exception as e:
    print(f'エラーが発生しました: {e}')
finally:
    # ブラウザを閉じる
    driver.quit()
