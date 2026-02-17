from flask import Flask, render_template, jsonify, request
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)

# بيانات تيليجرام
api_id = 31708187
api_hash = "594b5e7b6167621388cd15a15b3db1d8"
channel_username = "selva_card"

# توكن البوت
BOT_TOKEN = "7783212048:AAFBym2E2Ro6yCiNKtc0eo-XyTc8_Qet_XQ"

bot_messages = []

async def fetch_channel_messages():
    messages_list = []
    async with TelegramClient("session", api_id, api_hash) as client:
        async for message in client.iter_messages(channel_username, limit=50):
            if message.text:
                messages_list.append({
                    "text": message.text,
                    "date": str(message.date)[:16],
                    "source": "channel"
                })
    return messages_list

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/messages")
def get_messages():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    channel_msgs = loop.run_until_complete(fetch_channel_messages())
    all_msgs = bot_messages + channel_msgs
    return jsonify(all_msgs)

# استقبال رسائل البوت
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        text = data["message"].get("text")
        if text:
            bot_messages.insert(0, {
                "text": text,
                "date": "Now",
                "source": "bot"
            })
    return "ok"

if __name__ == "__main__":
    app.run()
