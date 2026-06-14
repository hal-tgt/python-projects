import requests

# 東京の緯度・経度
city = "大阪"
lat = 34.6937
lon = 135.5023

# APIにデータをリクエスト
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,relativehumidity_2m"

response = requests.get(url)
data = response.json()

# 必要なデータだけ取り出す
current = data["current"]

temperature = current["temperature_2m"]
humidity = current["relativehumidity_2m"]
weathercode = current["weathercode"]

# 天気コードを日本語に変換
weather_dict = {
    0: "快晴",
    1: "晴れ",
    2: "曇りがち",
    3: "曇り",
    45: "霧",
    51: "小雨",
    61: "雨",
    80: "にわか雨",
}

weather = weather_dict.get(weathercode, "不明")

# 表示
print(f"{city}の天気: {weather}")
print(f"気温: {temperature}℃")
print(f"湿度: {humidity}%")