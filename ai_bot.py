import discord
import requests
from groq import Groq
import os

# 設定（環境変数から読み込む）
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# Groq設定
groq_client = Groq(api_key=GROQ_API_KEY)

# Discord設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} としてログインしました！")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 天気コマンド
    if message.content == "天気":
        url = "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode,relativehumidity_2m"
        response = requests.get(url)
        data = response.json()
        current = data["current"]
        temperature = current["temperature_2m"]
        humidity = current["relativehumidity_2m"]
        weather_dict = {
            0: "快晴", 1: "晴れ", 2: "曇りがち",
            3: "曇り", 45: "霧", 51: "小雨",
            61: "雨", 80: "にわか雨",
        }
        weather = weather_dict.get(current["weathercode"], "不明")
        await message.channel.send(
            f"🌤 東京の天気\n天気: {weather}\n気温: {temperature}℃\n湿度: {humidity}%"
        )

    # AI会話
    else:
        chat = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "あなたは親切な日本語アシスタントです。"},
                {"role": "user", "content": message.content}
            ],
            model="llama-3.3-70b-versatile",
        )
        await message.channel.send(chat.choices[0].message.content)

client.run(DISCORD_TOKEN)