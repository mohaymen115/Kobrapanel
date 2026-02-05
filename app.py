import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from telethon import TelegramClient

# ============== CONFIG ==============
API_ID = 38077264
API_HASH = "4dac72033d68a6bab7586e67edb182ae"

SESSION_NAME = "selva_session"

# 👇 ID القناة (لازم يبدأ بـ -100)
CHANNEL = -1003808609180   # عدّل هنا فقط

REFRESH_SECONDS = 15
SITE_PASSWORD = "selva1"
# ====================================

app = FastAPI()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
messages_cache = []

# ============== TELETHON LOOP ==============
async def fetch_messages():
    global messages_cache

    print("🚀 Starting Telethon...")
    await client.start()
    print("✅ Logged in")

    channel = await client.get_entity(CHANNEL)
    print("📢 Channel loaded")

    while True:
        msgs = await client.get_messages(channel, limit=100)
        messages_cache = []

        for m in msgs:
            if m.message:
                messages_cache.append(m.message)

        print("📨 Messages:", len(messages_cache))
        await asyncio.sleep(REFRESH_SECONDS)

@app.on_event("startup")
async def startup():
    asyncio.create_task(fetch_messages())

# ============== AUTH ==============
@app.post("/login")
async def login(password: str = Form(...)):
    return {"ok": password == SITE_PASSWORD}

# ============== SEARCH ==============
@app.get("/search")
def search(last3: str):
    results = []
    for msg in messages_cache:
        if len(msg.strip()) >= 3 and msg.strip()[-3:] == last3:
            results.append(msg)
    return {"results": results}

# ============== DEBUG ==============
@app.get("/debug")
def debug():
    return {
        "count": len(messages_cache),
        "sample": messages_cache[:5]
    }

# ============== FRONTEND ==============
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<title>SELVA Massage ⚡</title>
<style>
body{margin:0;font-family:Segoe UI;background:radial-gradient(circle,#111,#000);color:#fff;text-align:center}
#splash,#login{position:fixed;inset:0;background:black;display:flex;flex-direction:column;justify-content:center;align-items:center}
#splash img{width:140px;height:140px;border-radius:50%;box-shadow:0 0 30px #00f6ff}
h1{letter-spacing:6px}
#main{display:none;padding:30px}
input,button{padding:12px;border-radius:8px;border:none;font-size:16px}
button{background:#00f6ff;font-weight:bold;cursor:pointer}
.msg{background:#111;margin:15px auto;padding:15px;width:80%;border-radius:10px;box-shadow:0 0 15px #00f6ff44}
</style>
</head>

<body>

<div id="splash">
<img src="https://i.ibb.co/m1jd1Hx/image.jpg">
<h1>S E L V A Massage ⚡</h1>
</div>

<div id="login" style="display:none">
<h2>🔐 Enter Password</h2>
<input id="pass" type="password">
<br><br>
<button onclick="login()">Login</button>
<p id="err" style="color:red"></p>
</div>

<div id="main">
<input id="last3" maxlength="3" placeholder="آخر 3 أرقام">
<button onclick="search()">بحث</button>
<div id="results"></div>
</div>

<script>
setTimeout(()=>{
  splash.style.display="none";
  login.style.display="flex";
},5000);

function login(){
  fetch("/login",{method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:"password="+pass.value})
  .then(r=>r.json()).then(d=>{
    if(d.ok){
      login.style.display="none";
      main.style.display="block";
    }else{
      err.innerText="Wrong password";
    }
  });
}

function search(){
  fetch("/search?last3="+last3.value)
  .then(r=>r.json()).then(d=>{
    results.innerHTML="";
    if(d.results.length===0){
      results.innerHTML="<p>لا توجد نتائج</p>";
    }
    d.results.forEach(m=>{
      results.innerHTML+=`<div class="msg">${m}</div>`;
    });
  });
}
</script>

</body>
</html>
"""
