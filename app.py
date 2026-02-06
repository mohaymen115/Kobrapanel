import asyncio
import re
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from telethon import TelegramClient

# ============ CONFIG ============
API_ID = 38077264
API_HASH = "4dac72033d68a6bab7586e67edb182ae"
SESSION_NAME = "selva_session"

CHANNEL_ID = -1003808609180  # <-- غير ID القناة هنا فقط

FILTER_TEXT = "Auto-delete in 5 min"
PASSWORD = "selva1"
REFRESH = 15
# ================================

KNOWN_CODES = {
    "+20": "Egypt",
    "+1": "United States",
    "+44": "United Kingdom",
    "+58": "Venezuela",
    "+91": "India",
    "+966": "Saudi Arabia",
    "+971": "UAE",
}

app = FastAPI()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

messages = {}
ready = False


def get_country(text):
    m = re.match(r"^\+(\d{1,4})", text)
    if not m:
        return None
    code = "+" + m.group(1)
    if code not in KNOWN_CODES:
        KNOWN_CODES[code] = f"Country {code}"
    return KNOWN_CODES[code]


async def worker():
    global messages, ready
    await client.start()
    channel = await client.get_entity(CHANNEL_ID)

    while True:
        temp = {}
        msgs = await client.get_messages(channel, limit=300)
        for m in msgs:
            if not m.message:
                continue
            text = m.message.strip()
            if FILTER_TEXT not in text:
                continue
            country = get_country(text)
            if not country:
                continue
            temp.setdefault(country, []).append(text)

        messages = temp
        ready = True
        await asyncio.sleep(REFRESH)


@app.on_event("startup")
async def start():
    asyncio.create_task(worker())


@app.post("/login")
async def login(data: dict):
    return {"ok": data.get("password") == PASSWORD}


@app.get("/status")
def status():
    return {"ready": ready}


@app.get("/countries")
def countries():
    return list(messages.keys())


@app.get("/messages/{country}")
def get_msgs(country: str):
    return messages.get(country, [])


@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SELVA Massage ⚡</title>
<style>
body{margin:0;font-family:Segoe UI;background:#000;color:#fff}
#splash,#login{
position:fixed;inset:0;background:#000;
display:flex;flex-direction:column;align-items:center;justify-content:center}
#splash img{width:140px;height:140px;border-radius:50%;box-shadow:0 0 30px #00f6ff}
h1{letter-spacing:6px}
#main{display:none}
#tabs{display:flex;gap:10px;overflow-x:auto;background:#111;padding:10px}
.tab{padding:10px 18px;background:#222;border-radius:8px;cursor:pointer}
.tab:hover{background:#00f6ff;color:#000}
.msg{margin:10px;background:#111;padding:15px;border-radius:10px;
box-shadow:0 0 10px #00f6ff44}
input,button{padding:10px;border-radius:6px;border:none;font-size:16px}
button{background:#00f6ff;font-weight:bold}
</style>
</head>
<body>

<div id="splash">
<img src="https://i.ibb.co/m1jd1Hx/image.jpg">
<h1>S E L V A Massage ⚡</h1>
</div>

<div id="login" style="display:none">
<h2>🔐 Login</h2>
<input id="pass" type="password" placeholder="Password">
<label><input type="checkbox" id="remember"> Remember me</label><br><br>
<button onclick="doLogin()">Login</button>
<p id="err" style="color:red"></p>
</div>

<div id="main">
<div id="tabs"></div>
<div id="content" style="padding:10px">Loading...</div>
</div>

<script>
const WEEK = 7*24*60*60*1000;

function saved(){
 let s=localStorage.getItem("selva");
 if(!s) return false;
 s=JSON.parse(s);
 return Date.now()<s.exp;
}

setTimeout(async ()=>{
 splash.style.display="none";
 if(saved()){
  main.style.display="block";
  await wait();
  loadCountries();
 }else login.style.display="flex";
},5000);

async function wait(){
 while(true){
  let r=await fetch("/status").then(r=>r.json());
  if(r.ready) return;
  await new Promise(x=>setTimeout(x,1000));
 }
}

async function doLogin(){
 let r=await fetch("/login",{method:"POST",
 headers:{'Content-Type':'application/json'},
 body:JSON.stringify({password:pass.value})});
 let d=await r.json();
 if(!d.ok){err.innerText="Wrong password";return;}
 if(remember.checked)
 localStorage.setItem("selva",JSON.stringify({exp:Date.now()+WEEK}));
 login.style.display="none";
 main.style.display="block";
 await wait();
 loadCountries();
}

async function loadCountries(){
 let c=await fetch("/countries").then(r=>r.json());
 tabs.innerHTML=""; content.innerHTML="Choose country";
 if(!c.length){content.innerHTML="No messages";return;}
 c.forEach(x=>{
  let t=document.createElement("div");
  t.className="tab"; t.innerText=x;
  t.onclick=()=>loadMsgs(x);
  tabs.appendChild(t);
 });
}

async function loadMsgs(c){
 content.innerHTML="Loading...";
 let d=await fetch("/messages/"+encodeURIComponent(c)).then(r=>r.json());
 content.innerHTML="";
 if(!d.length){content.innerHTML="No messages";return;}
 d.forEach(m=>content.innerHTML+=`<div class="msg">${m}</div>`);
}
</script>

</body>
</html>
"""
