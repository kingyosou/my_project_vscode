import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.yamada-denkiweb.com"
START_URL = "https://www.yamada-denkiweb.com/event/wes219a/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_product_links(start_url):
    """商品一覧ページから商品詳細ページのリンクを取得"""
    product_links = []
    response = requests.get(start_url, headers=HEADERS)
    
    if response.status_code != 200:
        print("ページ取得失敗:", response.status_code)
        return product_links

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.select("a[href*='/product/']"):  # 商品詳細ページのリンクを抽出
        href = link.get("href")
        if href and href.startswith("/product/"):
            product_links.append(BASE_URL + href)
    
    return list(set(product_links))  # 重複を排除

def get_jan_code(product_url):
    """商品詳細ページからJANコードを取得"""
    response = requests.get(product_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"取得失敗: {product_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    jan_code_elem = soup.find(string="JANコード")
    if jan_code_elem:
        jan_code = jan_code_elem.find_next("td").text.strip()
        return jan_code
    
    return None

def main():
    product_links = get_product_links(START_URL)
    data = []
    
    for idx, product_url in enumerate(product_links, 1):
        print(f"[{idx}/{len(product_links)}] {product_url}")
        jan_code = get_jan_code(product_url)
        if jan_code:
            data.append({"URL": product_url, "JANコード": jan_code})
        time.sleep(1)  # サーバー負荷を避けるためのスリープ
    
    df = pd.DataFrame(data)
    df.to_csv("jan_codes.csv", index=False, encoding="utf-8")
    print("JANコード取得完了！CSVに保存しました。")

if __name__ == "__main__":
    main()
