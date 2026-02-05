import asyncio
import re
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from telethon import TelegramClient

# ============ CONFIG ============
API_ID = 38077264
API_HASH = "4dac72033d68a6bab7586e67edb182ae"
SESSION_NAME = "selva_session"

# 🔴 حط ID القناة (لازم يبدأ بـ -100)
CHANNEL_ID = -1003808609180   # <-- عدّل هنا فقط

REFRESH_SECONDS = 15
FILTER_TEXT = "Auto-delete in 5 min"
SITE_PASSWORD = "selva1"
# ================================

# أكواد معروفة (والجديد بيتضاف تلقائي)
KNOWN_CODES = {
    "+93": "Afghanistan",
"+355": "Albania",
"+213": "Algeria",
"+376": "Andorra",
"+244": "Angola",
"+1-268": "Antigua and Barbuda",
"+54": "Argentina",
"+374": "Armenia",
"+61": "Australia",
"+43": "Austria",
"+994": "Azerbaijan",
"+1-242": "Bahamas",
"+973": "Bahrain",
"+880": "Bangladesh",
"+1-246": "Barbados",
"+375": "Belarus",
"+32": "Belgium",
"+501": "Belize",
"+229": "Benin",
"+975": "Bhutan",
"+591": "Bolivia",
"+387": "Bosnia and Herzegovina",
"+267": "Botswana",
"+55": "Brazil",
"+673": "Brunei",
"+359": "Bulgaria",
"+226": "Burkina Faso",
"+257": "Burundi",
"+238": "Cabo Verde",
"+855": "Cambodia",
"+237": "Cameroon",
"+1": "Canada",
"+236": "Central African Republic",
"+235": "Chad",
"+56": "Chile",
"+86": "China",
"+57": "Colombia",
"+269": "Comoros",
"+242": "Congo",
"+243": "Congo (DRC)",
"+506": "Costa Rica",
"+225": "Côte d'Ivoire",
"+385": "Croatia",
"+53": "Cuba",
"+357": "Cyprus",
"+420": "Czech Republic",
"+45": "Denmark",
"+253": "Djibouti",
"+1-767": "Dominica",
"+1-809, 1-829, 1-849": "Dominican Republic",
"+593": "Ecuador",
"+20": "Egypt",
"+503": "El Salvador",
"+240": "Equatorial Guinea",
"+291": "Eritrea",
"+372": "Estonia",
"+268": "Eswatini",
"+251": "Ethiopia",
"+679": "Fiji",
"+358": "Finland",
"+33": "France",
"+241": "Gabon",
"+220": "Gambia",
"+995": "Georgia",
"+49": "Germany",
"+233": "Ghana",
"+30": "Greece",
"+1-473": "Grenada",
"+502": "Guatemala",
"+224": "Guinea",
"+245": "Guinea-Bissau",
"+592": "Guyana",
"+509": "Haiti",
"+504": "Honduras",
"+36": "Hungary",
"+354": "Iceland",
"+91": "India",
"+62": "Indonesia",
"+98": "Iran",
"+964": "Iraq",
"+353": "Ireland",
"+972": "Israel",
"+39": "Italy",
"+1-876": "Jamaica",
"+81": "Japan",
"+962": "Jordan",
"+7": "Kazakhstan",
"+254": "Kenya",
"+686": "Kiribati",
"+383": "Kosovo",
"+965": "Kuwait",
"+996": "Kyrgyzstan",
"+856": "Laos",
"+371": "Latvia",
"+961": "Lebanon",
"+266": "Lesotho",
"+231": "Liberia",
"+218": "Libya",
"+423": "Liechtenstein",
"+370": "Lithuania",
"+352": "Luxembourg",
"+261": "Madagascar",
"+265": "Malawi",
"+60": "Malaysia",
"+960": "Maldives",
"+223": "Mali",
"+356": "Malta",
"+692": "Marshall Islands",
"+222": "Mauritania",
"+230": "Mauritius",
"+52": "Mexico",
"+691": "Micronesia",
"+373": "Moldova",
"+377": "Monaco",
"+976": "Mongolia",
"+382": "Montenegro",
"+212": "Morocco",
"+258": "Mozambique",
"+95": "Myanmar",
"+264": "Namibia",
"+674": "Nauru",
"+977": "Nepal",
"+31": "Netherlands",
"+64": "New Zealand",
"+505": "Nicaragua",
"+227": "Niger",
"+234": "Nigeria",
"+389": "North Macedonia",
"+850": "North Korea",
"+47": "Norway",
"+968": "Oman",
"+92": "Pakistan",
"+680": "Palau",
"+970": "Palestine",
"+507": "Panama",
"+675": "Papua New Guinea",
"+595": "Paraguay",
"+51": "Peru",
"+63": "Philippines",
"+48": "Poland",
"+351": "Portugal",
"+974": "Qatar",
"+40": "Romania",
"+7": "Russia",
"+250": "Rwanda",
"+1-869": "Saint Kitts and Nevis",
"+1-758": "Saint Lucia",
"+1-784": "Saint Vincent and the Grenadines",
"+685": "Samoa",
"+378": "San Marino",
"+239": "Sao Tome and Principe",
"+966": "Saudi Arabia",
"+221": "Senegal",
"+381": "Serbia",
"+248": "Seychelles",
"+232": "Sierra Leone",
"+65": "Singapore",
"+421": "Slovakia",
"+386": "Slovenia",
"+677": "Solomon Islands",
"+252": "Somalia",
"+27": "South Africa",
"+82": "South Korea",
"+211": "South Sudan",
"+34": "Spain",
"+94": "Sri Lanka",
"+249": "Sudan",
"+597": "Suriname",
"+46": "Sweden",
"+41": "Switzerland",
"+963": "Syria",
"+886": "Taiwan",
"+992": "Tajikistan",
"+255": "Tanzania",
"+66": "Thailand",
"+670": "Timor-Leste",
"+228": "Togo",
"+676": "Tonga",
"+1-868": "Trinidad and Tobago",
"+216": "Tunisia",
"+90": "Turkey",
"+993": "Turkmenistan",
"+688": "Tuvalu",
"+256": "Uganda",
"+380": "Ukraine",
"+971": "United Arab Emirates",
"+44": "United Kingdom",
"+1": "United States",
"+598": "Uruguay",
"+998": "Uzbekistan",
"+678": "Vanuatu",
"+379, +39": "Vatican City",
"+58": "Venezuela",
"+84": "Vietnam",
"+967": "Yemen",
"+260": "Zambia",
"+263": "Zimbabwe"
}

