import requests
from bs4 import BeautifulSoup
import pandas as pd

# サイトからデータを取得
url = "http://books.toscrape.com/"
response = requests.get(url)
response.encoding = "utf-8"

# HTMLを解析
soup = BeautifulSoup(response.text, "html.parser")

# 本のタイトルと価格を取得
books = soup.find_all("article", class_="product_pod")

# データを入れるリスト
data = []

for book in books:
    title = book.find("h3").find("a")["title"]
    price = book.find("p", class_="price_color").text
    data.append({"タイトル": title, "価格": price})

# DataFrameに変換
df = pd.DataFrame(data)

# 表示
print(df)

# Excelに保存
df.to_excel("books.xlsx", index=False)
print("Excelに保存しました！")