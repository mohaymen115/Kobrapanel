import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from telethon import TelegramClient, events
import uvicorn

# ================== CONFIG ==================
API_ID = 38077264
API_HASH = "4dac72033d68a6bab7586e67edb182ae"
SESSION_NAME = "selva_session"
CHANNEL_ID = -1003808609180

PASSWORD = "selva1"
COOKIE = "auth"
COOKIE_AGE = 60 * 60 * 24 * 7

IGNORE = (
    "⚠️ Access Denied",
    "✅ Verification Successful!",
    "Welcome!",
    "Type /start",
    "You must join",
    "Please join"
)

# ================== COUNTRIES ==================
COUNTRIES = {
    "+1-876": ("Jamaica", "🇯🇲"),
    "+1-868": ("Trinidad and Tobago", "🇹🇹"),
    "+1-809": ("Dominican Republic", "🇩🇴"),
    "+1-829": ("Dominican Republic", "🇩🇴"),
    "+1-849": ("Dominican Republic", "🇩🇴"),
    "+1-246": ("Barbados", "🇧🇧"),
    "+1-284": ("British Virgin Islands", "🇻🇬"),
    "+1-345": ("Cayman Islands", "🇰🇾"),
    "+1-242": ("Bahamas", "🇧🇸"),
    "+1-441": ("Bermuda", "🇧🇲"),
    "+1-767": ("Dominica", "🇩🇲"),
    "+1-473": ("Grenada", "🇬🇩"),
    "+1-664": ("Montserrat", "🇲🇸"),
    "+1-721": ("Sint Maarten", "🇸🇽"),
    "+1-758": ("Saint Lucia", "🇱🇨"),
    "+1-784": ("Saint Vincent", "🇻🇨"),
    "+1-787": ("Puerto Rico", "🇵🇷"),
    "+1-939": ("Puerto Rico", "🇵🇷"),
    "+971": ("UAE", "🇦🇪"),
    "+966": ("Saudi Arabia", "🇸🇦"),
    "+968": ("Oman", "🇴🇲"),
    "+974": ("Qatar", "🇶🇦"),
    "+973": ("Bahrain", "🇧🇭"),
    "+965": ("Kuwait", "🇰🇼"),
    "+964": ("Iraq", "🇮🇶"),
    "+963": ("Syria", "🇸🇾"),
    "+962": ("Jordan", "🇯🇴"),
    "+961": ("Lebanon", "🇱🇧"),
    "+970": ("Palestine", "🇵🇸"),
    "+972": ("Israel", "🇮🇱"),
    "+967": ("Yemen", "🇾🇪"),
    "+98": ("Iran", "🇮🇷"),
    "+212": ("Morocco", "🇲🇦"),
    "+213": ("Algeria", "🇩🇿"),
    "+216": ("Tunisia", "🇹🇳"),
    "+20": ("Egypt", "🇪🇬"),
    "+44": ("UK", "🇬🇧"),
    "+49": ("Germany", "🇩🇪"),
    "+33": ("France", "🇫🇷"),
    "+39": ("Italy", "🇮🇹"),
    "+34": ("Spain", "🇪🇸"),
    "+7": ("Russia", "🇷🇺"),
    "+81": ("Japan", "🇯🇵"),
    "+82": ("Korea", "🇰🇷"),
    "+84": ("Vietnam", "🇻🇳"),
    "+86": ("China", "🇨🇳"),
    "+91": ("India", "🇮🇳"),
    "+92": ("Pakistan", "🇵🇰"),
    "+60": ("Malaysia", "🇲🇾"),
    "+61": ("Australia", "🇦🇺"),
    "+62": ("Indonesia", "🇮🇩"),
    "+63": ("Philippines", "🇵🇭"),
    "+65": ("Singapore", "🇸🇬"),
    "+66": ("Thailand", "🇹🇭"),
    "+880": ("Bangladesh", "🇧🇩"),
    "+1": ("USA / Canada", "🇺🇸"),
}

MESSAGES = []

app = FastAPI()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ================== HELPERS ==================
def detect_country(text):
    for c in sorted(COUNTRIES, key=len, reverse=True):
        if text.startswith(c):
            return c, COUNTRIES[c][0], COUNTRIES[c][1]
    return "OTHER", "Other", "🌍"

def process(text):
    if not text:
        return
    for x in IGNORE:
        if text.startswith(x):
            return
    code, country, flag = detect_country(text)
    MESSAGES.append({
        "text": text,
        "code": code,
        "country": country,
        "flag": flag
    })

# ================== TELETHON ==================
@app.on_event("startup")
async def start():
    asyncio.create_task(run())

async def run():
    await client.start()
    ch = await client.get_entity(CHANNEL_ID)

    async for m in client.iter_messages(ch, limit=500):
        process(m.text)

    @client.on(events.NewMessage(chats=ch))
    async def handler(e):
        process(e.raw_text)

    await client.run_until_disconnected()

# ================== AUTH ==================
def authed(req: Request):
    return req.cookies.get(COOKIE) == "1"

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
<form method="post" style="margin:100px auto;width:300px">
<input type="password" name="password" placeholder="Password" style="width:100%;padding:10px">
<br><br>
<button style="width:100%">Login</button>
</form>
"""

@app.post("/login")
def login(password: str = Form(...)):
    if password != PASSWORD:
        return RedirectResponse("/login", 302)
    r = RedirectResponse("/", 302)
    r.set_cookie(COOKIE, "1", max_age=COOKIE_AGE)
    return r

# ================== UI ==================
@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    if not authed(req):
        return RedirectResponse("/login", 302)

    return """
<!DOCTYPE html>
<html>
<body style="background:#000;color:#fff">
<div id="top"></div>
<div id="msgs"></div>

<script>
async function load(){
 let d=await fetch('/api').then(r=>r.json())
 let top=document.getElementById('top')
 let msgs=document.getElementById('msgs')
 top.innerHTML=''
 msgs.innerHTML=''

 let all=document.createElement('button')
 all.innerText='All'
 all.onclick=()=>render(d)
 top.appendChild(all)

 let map={}
 d.forEach(x=>map[x.code]=x.country+' '+x.flag)
 for(let k in map){
  let b=document.createElement('button')
  b.innerText=map[k]
  b.onclick=()=>render(d.filter(x=>x.code==k))
  top.appendChild(b)
 }

 render(d)

 function render(arr){
  msgs.innerHTML=''
  arr.forEach(m=>{
   let div=document.createElement('div')
   div.style.border='1px solid #333'
   div.style.margin='10px'
   div.style.padding='10px'
   div.innerHTML = m.text + 
   ' <button onclick="navigator.clipboard.writeText(`'+m.text+'`)">نسخ</button>'
   msgs.appendChild(div)
  })
 }
}
setInterval(load,2000)
load()
</script>
</body>
</html>
"""

# ================== API ==================
@app.get("/api")
def api():
    return MESSAGES[::-1][:300]

# ================== RUN ==================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
