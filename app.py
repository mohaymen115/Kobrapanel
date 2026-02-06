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
    "Hey there"
)

# ================== COUNTRIES (ORDERED: longest -> shortest) ==================
COUNTRIES = {
    # NANP (specific first)
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
    "+1-784": ("Saint Vincent and the Grenadines", "🇻🇨"),
    "+1-787": ("Puerto Rico", "🇵🇷"),
    "+1-939": ("Puerto Rico", "🇵🇷"),

    # Middle East
    "+971": ("United Arab Emirates", "🇦🇪"),
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
    "+98":  ("Iran", "🇮🇷"),

    # Africa
    "+212": ("Morocco", "🇲🇦"),
    "+213": ("Algeria", "🇩🇿"),
    "+216": ("Tunisia", "🇹🇳"),
    "+20":  ("Egypt", "🇪🇬"),
    "+249": ("Sudan", "🇸🇩"),
    "+251": ("Ethiopia", "🇪🇹"),
    "+252": ("Somalia", "🇸🇴"),
    "+253": ("Djibouti", "🇩🇯"),
    "+254": ("Kenya", "🇰🇪"),
    "+255": ("Tanzania", "🇹🇿"),
    "+256": ("Uganda", "🇺🇬"),
    "+257": ("Burundi", "🇧🇮"),
    "+258": ("Mozambique", "🇲🇿"),
    "+260": ("Zambia", "🇿🇲"),
    "+261": ("Madagascar", "🇲🇬"),
    "+262": ("Reunion", "🇷🇪"),
    "+263": ("Zimbabwe", "🇿🇼"),
    "+264": ("Namibia", "🇳🇦"),
    "+265": ("Malawi", "🇲🇼"),
    "+266": ("Lesotho", "🇱🇸"),
    "+267": ("Botswana", "🇧🇼"),
    "+268": ("Eswatini", "🇸🇿"),
    "+269": ("Comoros", "🇰🇲"),
    "+27":  ("South Africa", "🇿🇦"),
    "+233": ("Ghana", "🇬🇭"),
    "+234": ("Nigeria", "🇳🇬"),
    "+235": ("Chad", "🇹🇩"),
    "+236": ("Central African Republic", "🇨🇫"),
    "+237": ("Cameroon", "🇨🇲"),
    "+238": ("Cape Verde", "🇨🇻"),
    "+239": ("Sao Tome and Principe", "🇸🇹"),
    "+240": ("Equatorial Guinea", "🇬🇶"),
    "+241": ("Gabon", "🇬🇦"),
    "+242": ("Republic of the Congo", "🇨🇬"),
    "+243": ("DR Congo", "🇨🇩"),
    "+244": ("Angola", "🇦🇴"),
    "+245": ("Guinea-Bissau", "🇬🇼"),
    "+246": ("Diego Garcia", "🇮🇴"),
    "+247": ("Ascension", "🇦🇨"),
    "+248": ("Seychelles", "🇸🇨"),

    # Europe
    "+44":  ("United Kingdom", "🇬🇧"),
    "+49":  ("Germany", "🇩🇪"),
    "+33":  ("France", "🇫🇷"),
    "+39":  ("Italy", "🇮🇹"),
    "+34":  ("Spain", "🇪🇸"),
    "+351": ("Portugal", "🇵🇹"),
    "+353": ("Ireland", "🇮🇪"),
    "+354": ("Iceland", "🇮🇸"),
    "+355": ("Albania", "🇦🇱"),
    "+356": ("Malta", "🇲🇹"),
    "+357": ("Cyprus", "🇨🇾"),
    "+358": ("Finland", "🇫🇮"),
    "+359": ("Bulgaria", "🇧🇬"),
    "+36":  ("Hungary", "🇭🇺"),
    "+370": ("Lithuania", "🇱🇹"),
    "+371": ("Latvia", "🇱🇻"),
    "+372": ("Estonia", "🇪🇪"),
    "+373": ("Moldova", "🇲🇩"),
    "+374": ("Armenia", "🇦🇲"),
    "+375": ("Belarus", "🇧🇾"),
    "+376": ("Andorra", "🇦🇩"),
    "+377": ("Monaco", "🇲🇨"),
    "+378": ("San Marino", "🇸🇲"),
    "+380": ("Ukraine", "🇺🇦"),
    "+381": ("Serbia", "🇷🇸"),
    "+382": ("Montenegro", "🇲🇪"),
    "+383": ("Kosovo", "🇽🇰"),
    "+385": ("Croatia", "🇭🇷"),
    "+386": ("Slovenia", "🇸🇮"),
    "+387": ("Bosnia and Herzegovina", "🇧🇦"),
    "+389": ("North Macedonia", "🇲🇰"),
    "+40":  ("Romania", "🇷🇴"),
    "+41":  ("Switzerland", "🇨🇭"),
    "+420": ("Czech Republic", "🇨🇿"),
    "+421": ("Slovakia", "🇸🇰"),
    "+43":  ("Austria", "🇦🇹"),
    "+45":  ("Denmark", "🇩🇰"),
    "+46":  ("Sweden", "🇸🇪"),
    "+47":  ("Norway", "🇳🇴"),
    "+48":  ("Poland", "🇵🇱"),
    "+90":  ("Turkey", "🇹🇷"),

    # Asia
    "+7":   ("Russia / Kazakhstan", "🇷🇺"),
    "+81":  ("Japan", "🇯🇵"),
    "+82":  ("South Korea", "🇰🇷"),
    "+84":  ("Vietnam", "🇻🇳"),
    "+86":  ("China", "🇨🇳"),
    "+91":  ("India", "🇮🇳"),
    "+92":  ("Pakistan", "🇵🇰"),
    "+93":  ("Afghanistan", "🇦🇫"),
    "+94":  ("Sri Lanka", "🇱🇰"),
    "+95":  ("Myanmar", "🇲🇲"),
    "+60":  ("Malaysia", "🇲🇾"),
    "+61":  ("Australia", "🇦🇺"),
    "+62":  ("Indonesia", "🇮🇩"),
    "+63":  ("Philippines", "🇵🇭"),
    "+64":  ("New Zealand", "🇳🇿"),
    "+65":  ("Singapore", "🇸🇬"),
    "+66":  ("Thailand", "🇹🇭"),
    "+880": ("Bangladesh", "🇧🇩"),
    "+886": ("Taiwan", "🇹🇼"),
    "+960": ("Maldives", "🇲🇻"),
    "+975": ("Bhutan", "🇧🇹"),
    "+976": ("Mongolia", "🇲🇳"),
    "+977": ("Nepal", "🇳🇵"),
    "+992": ("Tajikistan", "🇹🇯"),
    "+993": ("Turkmenistan", "🇹🇲"),
    "+994": ("Azerbaijan", "🇦🇿"),
    "+995": ("Georgia", "🇬🇪"),
    "+996": ("Kyrgyzstan", "🇰🇬"),
    "+998": ("Uzbekistan", "🇺🇿"),

    # Americas
    "+52":  ("Mexico", "🇲🇽"),
    "+54":  ("Argentina", "🇦🇷"),
    "+55":  ("Brazil", "🇧🇷"),
    "+56":  ("Chile", "🇨🇱"),
    "+57":  ("Colombia", "🇨🇴"),
    "+58":  ("Venezuela", "🇻🇪"),
    "+591": ("Bolivia", "🇧🇴"),
    "+593": ("Ecuador", "🇪🇨"),
    "+595": ("Paraguay", "🇵🇾"),
    "+598": ("Uruguay", "🇺🇾"),
    "+502": ("Guatemala", "🇬🇹"),
    "+503": ("El Salvador", "🇸🇻"),
    "+504": ("Honduras", "🇭🇳"),
    "+505": ("Nicaragua", "🇳🇮"),
    "+506": ("Costa Rica", "🇨🇷"),
    "+507": ("Panama", "🇵🇦"),
    "+509": ("Haiti", "🇭🇹"),

    # Generic NANP last
    "+1":   ("USA / Canada", "🇺🇸"),
}

