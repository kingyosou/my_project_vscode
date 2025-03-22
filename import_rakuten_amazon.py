import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re

# 入力・出力ファイル
INPUT_FILE = r"C:\Users\masa_\python\sedori\products.txt"   # 製品リスト（1行1製品）
OUTPUT_FILE = r"C:\Users\masa_\python\sedori\results.txt"   # 検索結果の保存ファイル

def get_search_results(product_name):
    """Google検索でAmazonと楽天のURLを取得"""
    query_amazon = f"{product_name} 価格 site:amazon.co.jp"
    query_rakuten = f"{product_name} 価格 site:rakuten.co.jp"

    amazon_url, rakuten_url = None, None

    # Google検索で最適なURLを取得
    for url in search(query_amazon, num_results=5):
        if "amazon.co.jp" in url:
            amazon_url = url
            break

    for url in search(query_rakuten, num_results=5):
        if "rakuten.co.jp" in url:
            rakuten_url = url
            break

    return amazon_url, rakuten_url

def get_price(url):
    """指定URLのページから価格を取得（簡易版）"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 価格情報の抽出
        price_patterns = [r"¥\d{1,3}(,\d{3})*"]
        for pattern in price_patterns:
            match = re.search(pattern, soup.text)
            if match:
                return match.group()
    except Exception as e:
        return f"取得失敗 ({str(e)})"
    return "価格情報なし"

def process_products():
    """ファイルから製品名を読み込み、価格情報を取得して保存"""
    with open(INPUT_FILE, "r", encoding="utf-8") as infile, open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for line in infile:
            product_name = line.strip()
            if not product_name:
                continue

            print(f"🔍 検索中: {product_name}...")
            amazon_url, rakuten_url = get_search_results(product_name)

            amazon_price = get_price(amazon_url) if amazon_url else "URLなし"
            rakuten_price = get_price(rakuten_url) if rakuten_url else "URLなし"

            # 結果をテキストファイルに保存
            result = (
                f"\n【{product_name}】\n"
                f"Amazon: {amazon_price} ({amazon_url})\n"
                f"楽天市場: {rakuten_price} ({rakuten_url})\n"
            )
            print(result)
            outfile.write(result)

    print(f"\n✅ 検索結果を {OUTPUT_FILE} に保存しました。")

# 実行
process_products()
