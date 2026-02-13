import os
import logging
import requests
import re
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
from dotenv import load_dotenv

# ================== CONFIG ==================
load_dotenv()

PANEL_URL = os.getenv("PANEL_URL", "http://198.135.52.238").rstrip("/")
PANEL_USERNAME = os.getenv("PANEL_USERNAME", "gagaywb66")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD", "gagaywb66")
PORT = int(os.getenv("PORT", 8080))
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", 100))
# ============================================

# ================== LOGGING ==================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ================== DATA STORAGE ==================
all_messages = []
debug_logs = []
seen_ids = set()

bot_stats = {
    "start_time": datetime.now().isoformat(),
    "total_otps": 0,
    "last_check": "Never",
    "is_running": False,
    "scraper_status": "⏳ Initializing",
    "last_error": None,
    "api_response": None
}

# ================== COUNTRY FLAGS ==================
COUNTRY_FLAGS = {
    'venezuela': '🇻🇪', 've': '🇻🇪', 'brazil': '🇧🇷', 'br': '🇧🇷',
    'argentina': '🇦🇷', 'ar': '🇦🇷', 'colombia': '🇨🇴', 'co': '🇨🇴',
    'usa': '🇺🇸', 'us': '🇺🇸', 'united states': '🇺🇸',
    'canada': '🇨🇦', 'ca': '🇨🇦', 'mexico': '🇲🇽', 'mx': '🇲🇽',
    'uk': '🇬🇧', 'gb': '🇬🇧', 'united kingdom': '🇬🇧',
    'germany': '🇩🇪', 'de': '🇩🇪', 'france': '🇫🇷', 'fr': '🇫🇷',
    'italy': '🇮🇹', 'it': '🇮🇹', 'spain': '🇪🇸', 'es': '🇪🇸',
    'russia': '🇷🇺', 'ru': '🇷🇺', 'india': '🇮🇳', 'in': '🇮🇳',
    'china': '🇨🇳', 'cn': '🇨🇳', 'japan': '🇯🇵', 'jp': '🇯🇵',
    'egypt': '🇪🇬', 'eg': '🇪🇬', 'morocco': '🇲🇦', 'ma': '🇲🇦',
    'uae': '🇦🇪', 'ae': '🇦🇪', 'saudi': '🇸🇦', 'sa': '🇸🇦',
    'australia': '🇦🇺', 'au': '🇦🇺',
}

