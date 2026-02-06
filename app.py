import os
import asyncio
import time
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from telethon import TelegramClient, events
import uvicorn

# ================== TELETHON CONFIG ==================
API_ID = 38077264
API_HASH = "4dac72033d68a6bab7586e67edb182ae"
SESSION_NAME = "selva_session"
CHANNEL_ID = -1003808609180

# ================== AUTH ==================
PASSWORD = "selva1"
COOKIE_NAME = "selva_auth"
COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days

# ================== FILTERS ==================
IGNORE_PREFIXES = (
    "⚠️ Access Denied",
    "✅ Verification Successful!",
    "Hey there"
)

# ================== COUNTRIES (Dial codes) ==================
COUNTRIES ={
    "+20": ("Egypt", "🇪🇬"),
    "+1": ("United States", "🇺🇸"),
    "+44": ("United Kingdom", "🇬🇧"),
    "+33": ("France", "🇫🇷"),
    "+49": ("Germany", "🇩🇪"),
    "+39": ("Italy", "🇮🇹"),
    "+34": ("Spain", "🇪🇸"),
    "+7": ("Russia", "🇷🇺"),
    "+81": ("Japan", "🇯🇵"),
    "+82": ("South Korea", "🇰🇷"),
    "+86": ("China", "🇨🇳"),
    "+91": ("India", "🇮🇳"),
    "+55": ("Brazil", "🇧🇷"),
    "+52": ("Mexico", "🇲🇽"),
    "+90": ("Turkey", "🇹🇷"),
    "+31": ("Netherlands", "🇳🇱"),
    "+41": ("Switzerland", "🇨🇭"),
    "+46": ("Sweden", "🇸🇪"),
    "+47": ("Norway", "🇳🇴"),
    "+45": ("Denmark", "🇩🇰"),
    "+358": ("Finland", "🇫🇮"),
    "+32": ("Belgium", "🇧🇪"),
    "+43": ("Austria", "🇦🇹"),
    "+353": ("Ireland", "🇮🇪"),
    "+351": ("Portugal", "🇵🇹"),
    "+30": ("Greece", "🇬🇷"),
    "+48": ("Poland", "🇵🇱"),
    "+420": ("Czech Republic", "🇨🇿"),
    "+36": ("Hungary", "🇭🇺"),
    "+40": ("Romania", "🇷🇴"),
    "+380": ("Ukraine", "🇺🇦"),
    "+375": ("Belarus", "🇧🇾"),
    "+60": ("Malaysia", "🇲🇾"),
    "+62": ("Indonesia", "🇮🇩"),
    "+63": ("Philippines", "🇵🇭"),
    "+84": ("Vietnam", "🇻🇳"),
    "+66": ("Thailand", "🇹🇭"),
    "+65": ("Singapore", "🇸🇬"),
    "+971": ("United Arab Emirates", "🇦🇪"),
    "+966": ("Saudi Arabia", "🇸🇦"),
    "+20": ("Egypt", "🇪🇬"),
    "+212": ("Morocco", "🇲🇦"),
    "+213": ("Algeria", "🇩🇿"),
    "+216": ("Tunisia", "🇹🇳"),
    "+961": ("Lebanon", "🇱🇧"),
    "+962": ("Jordan", "🇯🇴"),
    "+963": ("Syria", "🇸🇾"),
    "+964": ("Iraq", "🇮🇶"),
    "+965": ("Kuwait", "🇰🇼"),
    "+966": ("Saudi Arabia", "🇸🇦"),
    "+968": ("Oman", "🇴🇲"),
    "+974": ("Qatar", "🇶🇦"),
    "+973": ("Bahrain", "🇧🇭"),
    "+967": ("Yemen", "🇾🇪"),
    "+249": ("Sudan", "🇸🇩"),
    "+251": ("Ethiopia", "🇪🇹"),
    "+254": ("Kenya", "🇰🇪"),
    "+234": ("Nigeria", "🇳🇬"),
    "+27": ("South Africa", "🇿🇦"),
    "+233": ("Ghana", "🇬🇭"),
    "+225": ("Ivory Coast", "🇨🇮"),
    "+241": ("Gabon", "🇬🇦"),
    "+237": ("Cameroon", "🇨🇲"),
    "+236": ("Central African Republic", "🇨🇫"),
    "+235": ("Chad", "🇹🇩"),
    "+243": ("DR Congo", "🇨🇩"),
    "+242": ("Republic of the Congo", "🇨🇬"),
    "+257": ("Burundi", "🇧🇮"),
    "+250": ("Rwanda", "🇷🇼"),
    "+255": ("Tanzania", "🇹🇿"),
    "+256": ("Uganda", "🇺🇬"),
    "+260": ("Zambia", "🇿🇲"),
    "+263": ("Zimbabwe", "🇿🇼"),
    "+267": ("Botswana", "🇧🇼"),
    "+264": ("Namibia", "🇳🇦"),
    "+258": ("Mozambique", "🇲🇿"),
    "+261": ("Madagascar", "🇲🇬"),
    "+230": ("Mauritius", "🇲🇺"),
    "+248": ("Seychelles", "🇸🇨"),
    "+269": ("Comoros", "🇰🇲"),
    "+252": ("Somalia", "🇸🇴"),
    "+253": ("Djibouti", "🇩🇯"),
    "+291": ("Eritrea", "🇪🇷"),
    "+598": ("Uruguay", "🇺🇾"),
    "+595": ("Paraguay", "🇵🇾"),
    "+56": ("Chile", "🇨🇱"),
    "+51": ("Peru", "🇵🇪"),
    "+57": ("Colombia", "🇨🇴"),
    "+58": ("Venezuela", "🇻🇪"),
    "+593": ("Ecuador", "🇪🇨"),
    "+591": ("Bolivia", "🇧🇴"),
    "+54": ("Argentina", "🇦🇷"),
    "+506": ("Costa Rica", "🇨🇷"),
    "+507": ("Panama", "🇵🇦"),
    "+502": ("Guatemala", "🇬🇹"),
    "+503": ("El Salvador", "🇸🇻"),
    "+504": ("Honduras", "🇭🇳"),
    "+505": ("Nicaragua", "🇳🇮"),
    "+509": ("Haiti", "🇭🇹"),
    "+1-876": ("Jamaica", "🇯🇲"),
    "+1-868": ("Trinidad and Tobago", "🇹🇹"),
    "+1-767": ("Dominica", "🇩🇲"),
    "+1-809": ("Dominican Republic", "🇩🇴"),
    "+1-242": ("Bahamas", "🇧🇸"),
    "+1-246": ("Barbados", "🇧🇧"),
    "+1-284": ("British Virgin Islands", "🇻🇬"),
    "+1-345": ("Cayman Islands", "🇰🇾"),
    "+61": ("Australia", "🇦🇺"),
    "+64": ("New Zealand", "🇳🇿"),
    "+679": ("Fiji", "🇫🇯"),
    "+675": ("Papua New Guinea", "🇵🇬"),
    "+677": ("Solomon Islands", "🇸🇧"),
    "+682": ("Cook Islands", "🇨🇰"),
    "+685": ("Samoa", "🇼🇸"),
    "+686": ("Kiribati", "🇰🇮"),
    "+687": ("New Caledonia", "🇳🇨"),
    "+689": ("French Polynesia", "🇵🇫"),
    "+850": ("North Korea", "🇰🇵"),
    "+92": ("Pakistan", "🇵🇰"),
    "+93": ("Afghanistan", "🇦🇫"),
    "+94": ("Sri Lanka", "🇱🇰"),
    "+95": ("Myanmar", "🇲🇲"),
    "+98": ("Iran", "🇮🇷"),
    "+960": ("Maldives", "🇲🇻"),
    "+961": ("Lebanon", "🇱🇧"),
    "+962": ("Jordan", "🇯🇴"),
    "+963": ("Syria", "🇸🇾"),
    "+964": ("Iraq", "🇮🇶"),
    "+965": ("Kuwait", "🇰🇼"),
    "+966": ("Saudi Arabia", "🇸🇦"),
    "+967": ("Yemen", "🇾🇪"),
    "+968": ("Oman", "🇴🇲"),
    "+970": ("Palestine", "🇵🇸"),
    "+972": ("Israel", "🇮🇱"),
    "+973": ("Bahrain", "🇧🇭"),
    "+974": ("Qatar", "🇶🇦"),
    "+975": ("Bhutan", "🇧🇹"),
    "+976": ("Mongolia", "🇲🇳"),
    "+977": ("Nepal", "🇳🇵"),
    "+992": ("Tajikistan", "🇹🇯"),
    "+993": ("Turkmenistan", "🇹🇲"),
    "+994": ("Azerbaijan", "🇦🇿"),
    "+995": ("Georgia", "🇬🇪"),
    "+996": ("Kyrgyzstan", "🇰🇬"),
    "+998": ("Uzbekistan", "🇺🇿"),
    "+376": ("Andorra", "🇦🇩"),
    "+355": ("Albania", "🇦🇱"),
    "+374": ("Armenia", "🇦🇲"),
    "+387": ("Bosnia and Herzegovina", "🇧🇦"),
    "+359": ("Bulgaria", "🇧🇬"),
    "+385": ("Croatia", "🇭🇷"),
    "+357": ("Cyprus", "🇨🇾"),
    "+372": ("Estonia", "🇪🇪"),
    "+298": ("Faroe Islands", "🇫🇴"),
    "+995": ("Georgia", "🇬🇪"),
    "+350": ("Gibraltar", "🇬🇮"),
    "+299": ("Greenland", "🇬🇱"),
    "+354": ("Iceland", "🇮🇸"),
    "+353": ("Ireland", "🇮🇪"),
    "+370": ("Lithuania", "🇱🇹"),
    "+352": ("Luxembourg", "🇱🇺"),
    "+356": ("Malta", "🇲🇹"),
    "+373": ("Moldova", "🇲🇩"),
    "+377": ("Monaco", "🇲🇨"),
    "+382": ("Montenegro", "🇲🇪"),
    "+389": ("North Macedonia", "🇲🇰"),
    "+47": ("Norway", "🇳🇴"),
    "+378": ("San Marino", "🇸🇲"),
    "+381": ("Serbia", "🇷🇸"),
    "+421": ("Slovakia", "🇸🇰"),
    "+386": ("Slovenia", "🇸🇮"),
    "+46": ("Sweden", "🇸🇪"),
    "+41": ("Switzerland", "🇨🇭"),
    "+90": ("Turkey", "🇹🇷"),
    "+380": ("Ukraine", "🇺🇦"),
    "+39": ("Vatican City", "🇻🇦"),
    "+58": ("Venezuela", "🇻🇪"),
}

