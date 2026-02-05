from flask import Flask, request, jsonify
from flask import render_template_string
from telethon import TelegramClient, events
import asyncio
import threading
import re

# ===== إعدادات Telethon =====
api_id = 39864754
api_hash = '254da5354e8595342d963ef27049c7'
channel_id = -1003808609180  # القناة الخاصة بك

client = TelegramClient('session', api_id, api_hash)

# ===== إعدادات Flask =====
app = Flask(__name__)
messages = []

# ===== HTML + CSS + JS في render_template_string =====
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SELVA Massage</title>
<style>
body {
    margin: 0;
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #6b73ff, #000dff);
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
    flex-direction: column;
}
#intro {
    position: absolute;
    width: 100%;
    height: 100%;
    background: #000;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 100;
}
#intro img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #fff;
}
#intro h1 {
    margin-top: 20px;
    font-size: 28px;
    letter-spacing: 5px;
    text-align: center;
}
#main {
    display: none;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 20px;
}
input, button {
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: none;
    margin: 5px;
}
button {
    background: #fff;
    color: #000;
    cursor: pointer;
    transition: 0.3s;
}
button:hover {
    background: #ff0;
    color: #000;
}
#results {
    margin-top: 20px;
    width: 90%;
    max-width: 600px;
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 10px;
    max-height: 400px;
    overflow-y: auto;
}
.msg {
    background: rgba(255,255,255,0.2);
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}
</style>
</head>
<body>

<div id="intro">
    <img src="https://i.ibb.co/m1jd1Hx/image.png" alt="SELVA Massage">
    <h1>S E L V A Massage ⚡</h1>
</div>

<div id="main">
    <div>
        <input type="text" id="last3" placeholder="ادخل اخر 3 ارقام">
        <button onclick="searchMessages()">بحث</button>
    </div>
    <div id="results"></div>
</div>

<script>
let messages = [];

setTimeout(() => {
    document.getElementById('intro').style.display = 'none';
    document.getElementById('main').style.display = 'flex';
}, 5000);

async function fetchMessages() {
    let response = await fetch('/get_messages');
    messages = await response.json();
}

setInterval(fetchMessages, 2000);

function searchMessages() {
    let last3 = document.getElementById('last3').value.trim();
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if(last3.length !== 3) {
        resultsDiv.innerHTML = '<p>ادخل اخر 3 ارقام صحيحة</p>';
        return;
    }

    let filtered = messages.filter(msg => msg.includes(last3));
    if(filtered.length === 0) {
        resultsDiv.innerHTML = '<p>لا يوجد نتائج</p>';
    } else {
        filtered.forEach(m => {
            let div = document.createElement('div');
            div.className = 'msg';
            div.textContent = m;
            resultsDiv.appendChild(div);
        });
    }
}
</script>

</body>
</html>
"""

# ===== Routes =====
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.json
    msg = data.get('message')
    if msg:
        messages.append(msg)
    return jsonify({'status': 'ok'})

# ===== Telethon Event Handler مع فلتر OTP =====
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    msg_text = event.raw_text
    # فلتر: يظهر فقط الرسائل التي تحتوي على OTP أو كود رقمي
    if 'OTP' in msg_text.upper() or re.search(r'\b\d{4,8}\b', msg_text):
        messages.append(msg_text)

# ===== تشغيل Telethon في ثريد منفصل =====
def start_telethon():
    asyncio.run(client.start())
    asyncio.run(client.run_until_disconnected())

threading.Thread(target=start_telethon).start()

# ===== تشغيل Flask =====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

