import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from telethon import TelegramClient, events
import uvicorn

# ================== CONFIG ==================
API_ID = 30828166
API_HASH = "272132c1323a4bb1fd6994d8d51977cf"
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
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif}
#top{display:flex;gap:10px;overflow-x:auto;padding:10px;border-bottom:1px solid #222}
.btn{padding:8px 14px;background:#1a1a1a;border-radius:20px;cursor:pointer;white-space:nowrap}
.msg{background:#151515;margin:15px;padding:20px;border-radius:12px;font-size:16px;line-height:1.5}
.copy-btn{background:#333;color:#fff;border:none;padding:6px 10px;border-radius:6px;cursor:pointer;margin-left:10px}
</style>
</head>
<body>
<div id="top"></div>
<div id="msgs"></div>

<script>
let lastCount=0
async function update(){
    const data=await fetch('/api').then(r=>r.json())
    const msgs=document.getElementById('msgs')
    const top=document.getElementById('top')

    // تحديث الشريط العلوي
    top.innerHTML=''
    const all=document.createElement('div')
    all.className='btn'
    all.innerText='All'
    all.onclick=()=>renderMessages(data)
    top.appendChild(all)

    const map={}
    data.forEach(m=>map[m.code]=m.country+' '+m.flag)
    for(const c in map){
        const b=document.createElement('div')
        b.className='btn'
        b.innerText=map[c]
        b.onclick=()=>renderMessages(data.filter(x=>x.code===c))
        top.appendChild(b)
    }

    // فقط الرسائل الجديدة
    if(data.length>lastCount){
        renderMessages(data.slice(lastCount))
        lastCount=data.length
    }
}

function renderMessages(arr){
    const msgs=document.getElementById('msgs')
    arr.forEach(m=>{
        const d=document.createElement('div')
        d.className='msg'
        d.innerHTML = `<span>${m.text}</span> <button class="copy-btn" onclick="navigator.clipboard.writeText(\`${m.text}\`)">نسخ</button>`
        msgs.appendChild(d)
    })
}

setInterval(update,2000)
update()
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