app = FastAPI()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# { "Egypt": [msg...], "Country +777": [...] }
messages_by_country = {}

def detect_country(text: str):
    """
    يلتقط كود الدولة من أول الرسالة: +digits
    لو معروف يرجّع الاسم
    لو جديد يضيفه تلقائيًا باسم Country +code
    """
    m = re.match(r"^\+(\d{1,4})", text)
    if not m:
        return None

    code = "+" + m.group(1)
    if code in KNOWN_CODES:
        return KNOWN_CODES[code]

    # إضافة تلقائية
    name = f"Country {code}"
    KNOWN_CODES[code] = name
    return name

# ============ TELETHON ============
async def fetch_messages():
    global messages_by_country

    print("🚀 Telethon starting...")
    await client.start()
    channel = await client.get_entity(CHANNEL_ID)
    print("✅ Channel loaded")

    while True:
        msgs = await client.get_messages(channel, limit=300)
        messages_by_country = {}

        for m in msgs:
            if not m.message:
                continue

            text = m.message.strip()

            # فلترة النص
            if FILTER_TEXT not in text:
                continue

            country = detect_country(text)
            if not country:
                continue

            messages_by_country.setdefault(country, []).append(text)

        print("📨 Tabs:", list(messages_by_country.keys()))
        await asyncio.sleep(REFRESH_SECONDS)

@app.on_event("startup")
async def startup():
    asyncio.create_task(fetch_messages())

# ============ AUTH ============
@app.post("/login")
async def login(data: dict):
    return {"ok": data.get("password") == SITE_PASSWORD}

# ============ API ============
@app.get("/countries")
def countries():
    return list(messages_by_country.keys())

@app.get("/messages/{country}")
def get_messages(country: str):
    return messages_by_country.get(country, [])

# ============ FRONTEND ============
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<title>SELVA Massage ⚡</title>
<style>
body{margin:0;font-family:Segoe UI;background:#000;color:#fff}
#splash,#login{
position:fixed;inset:0;background:black;
display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:10}
#splash img{width:140px;height:140px;border-radius:50%;box-shadow:0 0 30px #00f6ff}
h1{letter-spacing:6px}
#main{display:none}
#tabs{display:flex;overflow-x:auto;background:#111;padding:10px}
.tab{padding:10px 20px;margin-right:10px;background:#222;border-radius:8px;cursor:pointer;white-space:nowrap}
.tab:hover{background:#00f6ff;color:#000}
.msg{margin:15px;background:#111;padding:15px;border-radius:10px;box-shadow:0 0 10px #00f6ff44}
input,button{padding:10px;border-radius:6px;border:none;font-size:16px}
button{background:#00f6ff;font-weight:bold;cursor:pointer}
label{margin-top:10px;font-size:14px}
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
  <label><input type="checkbox" id="remember"> Remember me (7 days)</label>
  <br><br>
  <button onclick="login()">Login</button>
  <p id="err" style="color:red"></p>
</div>

<div id="main">
  <div id="tabs"></div>
  <div id="content"></div>
</div>

<script>
const WEEK = 7 * 24 * 60 * 60 * 1000;

function isLogged(){
  const d = localStorage.getItem("selva_auth");
  if(!d) return false;
  const o = JSON.parse(d);
  return Date.now() < o.expire;
}

setTimeout(()=>{
  splash.style.display="none";
  if(isLogged()){
    main.style.display="block";
    loadCountries();
  }else{
    login.style.display="flex";
  }
},5000);

function login(){
  fetch("/login",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({password:pass.value})
  }).then(r=>r.json()).then(d=>{
    if(d.ok){
      if(remember.checked){
        localStorage.setItem("selva_auth", JSON.stringify({expire: Date.now()+WEEK}));
      }
      login.style.display="none";
      main.style.display="block";
      loadCountries();
    }else{
      err.innerText="Wrong password";
    }
  });
}

function loadCountries(){
  fetch("/countries").then(r=>r.json()).then(data=>{
    tabs.innerHTML="";
    content.innerHTML="";
    data.forEach(c=>{
      let t=document.createElement("div");
      t.className="tab";
      t.innerText=c;
      t.onclick=()=>loadMessages(c);
      tabs.appendChild(t);
    });
  });
}

function loadMessages(country){
  fetch("/messages/"+encodeURIComponent(country))
  .then(r=>r.json()).then(data=>{
    content.innerHTML="";
    if(!data.length){
      content.innerHTML="<p style='padding:20px'>No messages</p>";
    }
    data.forEach(m=>{
      content.innerHTML+=`<div class="msg">${m}</div>`;
    });
  });
}
</script>

</body>
</html>
"""
