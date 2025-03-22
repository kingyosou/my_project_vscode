import requests
import pandas as pd
import time
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# 楽天APIの設定
RAKUTEN_APP_ID = "1031766687290699191"
RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
MAX_ITEMS = 20  # 取得する最大件数
HITS_PER_PAGE = 10  # 1回のリクエストで取得する件数（最大30）
KEY_WORDS = "シャープ 日立"  # OR検索（複数キーワード対応）

# ヘッダー設定
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Seleniumの設定
options = Options()
options.add_argument("--headless")  # ヘッドレスモード（画面を開かずに動作）
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# WebDriverのセットアップ
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 楽天APIから商品を取得する関数
def get_rakuten_deal_items():
    items = []
    print(f"📦 楽天APIから商品を取得中...")

    total_pages = math.ceil(MAX_ITEMS / HITS_PER_PAGE)  # 切り上げ計算でページ数を求める

    for page in range(1, total_pages + 1):  # 1ページ目から順に取得
        print(f"📄 ページ {page} を取得中...")

        params = {
            "format": "json",
            "applicationId": RAKUTEN_APP_ID,
            "hits": HITS_PER_PAGE,  # 1ページあたりの取得件数
            "sort": "standard",  
            "page": page,  # ページ番号を設定
            "keyword": KEY_WORDS,  
            "itemCondition": 1,  
            "orFlag": 1, # 0:AND検索 1:OR検索
            "shopCode": "superdeal",
            "availability": 1,
            "field": 1, # 0：多くの検索結果 1：限定された結果
        }

        response = requests.get(RAKUTEN_API_URL, params=params)
        if response.status_code != 200:
            print(f"❌ APIリクエスト失敗: {response.status_code}")
            print("エラーメッセージ:", response.text)
            continue

        data = response.json()
        if not data.get("Items"):
            print("⚠ データが空です。")
            break

        # 商品情報をリストに追加
        for item in data["Items"]:
            item_info = item["Item"]
            item_name = item_info.get("itemName", "N/A")

            items.append({
                "itemName": item_name,
                "catchcopy": item_info.get("catchcopy", "N/A"),
                "itemCode": item_info.get("itemCode", "N/A"),
                "itemPrice": item_info.get("itemPrice", "N/A"),
                "itemUrl": item_info.get("itemUrl", "N/A"),
                "shop_name": item_info.get("shopName", "N/A"),
                "availability": item_info.get("availability", "N/A"),
                "taxFlag": item_info.get("taxFlag", "N/A"),
                "postageFlag": item_info.get("postageFlag", "N/A"),
                "pointRate": item_info.get("pointRate", "N/A"),
                "pointRateStartTime": item_info.get("pointRateStartTime", "N/A"),
                "pointRateEndTime": item_info.get("pointRateEndTime", "N/A"),
                "genreId": item_info.get("genreId", "N/A"),
            })

    return items

# 楽天の商品ページからポイント還元情報の`ul`要素を取得する関数
def get_point_summary_block(itemUrl):
    print(f"🔍 {itemUrl} のポイント情報を取得中...")
    try:
        driver.get(itemUrl)
        time.sleep(1)  # JavaScriptが実行されるのを待つ

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # `ul.point-summary` のブロック全体を取得
        point_element = soup.select_one("ul[class*=point-summary]")
        if point_element:
            return point_element.text.strip()  # HTML全体ではなく、テキストのみ取得

        return "N/A"

    except Exception as e:
        print(f"⚠ スクレイピング失敗: {itemUrl} - {str(e)}")
        return "N/A"

# メイン処理
def main():
    rakuten_items = get_rakuten_deal_items()
    if not rakuten_items:
        print("❌ 商品データが取得できませんでした。")
        return
    
    df = pd.DataFrame(rakuten_items)

    # 各商品のポイント還元情報のブロックをスクレイピングして追加
    print("🔍 各商品のポイント還元情報ブロックを取得中...")
    df["point_summary_block"] = df["itemUrl"].apply(get_point_summary_block)

    # CSVに保存
    output_path = r"C:\Users\masa_\python\rakuten_dealshop_items.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ データを保存しました: {output_path}")

    # 取得したデータの上位5件を表示
    print("\n📊 取得したデータ（上位5件）:")
    print(df.head())

if __name__ == "__main__":
    main()

    # WebDriverを閉じる
    driver.quit()
