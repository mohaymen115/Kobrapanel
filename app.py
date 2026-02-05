import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# ================= CONFIG =================
API_ID = 38077264            # <-- api_id
API_HASH = "4dac72033d68a6bab7586e67edb182ae"   # <-- api_hash
CHANNEL = "https://t.me/ie_zy"  # قناة انت مالكها
SESSION = "selva_session"

SITE_PASSWORD = "selvapanel"     # 🔐 باسورد الموقع
REFRESH_SECONDS = 10       # ⏱ تحديث تلقائي

FILTER_TEXT = "Auto-delete in 5 min"
# =========================================

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = TelegramClient(SESSION, API_ID, API_HASH)
messages_cache = []

# ============ TELETHON LOOP ============
async def update_messages():
    global messages_cache
    await client.start()
    channel = await client.get_entity(CHANNEL)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            limit=300,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        messages_cache = [
            m.message for m in history.messages
            if m.message and FILTER_TEXT in m.message
        ]

        await asyncio.sleep(REFRESH_SECONDS)

@app.on_event("startup")
async def startup():
    asyncio.create_task(update_messages())

# ============ AUTH ============
@app.post("/login")
async def login(password: str = Form(...)):
    return {"ok": password == SITE_PASSWORD}

# ============ SEARCH ============
@app.get("/search")
def search(last3: str):
    results = []
    for msg in messages_cache:
        if msg.strip()[-3:] == last3:
            results.append(msg)
    return {"results": results}

# ============ FRONT ============
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<title>SELVA Massage ⚡</title>
<style>
body{margin:0;font-family:Segoe UI;background:radial-gradient(circle,#111,#000);color:#fff;text-align:center}
#splash,#login{position:fixed;inset:0;background:black;display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:10}
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
document.getElementById("splash").style.display="none";
document.getElementById("login").style.display="flex";
},5000);

function login(){
fetch("/login",{method:"POST",
headers:{"Content-Type":"application/x-www-form-urlencoded"},
body:"password="+document.getElementById("pass").value})
.then(r=>r.json()).then(d=>{
if(d.ok){
loginBox.style.display="none";
main.style.display="block";
}else{err.innerText="Wrong password";}
});
}

function search(){
fetch("/search?last3="+last3.value)
.then(r=>r.json()).then(d=>{
results.innerHTML="";
if(d.results.length==0) results.innerHTML="<p>لا توجد نتائج</p>";
d.results.forEach(m=>results.innerHTML+=`<div class="msg">${m}</div>`);
});
}
</script>

</body>
</html>
"""
