# app.py  (ملف واحد كامل)

import asyncio
import re
from flask import Flask, jsonify, render_template_string
from telethon import TelegramClient, events

# ================== إعدادات Telegram ==================
api_id = 39864754
api_hash = "254da5354e8595342d963ef27049c7"
channel_id = -1003808609180  # ID القناة

# ================== تهيئة Telethon ==================
client = TelegramClient("session", api_id, api_hash)

# تخزين الرسائل في الذاكرة
MESSAGES = []

# ================== واجهة HTML (مدمجة) ==================
HTML = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>SELVA Massage</title>
<style>
body{
  margin:0;font-family:Arial,sans-serif;
  background:linear-gradient(135deg,#6b73ff,#000dff);
  color:#fff;display:flex;align-items:center;justify-content:center;
  height:100vh;overflow:hidden;flex-direction:column
}
#intro{
  position:absolute;inset:0;background:#000;
  display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:10
}
#intro img{
  width:150px;height:150px;border-radius:50%;border:3px solid #fff;object-fit:cover
}
#intro h1{margin-top:20px;letter-spacing:5px}
#main{display:none;width:100%;max-width:900px;padding:20px}
.controls{display:flex;gap:10px;justify-content:center}
input,button{
  padding:10px 12px;border-radius:6px;border:none;font-size:16px
}
button{cursor:pointer;background:#fff;color:#000}
button:hover{background:#ff0}
#results{
  margin-top:20px;background:rgba(255,255,255,.12);
  border-radius:12px;padding:15px;max-height:420px;overflow:auto
}
.msg{
  background:rgba(255,255,255,.18);
  padding:10px;border-radius:8px;margin-bottom:10px
}
</style>
</head>
<body>

<div id="intro">
  <img src="https://i.ibb.co/m1jd1Hx/image.png" alt="logo"/>
  <h1>S E L V A Massage ⚡</h1>
</div>

<div id="main">
  <div class="controls">
    <input id="last3" placeholder="ادخل آخر 3 أرقام" />
    <button onclick="search()">بحث</button>
  </div>
  <div id="results"></div>
</div>

<script>
let messages = [];

setTimeout(()=>{
  document.getElementById('intro').style.display='none';
  document.getElementById('main').style.display='block';
},5000);

async function pull(){
  const r = await fetch('/get_messages');
  messages = await r.json();
}
setInterval(pull,2000);

function search(){
  const q = document.getElementById('last3').value.trim();
  const box = document.getElementById('results');
  box.innerHTML='';
  if(q.length!==3){ box.innerHTML='<p>ادخل 3 أرقام</p>'; return; }
  const res = messages.filter(m=>m.includes(q));
  if(!res.length){ box.innerHTML='<p>لا يوجد نتائج</p>'; return; }
  res.forEach(t=>{
    const d=document.createElement('div'); d.className='msg'; d.textContent=t; box.appendChild(d);
  });
}
</script>
</body>
</html>
"""

# ================== Flask ==================
app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/get_messages")
def get_messages():
    # إرجاع آخر 500 رسالة فقط لتقليل الحمل
    return jsonify(MESSAGES[-500:])

# ================== Telethon Handler ==================
@client.on(events.NewMessage(chats=channel_id))
async def on_new_message(event):
    text = event.raw_text or ""
    # فلترة عامة: رسائل تحتوي أرقام (4 إلى 8)
    if re.search(r"\b\d{4,8}\b", text):
        MESSAGES.append(text)

# ================== التشغيل ==================
async def main():
    await client.start()
    print("Telethon connected")
    # تشغيل Flask داخل نفس الـ event loop بطريقة آمنة
    from werkzeug.serving import run_simple
    await asyncio.to_thread(run_simple, "0.0.0.0", 8000, app, use_reloader=False)

if __name__ == "__main__":
    asyncio.run(main())
