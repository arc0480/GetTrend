import csv
import requests
from datetime import datetime
import time

# YahooニュースのAPIまたはスクレイピング設定（ここでは仮のエンドポイントを使用）
API_ENDPOINT = "https://example.com/yahoo_news/trends"
OUTPUT_CSV = "yahoo_news_trends.csv"

def fetch_trending_news():
    # 仮のAPIリクエスト（実際にはAPIの仕様に従って変更してください）
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        # データをパース
        news_data = response.json()  # 仮のJSONレスポンス
        return [
            {
                "title": item["title"],
                "genre": item["genre"],
                "comments": item["comments"]
            }
            for item in news_data if item["comments"] >= 2000
        ]
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def append_to_csv(data):
    # ファイルが存在する場合は追記、存在しない場合は新規作成
    file_exists = False
    try:
        with open(OUTPUT_CSV, 'x', encoding='utf-8') as file:
            writer = csv.writer(file)
            # ヘッダーを書き込む
            writer.writerow(["Timestamp", "Title", "Genre", "Comments"])
    except FileExistsError:
        file_exists = True

    with open(OUTPUT_CSV, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        # データを書き込む
        for entry in data:
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), entry["title"], entry["genre"], entry["comments"]])

def main():
    while True:
        print("Fetching trending news...")
        news_data = fetch_trending_news()
        if news_data:
            append_to_csv(news_data)
        else:
            print("No data to append.")
        # 1時間待機
        print("Waiting for 1 hour...")
        time.sleep(3600)

if __name__ == "__main__":
    main()
