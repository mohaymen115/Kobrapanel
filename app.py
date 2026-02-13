import os
import threading
import time
import logging
import re
import requests
from datetime import datetime
from flask import Flask, jsonify, render_template_string

# ================== CONFIG ==================
PANEL_URL = os.getenv("PANEL_URL", "").rstrip("/")
PANEL_USERNAME = os.getenv("PANEL_USERNAME", "")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD", "")
PORT = int(os.getenv("PORT", 8080))
FETCH_INTERVAL = 10
# ============================================

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# ================== GLOBAL STATE ==================
MESSAGES = []
SEEN_IDS = set()
LOGS = []

STATS = {
    "start_time": datetime.now().isoformat(),
    "total_otps": 0,
    "last_check": "never",
    "status": "starting",
    "last_error": None
}

MAX_MESSAGES = 100
# ================================================

def log(msg):
    LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    if len(LOGS) > 50:
        LOGS.pop()
    logging.info(msg)

# ================== PANEL API ====================
class PanelAPI:
    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def login(self):
        try:
            r = self.session.post(
                f"{PANEL_URL}/api/auth/login",
                json={
                    "username": PANEL_USERNAME,
                    "password": PANEL_PASSWORD
                },
                timeout=10
            )
            if r.status_code == 200 and "token" in r.json():
                self.token = r.json()["token"]
                self.session.headers["Authorization"] = f"Bearer {self.token}"
                log("Login success")
                return True
            log("Login failed")
        except Exception as e:
            STATS["last_error"] = str(e)
            log(f"Login error: {e}")
        return False

    def fetch_sms(self):
        if not self.token:
            if not self.login():
                return []

        try:
            r = self.session.get(
                f"{PANEL_URL}/api/sms?limit=50",
                timeout=10
            )
            if r.status_code == 401:
                self.token = None
                return []
            if r.status_code == 200:
                return r.json() if isinstance(r.json(), list) else []
        except Exception as e:
            STATS["last_error"] = str(e)
            log(f"Fetch error: {e}")
        return []

panel = PanelAPI()
# =================================================

def extract_otp(text):
    if not text:
        return None
    m = re.search(r"\b\d{4,8}\b", text)
    return m.group(0) if m else None

def background_worker():
    STATS["status"] = "running"
    log("Background worker started")

    while True:
        try:
            messages = panel.fetch_sms()
            STATS["last_check"] = datetime.now().strftime("%H:%M:%S")

            for m in messages:
                msg_id = m.get("id") or hash(str(m))
                if msg_id in SEEN_IDS:
                    continue

                SEEN_IDS.add(msg_id)
                otp = extract_otp(m.get("content", ""))

                if otp:
                    MESSAGES.insert(0, {
                        "otp": otp,
                        "service": m.get("service", "Unknown"),
                        "phone": m.get("number", "Unknown"),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    STATS["total_otps"] += 1

            del MESSAGES[MAX_MESSAGES:]

        except Exception as e:
            STATS["last_error"] = str(e)
            log(f"Worker crash: {e}")

        time.sleep(FETCH_INTERVAL)

# ================== HTML ==================
HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>OTP Dashboard</title>
<style>
body{font-family:Arial;background:#0f1220;color:#fff;padding:20px}
.card{background:#1a1f3c;padding:15px;border-radius:10px;margin-bottom:10px}
.otp{font-size:26px;color:#00ff88;font-weight:bold}
.small{color:#aaa;font-size:12px}
</style>
</head>
<body>
<h2>📱 OTP Dashboard</h2>
<p>Status: {{stats.status}}</p>
<p>Total OTPs: {{stats.total_otps}}</p>
<p>Last Check: {{stats.last_check}}</p>

{% for m in messages %}
<div class="card">
  <div class="otp">{{m.otp}}</div>
  <div class="small">Service: {{m.service}}</div>
  <div class="small">Phone: {{m.phone}}</div>
  <div class="small">{{m.time}}</div>
</div>
{% else %}
<p>No messages yet</p>
{% endfor %}

<hr>
<h3>Logs</h3>
<pre>{{logs}}</pre>
</body>
</html>
"""
# =========================================

@app.route("/")
def index():
    return render_template_string(
        HTML,
        messages=MESSAGES,
        stats=STATS,
        logs="\n".join(LOGS)
    )

@app.route("/health")
def health():
    return jsonify(ok=True)

# ================== START ==================
if __name__ == "__main__":
    threading.Thread(target=background_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
