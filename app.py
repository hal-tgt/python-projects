from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>天気予報アプリ</title>
        <style>
            body {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #74b9ff, #0984e3);
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                width: 300px;
            }
            h1 {
                color: #0984e3;
                font-size: 24px;
            }
            input {
                width: 90%;
                padding: 12px;
                border: 2px solid #74b9ff;
                border-radius: 10px;
                font-size: 16px;
                margin-bottom: 15px;
            }
            button {
                background: #0984e3;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background: #74b9ff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌤️ 天気予報アプリ</h1>
            <form action="/weather" method="get">
                <input type="text" name="city" placeholder="都市名を入力">
                <br>
                <button type="submit">検索</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route("/weather")
def weather():
    city = request.args.get("city", "東京")

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ja"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data:
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1>「{city}」が見つかりませんでした</h1>
            <a href="/">戻る</a>
        </div>
        """

    result = geo_data["results"][0]
    lat = result["latitude"]
    lon = result["longitude"]
    found_name = result["name"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,relativehumidity_2m"
    response = requests.get(url)
    data = response.json()

    if "current" not in data:
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h1>天気情報の取得に失敗しました</h1>
            <p>エラー: {data}</p>
            <a href="/">戻る</a>
        </div>
        """
    
    current = data["current"]
    temperature = current["temperature_2m"]
    humidity = current["relativehumidity_2m"]

    weather_dict = {
        0: "快晴", 1: "晴れ", 2: "曇りがち",
        3: "曇り", 45: "霧", 51: "小雨",
        61: "雨", 80: "にわか雨",
    }
    weather = weather_dict.get(current["weathercode"], "不明")

    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>{found_name}の天気</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #74b9ff, #0984e3);
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                width: 300px;
            }}
            h1 {{
                color: #0984e3;
                font-size: 22px;
            }}
            p {{
                font-size: 18px;
                color: #2d3436;
                margin: 10px 0;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                color: #0984e3;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📍 {found_name}</h1>
            <p>☁️ {weather}</p>
            <p>🌡️ {temperature}℃</p>
            <p>💧 湿度 {humidity}%</p>
            <a href="/">← 戻る</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