MESSAGES = []

app = FastAPI()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ================== HELPERS ==================
def detect_country(text: str):
    for code in sorted(COUNTRIES, key=len, reverse=True):
        if text.startswith(code):
            name, flag = COUNTRIES[code]
            return code, name, flag
    return "OTHER", "Other", "🌍"

def process(text: str):
    if not text:
        return
    for p in IGNORE:
        if text.startswith(p):
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
async def startup():
    asyncio.create_task(run_telethon())

async def run_telethon():
    await client.start()
    ch = await client.get_entity(CHANNEL_ID)

    # load old
    async for m in client.iter_messages(ch, limit=500):
        process(m.text)

    # listen new
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
<body style="background:#000;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh">
<form method="post" style="background:#111;padding:30px;border-radius:12px">
<h3>Selva Login</h3>
<input type="password" name="password" placeholder="Password" style="width:100%;padding:10px"><br><br>
<label><input type="checkbox" name="remember"> Remember me</label><br><br>
<button style="width:100%">Login</button>
</form>
</body>
"""

@app.post("/login")
def login(password: str = Form(...), remember: str = Form(None)):
    if password != PASSWORD:
        return RedirectResponse("/login", 302)
    r = RedirectResponse("/", 302)
    r.set_cookie(COOKIE, "1", max_age=COOKIE_AGE if remember else None)
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
body{margin:0;background:#0b0b0b;color:#fff;font-family:sans-serif}
#top{display:flex;gap:10px;overflow-x:auto;padding:10px;border-bottom:1px solid #222}
.btn{padding:8px 14px;background:#1a1a1a;border-radius:20px;cursor:pointer;white-space:nowrap}
.msg{background:#151515;margin:10px;padding:12px;border-radius:10px}
</style>
</head>
<body>

<div id="top"></div>
<div id="messages"></div>

<script>
fetch("/api").then(r=>r.json()).then(data=>{
 const top=document.getElementById("top")
 const msgs=document.getElementById("messages")

 function render(arr){
   msgs.innerHTML=""
   arr.forEach(m=>{
     const d=document.createElement("div")
     d.className="msg"
     d.innerText=m.text
     msgs.appendChild(d)
   })
 }

 const all=document.createElement("div")
 all.className="btn"
 all.innerText="All"
 all.onclick=()=>render(data)
 top.appendChild(all)

 const map={}
 data.forEach(m=>map[m.code]=m.country+" "+m.flag)

 for(const c in map){
   const b=document.createElement("div")
   b.className="btn"
   b.innerText=map[c]
   b.onclick=()=>render(data.filter(x=>x.code===c))
   top.appendChild(b)
 }

 render(data)
})
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