# ================== DEBUG FUNCTION ==================
def add_debug(message):
    """Add debug message with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log = f"[{timestamp}] {message}"
    debug_logs.insert(0, log)
    if len(debug_logs) > 50:
        debug_logs.pop()
    logger.info(message)

# ================== HELPER FUNCTIONS ==================
def mask_phone_number(phone):
    """Mask phone number for privacy"""
    if not phone or phone == 'Unknown':
        return 'Unknown'
    phone = str(phone).strip()
    if len(phone) <= 6:
        return phone[:2] + '•••' + phone[-1:]
    if phone.startswith('+'):
        return f"{phone[:5]}•••{phone[-4:]}"
    return f"{phone[:4]}•••{phone[-4:]}"

def extract_otp(content):
    """Extract OTP from message content"""
    if not content:
        return 'N/A'
    
    patterns = [
        r'(\d{4,8})',
        r'(?:code|kode|otp|pin)[:\s]*(\d{4,8})',
        r'(\d{3}[-\s]?\d{3})',
        r'(\d{4}[-\s]?\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).replace(' ', '-')
    return 'N/A'

def detect_service(content):
    """Detect service from message content"""
    if not content:
        return 'SMS Service'
    
    services = {
        'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
        'facebook': 'Facebook', 'instagram': 'Instagram',
        'twitter': 'Twitter', 'google': 'Google',
        'tiktok': 'TikTok', 'snapchat': 'Snapchat',
        'paypal': 'PayPal', 'amazon': 'Amazon',
        'netflix': 'Netflix', 'spotify': 'Spotify',
    }
    
    content_lower = content.lower()
    for key, name in services.items():
        if key in content_lower:
            return name
    return 'SMS Service'

def get_country_flag(country):
    """Get flag emoji for country"""
    if not country:
        return '🌍'
    country_lower = country.lower().strip()
    if country_lower in COUNTRY_FLAGS:
        return COUNTRY_FLAGS[country_lower]
    for key, flag in COUNTRY_FLAGS.items():
        if key in country_lower:
            return flag
    return '🌍'

# ================== PANEL API CLASS ==================
class PanelAPI:
    def __init__(self):
        self.base_url = PANEL_URL
        self.username = PANEL_USERNAME
        self.password = PANEL_PASSWORD
        self.token = None
        self.session = requests.Session()
        self.logged_in = False
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    
    def login(self):
        """Login to panel and get token"""
        try:
            add_debug(f"🔐 Attempting login to {self.base_url}")
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"username": self.username, "password": self.password},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'token' in data:
                    self.token = data['token']
                    self.logged_in = True
                    self.session.headers['Authorization'] = f'Bearer {self.token}'
                    bot_stats['scraper_status'] = '✅ Connected'
                    add_debug("✅ Login successful!")
                    return True
                else:
                    add_debug(f"❌ No token in response")
            else:
                add_debug(f"❌ Login failed: {response.status_code}")
            
            bot_stats['scraper_status'] = '❌ Login failed'
            return False
            
        except Exception as e:
            add_debug(f"❌ Login error: {str(e)}")
            bot_stats['scraper_status'] = f'❌ Error'
            bot_stats['last_error'] = str(e)
            return False
    
    def fetch_messages(self):
        """Fetch messages from panel API"""
        if not self.logged_in:
            add_debug("⚠️ Not logged in, attempting login...")
            if not self.login():
                return []
        
        try:
            url = f"{self.base_url}/api/sms?limit=100"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 401:
                add_debug("⚠️ Token expired, re-logging...")
                self.logged_in = False
                if not self.login():
                    return []
                response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                add_debug(f"❌ Failed to fetch: {response.status_code}")
                return []
            
            # Save response for debugging
            bot_stats['api_response'] = response.text[:500]
            
            try:
                data = response.json()
            except:
                add_debug("❌ Invalid JSON response")
                return []
            
            # Handle different response formats
            if isinstance(data, list):
                messages = data
            elif isinstance(data, dict):
                messages = data.get('sms', data.get('messages', data.get('data', [])))
            else:
                messages = []
            
            formatted = []
            for msg in messages:
                formatted_msg = self._format_message(msg)
                if formatted_msg:
                    formatted.append(formatted_msg)
            
            return formatted
            
        except Exception as e:
            add_debug(f"❌ Fetch error: {str(e)}")
            bot_stats['last_error'] = str(e)
            return []
    
    def _format_message(self, msg):
        """Format raw message to standard format"""
        try:
            # Extract content
            content = msg.get('content') or msg.get('message') or msg.get('text', '')
            
            # Extract OTP
            otp = extract_otp(content)
            
            # Extract phone
            phone = msg.get('number') or msg.get('phone') or msg.get('Number', 'Unknown')
            
            # Extract country
            country = msg.get('country') or msg.get('Country') or ''
            country_flag = get_country_flag(country)
            
            # Extract service
            service = (
                msg.get('service') or 
                msg.get('sender') or 
                detect_service(content)
            )
            
            # Extract timestamp
            timestamp = msg.get('created_at') or msg.get('timestamp') or ''
            if timestamp:
                try:
                    dt = datetime.strptime(str(timestamp)[:19], '%Y-%m-%dT%H:%M:%S')
                    timestamp = dt.strftime('%Y-%m-%d %I:%M %p')
                except:
                    timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
            
            # Generate unique ID
            msg_id = msg.get('id') or msg.get('_id') or str(hash(str(msg)))
            
            return {
                'id': msg_id,
                'otp': otp,
                'phone': phone,
                'phone_masked': mask_phone_number(phone),
                'service': service,
                'country': country,
                'country_flag': country_flag,
                'timestamp': timestamp,
                'raw_message': content[:200] if content else ''
            }
        except Exception as e:
            add_debug(f"❌ Format error: {str(e)}")
            return None

# ================== INITIALIZE API ==================
panel = PanelAPI()

# ================== BACKGROUND WORKER ==================
def background_worker():
    """Background thread to fetch messages periodically"""
    bot_stats['is_running'] = True
    add_debug("🚀 Background worker started")
    
    # Initial login
    panel.login()
    
    while True:
        try:
            # Fetch messages
            messages = panel.fetch_messages()
            bot_stats['last_check'] = datetime.now().strftime('%H:%M:%S')
            
            # Process new messages
            new_count = 0
            for msg in messages:
                msg_id = msg['id']
                
                if msg_id not in seen_ids:
                    seen_ids.add(msg_id)
                    
                    # Only add if OTP is valid
                    if msg['otp'] != 'N/A':
                        all_messages.insert(0, msg)
                        bot_stats['total_otps'] += 1
                        new_count += 1
            
            if new_count > 0:
                add_debug(f"📨 {new_count} new OTPs received")
            
            # Keep only latest messages
            del all_messages[MAX_MESSAGES:]
            
        except Exception as e:
            bot_stats['last_error'] = str(e)
            add_debug(f"❌ Worker error: {str(e)}")
        
        time.sleep(FETCH_INTERVAL)

# ================== HTML TEMPLATE ==================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 OTP KING PANEL</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .logo { font-size: 24px; font-weight: 700; }
        
        .stats-bar {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #00ff88;
        }
        
        .stat-label {
            font-size: 12px;
            color: #aaa;
        }
        
        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .status-online {
            background: rgba(0,255,136,0.2);
            color: #00ff88;
        }
        
        .status-offline {
            background: rgba(255,68,68,0.2);
            color: #ff4444;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .btn {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: #000;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
        
        .btn-danger {
            background: #ff4444;
            color: #fff;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            opacity: 0.9;
        }
        
        .messages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .message-card {
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            animation: fadeIn 0.5s ease;
            transition: transform 0.3s;
        }
        
        .message-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,255,136,0.1);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .country-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .country-flag {
            font-size: 32px;
        }
        
        .country-name {
            font-weight: 600;
        }
        
        .service-badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
        }
        
        .otp-section {
            background: rgba(0,255,136,0.1);
            border: 2px solid rgba(0,255,136,0.3);
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
        }
        
        .otp-code {
            font-size: 28px;
            font-weight: 700;
            color: #00ff88;
            letter-spacing: 3px;
            font-family: monospace;
        }
        
        .copy-btn {
            background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88;
            padding: 8px 16px;
            border-radius: 8px;
            color: #00ff88;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.3s;
        }
        
        .copy-btn:hover {
            background: #00ff88;
            color: #000;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .info-label {
            color: #888;
            font-size: 13px;
        }
        
        .info-value {
            color: #fff;
            font-size: 13px;
        }
        
        .message-content {
            background: rgba(0,0,0,0.2);
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 13px;
            color: #aaa;
            max-height: 80px;
            overflow-y: auto;
        }
        
        .timestamp {
            text-align: right;
            font-size: 11px;
            color: #666;
            margin-top: 10px;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px;
            color: #888;
            grid-column: 1/-1;
        }
        
        .empty-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .debug-panel {
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-family: monospace;
            font-size: 12px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .debug-log {
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .refresh-indicator {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 12px;
            z-index: 1000;
        }
        
        .pulse {
            width: 10px;
            height: 10px;
            background: #00ff88;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
            margin-right: 10px;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        
        .tab {
            padding: 10px 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: #00ff88;
            color: #000;
        }
        
        .tab:hover {
            background: rgba(255,255,255,0.2);
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }
            .messages-grid {
                grid-template-columns: 1fr;
            }
            .refresh-indicator {
                bottom: 10px;
                right: 10px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">📱 OTP KING PANEL</div>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-value">{{ stats.total_otps }}</div>
                    <div class="stat-label">Total OTPs</div>
                </div>
                <div class="stat-item">
                    <div class