MESSAGES = []

# ================== APP ==================
app = FastAPI()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def detect_country(text):
    for code, (name, flag) in COUNTRIES.items():
        if text.strip().startswith(code):
            return code, name, flag
    return None, "Unknown", "🌍"

# ================== TELETHON START ==================
@app.on_event("startup")
async def startup():
    asyncio.create_task(start_telethon())

async def start_telethon():
    await client.start()
    channel = await client.get_entity(CHANNEL_ID)

    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        text = event.raw_text or ""

        for p in IGNORE_PREFIXES:
            if text.startswith(p):
                return

        code, country, flag = detect_country(text)

        MESSAGES.append({
            "text": text,
            "code": code,
            "country": country,
            "flag": flag
        })

    await client.run_until_disconnected()

# ================== AUTH CHECK ==================
def is_authed(request: Request):
    return request.cookies.get(COOKIE_NAME) == "1"

# ================== LOGIN ==================
@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body{background:#0f0f0f;color:#fff;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh}
.box{background:#1a1a1a;padding:30px;border-radius:12px;width:300px}
input,button{width:100%;padding:10px;margin-top:10px;border-radius:8px;border:none}
button{background:#6c63ff;color:white;font-weight:bold}
label{font-size:14px}
</style>
</head>
<body>
<form class="box" method="post">
<h2>Selva Panel</h2>
<input type="password" name="password" placeholder="Password" required>
<label><input type="checkbox" name="remember"> Remember me</label>
<button type="submit">Login</button>
</form>
</body>
</html>
"""

@app.post("/login")
def login(password: str = Form(...), remember: str = Form(None)):
    if password != PASSWORD:
        return RedirectResponse("/login", status_code=302)

    res = RedirectResponse("/", status_code=302)
    if remember:
        res.set_cookie(COOKIE_NAME, "1", max_age=COOKIE_AGE)
    else:
        res.set_cookie(COOKIE_NAME, "1")
    return res

# ================== MAIN UI ==================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not is_authed(request):
        return RedirectResponse("/login", status_code=302)

    return """
<!DOCTYPE html>
<html>
<head>
<title>Selva Massage</title>
<style>
body{margin:0;background:#0b0b0b;color:#fff;font-family:sans-serif}
#splash{position:fixed;inset:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:10}
#splash img{width:140px;height:140px;border-radius:50%}
#top{padding:15px;border-bottom:1px solid #222;display:flex;gap:15px;overflow-x:auto}
.country{cursor:pointer;white-space:nowrap}
.msg{background:#151515;margin:10px;padding:12px;border-radius:10px}
.hidden{display:none}
</style>
</head>
<body>

<div id="splash">
<img src="https://i.ibb.co/m1jd1Hx/image.jpg">
<h2>selva massage ⚡</h2>
</div>

<div id="top"></div>
<div id="messages"></div>

<script>
setTimeout(()=>document.getElementById("splash").style.display="none",5000)

fetch("/api/messages").then(r=>r.json()).then(data=>{
  const top=document.getElementById("top")
  const msgs=document.getElementById("messages")
  const countries={}

  data.forEach(m=>{
    if(m.code){
      countries[m.code]=m.country+" "+m.flag
    }
  })

  for(const c in countries){
    const d=document.createElement("div")
    d.className="country"
    d.innerText=countries[c]
    d.onclick=()=>show(c)
    top.appendChild(d)
  }

  window.show=(code)=>{
    msgs.innerHTML=""
    data.filter(m=>m.code==code).forEach(m=>{
      const div=document.createElement("div")
      div.className="msg"
      div.innerText=m.text
      msgs.appendChild(div)
    })
  }
})
</script>
</body>
</html>
"""

# ================== API ==================
@app.get("/api/messages")
def api_messages():
    return MESSAGES[-500:]

# ================== RUN ==================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
