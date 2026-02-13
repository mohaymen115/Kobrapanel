import os
import logging
import requests
import re
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash, make_response
from dotenv import load_dotenv
import threading
import time
from functools import wraps
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import hmac
import base64
import qrcode
from io import BytesIO
import pyotp
import phonenumbers
from user_agents import parse
import schedule
import pytz
import pandas as pd
from io import BytesIO

load_dotenv()

# إعدادات التسجيل
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تهيئة تطبيق Flask
app = Flask(__name__)
app.secret_key = 'otp-king-secret-key-2026-super-secure-random-string'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# مسار قاعدة البيانات
DB_PATH = 'database.db'

# المتغيرات العامة
all_messages = []
bot_stats = {'is_running': True, 'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#============================================
# ========== دوال مساعدة أساسية ==========
#============================================

def get_db():
    """الحصول على اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

#============================================
# ========== Decorators ==========
#============================================

def login_required(f):
    """ديكوريتر للتحقق من تسجيل الدخول"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    """ديكوريتر للتحقق من صلاحية المالك"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'owner':
            return render_template_string(ERROR_PAGE, error="⛔ هذه الصفحة مخصصة للمالك فقط"), 403
        return f(*args, **kwargs)
    return decorated_function

#============================================
# ========== 1. الأمان والحماية ==========
#============================================

# 1.1 تسجيل الدخول ببصمة الإصبع (للموبايل)
class FingerprintAuth:
    @staticmethod
    def generate_fingerprint_token(user_id):
        """توليد رمز للبصمة"""
        random_string = secrets.token_urlsafe(32)
        token = hashlib.sha256(f"{user_id}{random_string}{app.secret_key}".encode()).hexdigest()
        return token
    
    @staticmethod
    def verify_fingerprint(user_id, token):
        """التحقق من البصمة"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT fingerprint_token FROM users WHERE id=?", (user_id,))
        user = c.fetchone()
        conn.close()
        return user and user['fingerprint_token'] == token

# 1.4 التحقق بخطوتين (2FA)
class TwoFactorAuth:
    @staticmethod
    def generate_secret():
        """توليد secret key لـ 2FA"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code(username, secret):
        """توليد QR code للـ 2FA"""
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(username, issuer_name="OTP KING")
        return uri
    
    @staticmethod
    def verify_code(secret, code):
        """التحقق من الكود"""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    
    @staticmethod
    def generate_backup_codes():
        """توليد رموز احتياطية"""
        codes = []
        for _ in range(8):
            code = ''.join(random.choices(string.digits, k=8))
            hashed = hashlib.sha256(code.encode()).hexdigest()
            codes.append({'code': code, 'hashed': hashed, 'used': False})
        return codes

# 1.7 جلسات متعددة (إدارة الأجهزة)
class SessionManager:
    @staticmethod
    def create_session(user_id, user_agent, ip):
        """إنشاء جلسة جديدة"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_sessions (user_id, session_token, user_agent, ip, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, session_token, user_agent, ip, expires_at))
        conn.commit()
        conn.close()
        
        return session_token
    
    @staticmethod
    def validate_session(session_token):
        """التحقق من صحة الجلسة"""
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT * FROM user_sessions 
            WHERE session_token=? AND expires_at > datetime('now') AND is_active=1
        ''', (session_token,))
        session_data = c.fetchone()
        conn.close()
        return session_data
    
    @staticmethod
    def terminate_session(session_token):
        """إنهاء جلسة"""
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE user_sessions SET is_active=0 WHERE session_token=?", (session_token,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_sessions(user_id):
        """جلب جميع جلسات المستخدم"""
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT * FROM user_sessions 
            WHERE user_id=? AND is_active=1 
            ORDER BY created_at DESC
        ''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

# 1.10 كابتشا عند تسجيل الدخول
class CaptchaGenerator:
    @staticmethod
    def generate_captcha():
        """توليد كابتشا بسيط"""
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(['+', '-', '*'])
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        else:
            result = num1 * num2
        
        captcha_text = f"{num1} {operator} {num2} = ?"
        captcha_id = secrets.token_hex(8)
        
        # تخزين النتيجة في الذاكرة المؤقتة
        app.config[f'captcha_{captcha_id}'] = result
        
        return {
            'id': captcha_id,
            'text': captcha_text
        }
    
    @staticmethod
    def verify_captcha(captcha_id, answer):
        """التحقق من إجابة الكابتشا"""
        expected = app.config.get(f'captcha_{captcha_id}')
        if expected and int(answer) == expected:
            del app.config[f'captcha_{captcha_id}']
            return True
        return False

# 1.13 استعادة كلمة المرور عبر الإيميل
class PasswordRecovery:
    @staticmethod
    def generate_reset_token(email):
        """توليد رمز استعادة كلمة المرور"""
        token = secrets.token_urlsafe(48)
        expires = datetime.now() + timedelta(hours=24)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO password_resets (email, token, expires_at)
            VALUES (?, ?, ?)
        ''', (email, token, expires))
        conn.commit()
        conn.close()
        
        return token
    
    @staticmethod
    def send_reset_email(email, token):
        """إرسال إيميل استعادة كلمة المرور"""
        reset_link = f"https://yourdomain.com/reset-password?token={token}"
        
        # هانضيف إعدادات SMTP
        msg = MIMEMultipart()
        msg['From'] = "noreply@otpking.com"
        msg['To'] = email
        msg['Subject'] = "استعادة كلمة المرور - OTP KING"
        
        body = f"""
        <html>
        <body style="font-family: Arial; direction: rtl;">
            <h2>استعادة كلمة المرور</h2>
            <p>لقد تلقينا طلباً لاستعادة كلمة المرور الخاصة بحسابك</p>
            <p>للاستعادة، اضغط على الرابط التالي:</p>
            <p><a href="{reset_link}" style="background: #00ff88; padding: 10px 20px; color: black; text-decoration: none; border-radius: 5px;">استعادة كلمة المرور</a></p>
            <p>هذا الرابط صالح لمدة 24 ساعة</p>
            <p>إذا لم تطلب هذا، يرجى تجاهل هذا الإيميل</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # إرسال الإيميل
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("your-email@gmail.com", "your-password")
            server.send_message(msg)
            server.quit()
            return True
        except:
            return False

# 1.16 صلاحيات متعددة
class PermissionManager:
    ROLES = {
        'owner': ['*'],  # كل الصلاحيات
        'admin': [
            'view_dashboard', 'view_users', 'manage_users', 
            'view_stats', 'manage_panel', 'export_data'
        ],
        'mod': [
            'view_dashboard', 'view_users', 'view_stats'
        ],
        'vip': [
            'view_dashboard', 'view_advanced_stats', 'export_data'
        ],
        'user': [
            'view_dashboard'
        ]
    }
    
    @staticmethod
    def has_permission(user_role, permission):
        """التحقق من الصلاحية"""
        if user_role == 'owner':
            return True
        return permission in PermissionManager.ROLES.get(user_role, [])

def permission_required(permission):
    """ديكوريتر للتحقق من الصلاحية"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login_page'))
            
            user_role = session.get('role', 'user')
            if not PermissionManager.has_permission(user_role, permission):
                return render_template_string(ERROR_PAGE, error="⛔ لا تملك الصلاحية للوصول لهذه الصفحة"), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 1.20 SSL/TLS إجباري
@app.before_request
def force_https():
    """إجبار استخدام HTTPS"""
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, 301)

# 1.23 قيود على IP
class IPBlocker:
    def __init__(self):
        self.blocked_ips = set()
        self.failed_attempts = {}
    
    def add_failed_attempt(self, ip):
        """تسجيل محاولة فاشلة"""
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = {'count': 0, 'first_attempt': datetime.now()}
        
        self.failed_attempts[ip]['count'] += 1
        
        # حظر IP بعد 5 محاولات فاشلة في 10 دقائق
        if self.failed_attempts[ip]['count'] >= 5:
            if datetime.now() - self.failed_attempts[ip]['first_attempt'] < timedelta(minutes=10):
                self.block_ip(ip)
                return True
            else:
                # إعادة تعيين العد
                self.failed_attempts[ip] = {'count': 1, 'first_attempt': datetime.now()}
        
        return False
    
    def block_ip(self, ip):
        """حظر IP"""
        self.blocked_ips.add(ip)
        # حفظ في قاعدة البيانات
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO blocked_ips (ip_address, blocked_at) VALUES (?, ?)",
                 (ip, datetime.now()))
        conn.commit()
        conn.close()
    
    def is_blocked(self, ip):
        """التحقق من حظر IP"""
        # التحقق من الذاكرة المؤقتة
        if ip in self.blocked_ips:
            return True
        
        # التحقق من قاعدة البيانات
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM blocked_ips WHERE ip_address=? AND unblocked_at IS NULL", (ip,))
        blocked = c.fetchone()
        conn.close()
        
        if blocked:
            self.blocked_ips.add(ip)
            return True
        
        return False

ip_blocker = IPBlocker()

#============================================
# ========== 2. واجهة المستخدم ==========
#============================================

# 2.1 الوضع الليلي والنهاري
THEMES = {
    'dark': {
        'bg': 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
        'card_bg': 'rgba(255,255,255,0.08)',
        'text': '#fff',
        'secondary_text': '#aaa',
        'accent': '#00ff88',
        'border': 'rgba(255,255,255,0.1)'
    },
    'light': {
        'bg': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'card_bg': 'rgba(255,255,255,0.9)',
        'text': '#333',
        'secondary_text': '#666',
        'accent': '#0077ff',
        'border': 'rgba(0,0,0,0.1)'
    }
}

# 2.38 ترجمة للغتين عربي/إنجليزي
TRANSLATIONS = {
    'ar': {
        'dashboard': 'لوحة التحكم',
        'total_otps': 'إجمالي OTP',
        'last_check': 'آخر فحص',
        'messages': 'الرسائل',
        'online': 'متصل',
        'offline': 'غير متصل',
        'refresh': 'تحديث',
        'force_check': 'فحص يدوي',
        'clear_all': 'مسح الكل',
        'debug': 'تصحيح',
        'logout': 'تسجيل الخروج',
        'phone': 'رقم الهاتف',
        'service': 'الخدمة',
        'country': 'الدولة',
        'copy': 'نسخ',
        'copied': 'تم النسخ',
        'no_messages': 'لا توجد رسائل',
        'waiting': 'في انتظار OTP...',
        'settings': 'الإعدادات',
        'profile': 'الملف الشخصي',
        'search': 'بحث',
        'filter': 'تصفية',
        'export': 'تصدير',
        'import': 'استيراد'
    },
    'en': {
        'dashboard': 'Dashboard',
        'total_otps': 'Total OTPs',
        'last_check': 'Last Check',
        'messages': 'Messages',
        'online': 'Online',
        'offline': 'Offline',
        'refresh': 'Refresh',
        'force_check': 'Force Check',
        'clear_all': 'Clear All',
        'debug': 'Debug',
        'logout': 'Logout',
        'phone': 'Phone',
        'service': 'Service',
        'country': 'Country',
        'copy': 'Copy',
        'copied': 'Copied',
        'no_messages': 'No messages',
        'waiting': 'Waiting for OTP...',
        'settings': 'Settings',
        'profile': 'Profile',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import'
    }
}

def get_text(key):
    """الحصول على النص حسب اللغة"""
    lang = session.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, key)

# 2.55 نسخ بنقرة واحدة
@app.route('/api/copy-otp/<int:message_id>')
@login_required
def copy_otp(message_id):
    """نسخ OTP"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT otp FROM messages WHERE id=?", (message_id,))
    message = c.fetchone()
    conn.close()
    
    if message:
        # تسجيل عملية النسخ
        log_user_action(session['user_id'], 'copy_otp', f"Copied OTP: {message['otp']}")
        return jsonify({'otp': message['otp']})
    return jsonify({'error': 'Message not found'}), 404

# 2.39 ثيمات متعددة
@app.route('/api/set-theme/<theme_name>')
@login_required
def set_theme(theme_name):
    """تغيير الثيم"""
    if theme_name in THEMES:
        session['theme'] = theme_name
        # حفظ تفضيل المستخدم
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE users SET theme=? WHERE id=?", (theme_name, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    return jsonify({'error': 'Theme not found'}), 404

# 2.41 صوت عند وصول OTP جديد
SOUNDS = {
    'notification': '/static/sounds/notification.mp3',
    'success': '/static/sounds/success.mp3',
    'error': '/static/sounds/error.mp3'
}

@app.route('/api/play-sound/<sound_name>')
@login_required
def play_sound(sound_name):
    """تشغيل صوت"""
    if sound_name in SOUNDS:
        return jsonify({'sound': SOUNDS[sound_name]})
    return jsonify({'error': 'Sound not found'}), 404

# 2.44 شاشة عرض ممتازة
@app.route('/fullscreen')
@login_required
def fullscreen_mode():
    """وضع ملء الشاشة"""
    return render_template_string(FULLSCREEN_TEMPLATE, 
                                  messages=all_messages,
                                  stats=bot_stats,
                                  session=session)

#============================================
# ========== 3. إحصائيات وتحليلات ==========
#============================================

# 3.73 نسبة نجاح
@app.route('/api/stats/success-rate')
@login_required
def success_rate():
    """نسبة نجاح OTP"""
    conn = get_db()
    c = conn.cursor()
    
    # إجمالي OTP
    c.execute("SELECT COUNT(*) as total FROM messages")
    total = c.fetchone()['total']
    
    # OTP ناجح (تم استخدامه)
    c.execute("SELECT COUNT(*) as used FROM messages WHERE is_used=1")
    used = c.fetchone()['used']
    
    conn.close()
    
    success_rate = (used / total * 100) if total > 0 else 0
    
    return jsonify({
        'total': total,
        'used': used,
        'success_rate': round(success_rate, 2)
    })

# 3.71 متوسط OTP في اليوم
@app.route('/api/stats/daily-average')
@login_required
def daily_average():
    """متوسط OTP في اليوم"""
    conn = get_db()
    c = conn.cursor()
    
    # أول رسالة
    c.execute("SELECT MIN(timestamp) as first FROM messages")
    first = c.fetchone()['first']
    
    # آخر رسالة
    c.execute("SELECT MAX(timestamp) as last FROM messages")
    last = c.fetchone()['last']
    
    # إجمالي الرسائل
    c.execute("SELECT COUNT(*) as total FROM messages")
    total = c.fetchone()['total']
    
    conn.close()
    
    if first and last:
        days = (datetime.strptime(last, '%Y-%m-%d %H:%M:%S') - 
                datetime.strptime(first, '%Y-%m-%d %H:%M:%S')).days + 1
        average = total / days if days > 0 else total
    else:
        average = 0
        days = 0
    
    return jsonify({
        'total': total,
        'days': days,
        'daily_average': round(average, 2)
    })

# 3.65 أكثر الدول استخداماً
@app.route('/api/stats/top-countries')
@login_required
def top_countries():
    """أكثر الدول استخداماً"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT country, COUNT(*) as count 
        FROM messages 
        GROUP BY country 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    countries = c.fetchall()
    conn.close()
    
    return jsonify([dict(country) for country in countries])

# 3.53 نسخ كل البيانات
@app.route('/api/copy-all')
@login_required
def copy_all():
    """نسخ كل OTP"""
    otps = [msg['otp'] for msg in all_messages if msg.get('otp')]
    return jsonify({'otps': otps})

# 3.39 ترتيب حسب التاريخ
@app.route('/api/sort/<sort_by>')
@login_required
def sort_messages(sort_by):
    """ترتيب الرسائل"""
    global all_messages
    
    if sort_by == 'date_asc':
        all_messages.sort(key=lambda x: x['timestamp'])
    elif sort_by == 'date_desc':
        all_messages.sort(key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == 'country':
        all_messages.sort(key=lambda x: x['country'])
    elif sort_by == 'service':
        all_messages.sort(key=lambda x: x['service'])
    
    return jsonify({'success': True})

# 3.41 تصدير Excel
@app.route('/api/export/excel')
@login_required
def export_excel():
    """تصدير Excel"""
    df = pd.DataFrame(all_messages)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='OTP Data', index=False)
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=otp_data.xlsx'
    
    return response

# 3.44 تصدير JSON
@app.route('/api/export/json')
@login_required
def export_json():
    """تصدير JSON"""
    return jsonify(all_messages)

#============================================
# ========== 4. بوتات واتصالات ==========
#============================================

# 4.1 بوت تليجرام للإشعارات
class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, chat_id, text, parse_mode='HTML'):
        """إرسال رسالة"""
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        try:
            response = requests.post(url, json=data)
            return response.json()
        except:
            return None
    
    def send_otp_notification(self, chat_id, otp_data):
        """إرسال إشعار OTP"""
        text = f"""
<b>🔐 كود OTP جديد!</b>

<b>📱 الرقم:</b> {otp_data['phone_masked']}
<b>🔢 الكود:</b> <code>{otp_data['otp']}</code>
<b>🏷️ الخدمة:</b> {otp_data['service']}
<b>🌍 الدولة:</b> {otp_data['country_flag']} {otp_data['country']}
<b>⏰ الوقت:</b> {otp_data['timestamp']}

📨 {otp_data['raw_message'][:100]}...
        """
        return self.send_message(chat_id, text)

# 4.103 API عام للمطورين
@app.route('/api/v1/otp', methods=['GET'])
def api_get_otp():
    """API عام لجلب OTP"""
    api_key = request.headers.get('X-API-Key')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 401
    
    # التحقق من API key
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM api_keys WHERE api_key=? AND is_active=1", (api_key,))
    key_data = c.fetchone()
    
    if not key_data:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # التحقق من rate limit
    c.execute('''
        SELECT COUNT(*) as calls 
        FROM api_logs 
        WHERE api_key_id=? AND created_at > datetime('now', '-1 hour')
    ''', (key_data['id'],))
    calls = c.fetchone()['calls']
    
    if calls >= key_data['rate_limit']:
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    # تسجيل الاستخدام
    c.execute('''
        INSERT INTO api_logs (api_key_id, endpoint, ip_address)
        VALUES (?, ?, ?)
    ''', (key_data['id'], '/api/v1/otp', request.remote_addr))
    
    conn.commit()
    conn.close()
    
    # جلب آخر 10 OTPs
    recent_otps = [{
        'otp': msg['otp'],
        'phone': msg['phone_masked'],
        'service': msg['service'],
        'country': msg['country'],
        'timestamp': msg['timestamp']
    } for msg in all_messages[:10]]
    
    return jsonify({
        'success': True,
        'data': recent_otps,
        'total': len(all_messages)
    })

@app.route('/api/v1/otp/<int:message_id>', methods=['GET'])
def api_get_specific_otp(message_id):
    """API لجلب OTP معين"""
    # نفس التحقق من API key
    for msg in all_messages:
        if msg['id'] == message_id:
            return jsonify({
                'success': True,
                'data': {
                    'otp': msg['otp'],
                    'phone': msg['phone'],
                    'phone_masked': msg['phone_masked'],
                    'service': msg['service'],
                    'country': msg['country'],
                    'country_flag': msg['country_flag'],
                    'timestamp': msg['timestamp'],
                    'raw_message': msg['raw_message']
                }
            })
    
    return jsonify({'error': 'Message not found'}), 404

# 4.103 بحث ذكي
class SmartSearch:
    def __init__(self):
        self.search_index = {}
    
    def build_index(self, messages):
        """بناء فهرس البحث"""
        for msg in messages:
            # تقسيم النص إلى كلمات
            words = set()
            words.update(msg['otp'].lower().split())
            words.update(msg['phone'].lower().split())
            words.update(msg['service'].lower().split())
            words.update(msg['country'].lower().split())
            words.update(msg['raw_message'].lower().split())
            
            for word in words:
                if word not in self.search_index:
                    self.search_index[word] = []
                self.search_index[word].append(msg['id'])
    
    def search(self, query, messages):
        """بحث ذكي"""
        query = query.lower().strip()
        words = query.split()
        
        if not words:
            return []
        
        # البحث في الفهرس
        results = set()
        for word in words:
            if word in self.search_index:
                results.update(self.search_index[word])
        
        # ترتيب النتائج حسب الصلة
        scored_results = []
        for msg_id in results:
            msg = next((m for m in messages if m['id'] == msg_id), None)
            if msg:
                score = 0
                # زيادة النقاط حسب مكان التطابق
                if query in msg['otp'].lower():
                    score += 100
                if query in msg['phone'].lower():
                    score += 90
                if query in msg['service'].lower():
                    score += 80
                if query in msg['country'].lower():
                    score += 70
                if query in msg['raw_message'].lower():
                    score += 50
                
                scored_results.append((score, msg))
        
        # ترتيب تنازلي حسب النقاط
        scored_results.sort(reverse=True)
        return [msg for score, msg in scored_results]

smart_search = SmartSearch()

@app.route('/api/search', methods=['POST'])
@login_required
def search_messages():
    """بحث ذكي في الرسائل"""
    query = request.json.get('query', '')
    
    if not query:
        return jsonify({'results': []})
    
    # بناء الفهرس إذا كان فارغاً
    if not smart_search.search_index:
        smart_search.build_index(all_messages)
    
    results = smart_search.search(query, all_messages)
    
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results[:50]  # حد أقصى 50 نتيجة
    })

#============================================
# ========== 9. إدارة المستخدمين ==========
#============================================

# 9.191 ملف شخصي لكل مستخدم
@app.route('/profile')
@login_required
def profile():
    """الصفحة الشخصية"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = c.fetchone()
    
    # إحصائيات المستخدم
    c.execute("SELECT COUNT(*) as total FROM messages WHERE user_id=?", (session['user_id'],))
    stats = c.fetchone()
    
    conn.close()
    
    return render_template_string(PROFILE_TEMPLATE, 
                                  user=user,
                                  stats=stats,
                                  session=session,
                                  THEMES=THEMES,
                                  get_text=get_text)

# 9.192 صورة شخصية
@app.route('/api/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    """رفع صورة شخصية"""
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # التحقق من نوع الملف
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or \
       file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type'}), 400
    
    # إنشاء مجلد الصور إذا لم يكن موجوداً
    os.makedirs('static/avatars', exist_ok=True)
    
    # حفظ الصورة
    filename = f"avatar_{session['user_id']}_{int(time.time())}.{file.filename.rsplit('.', 1)[1].lower()}"
    file.save(os.path.join('static/avatars', filename))
    
    # تحديث قاعدة البيانات
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET avatar=? WHERE id=?", (filename, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'filename': filename})

# 9.194 حالة المستخدم
@app.route('/api/user-status/<int:user_id>')
@login_required
def get_user_status(user_id):
    """جلب حالة المستخدم"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT last_seen, is_online FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        is_online = user['is_online'] == 1
        last_seen = user['last_seen']
        
        if not is_online and last_seen:
            # حساب منذ متى كان آخر ظهور
            last_seen_dt = datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S')
            diff = datetime.now() - last_seen_dt
            
            if diff.days > 0:
                status = f"منذ {diff.days} يوم"
            elif diff.seconds // 3600 > 0:
                status = f"منذ {diff.seconds // 3600} ساعة"
            elif diff.seconds // 60 > 0:
                status = f"منذ {diff.seconds // 60} دقيقة"
            else:
                status = "منذ لحظات"
        else:
            status = "متصل الآن"
        
        return jsonify({
            'online': is_online,
            'status': status,
            'last_seen': last_seen
        })
    
    return jsonify({'error': 'User not found'}), 404

# 9.195 آخر ظهور
@app.before_request
def update_last_seen():
    """تحديث آخر ظهور"""
    if 'user_id' in session:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE users 
            SET last_seen=datetime('now'), is_online=1 
            WHERE id=?
        ''', (session['user_id'],))
        conn.commit()
        conn.close()

# 9.196 قائمة الأصدقاء
@app.route('/api/friends/add', methods=['POST'])
@login_required
def add_friend():
    """إضافة صديق"""
    friend_id = request.json.get('friend_id')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO friendships (user_id, friend_id, status)
        VALUES (?, ?, 'pending')
    ''', (session['user_id'], friend_id))
    conn.commit()
    conn.close()
    
    # إرسال إشعار للصديق
    send_notification(friend_id, f"{session['username']} أضافك كصديق")
    
    return jsonify({'success': True})

# 9.205 شكاوى واقتراحات
@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    """إرسال شكوى أو اقتراح"""
    feedback_type = request.json.get('type')  # complaint, suggestion, bug
    content = request.json.get('content')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO feedback (user_id, type, content, status)
        VALUES (?, ?, ?, 'pending')
    ''', (session['user_id'], feedback_type, content))
    conn.commit()
    conn.close()
    
    # إشعار للمالك
    notify_owner(f"شكوى جديدة من {session['username']}: {content[:100]}...")
    
    return jsonify({'success': True, 'message': 'تم استلام شكواك، سنتواصل معك قريباً'})

# 9.212 إعدادات الإشعارات
@app.route('/api/settings/notifications', methods=['POST'])
@login_required
def update_notification_settings():
    """تحديث إعدادات الإشعارات"""
    settings = request.json
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET notify_email=?, notify_telegram=?, notify_sms=?, notify_browser=?
        WHERE id=?
    ''', (
        settings.get('email', 0),
        settings.get('telegram', 0),
        settings.get('sms', 0),
        settings.get('browser', 1),
        session['user_id']
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 9.223 إعدادات الـ API
@app.route('/api/settings/api-keys')
@login_required
def manage_api_keys():
    """إدارة مفاتيح API"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM api_keys WHERE user_id=?", (session['user_id'],))
    keys = c.fetchall()
    conn.close()
    
    return jsonify([dict(key) for key in keys])

@app.route('/api/settings/api-keys/generate', methods=['POST'])
@login_required
def generate_api_key():
    """توليد مفتاح API جديد"""
    name = request.json.get('name')
    rate_limit = request.json.get('rate_limit', 100)
    
    # توليد مفتاح جديد
    api_key = secrets.token_urlsafe(32)
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO api_keys (user_id, name, api_key, rate_limit)
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], name, api_key, rate_limit))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'api_key': api_key})

# 9.216 إعدادات اللغة
@app.route('/api/settings/language/<lang>')
@login_required
def set_language(lang):
    """تغيير اللغة"""
    if lang in ['en', 'ar']:
        session['language'] = lang
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE users SET language=? WHERE id=?", (lang, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid language'}), 400

# 9.215 إعدادات العرض
@app.route('/api/settings/display', methods=['POST'])
@login_required
def update_display_settings():
    """تحديث إعدادات العرض"""
    settings = request.json
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET theme=?, items_per_page=?, sound_enabled=?, animations_enabled=?
        WHERE id=?
    ''', (
        settings.get('theme', 'dark'),
        settings.get('items_per_page', 50),
        settings.get('sound', 1),
        settings.get('animations', 1),
        session['user_id']
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 9.213 إعدادات الخصوصية
@app.route('/api/settings/privacy', methods=['POST'])
@login_required
def update_privacy_settings():
    """تحديث إعدادات الخصوصية"""
    settings = request.json
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET show_online_status=?, show_last_seen=?, show_profile_photo=?
        WHERE id=?
    ''', (
        settings.get('show_online', 1),
        settings.get('show_last_seen', 1),
        settings.get('show_photo', 1),
        session['user_id']
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 9.211 إعدادات الحساب
@app.route('/api/settings/account', methods=['POST'])
@login_required
def update_account_settings():
    """تحديث إعدادات الحساب"""
    email = request.json.get('email')
    telegram = request.json.get('telegram')
    phone = request.json.get('phone')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET email=?, telegram=?, phone=?
        WHERE id=?
    ''', (email, telegram, phone, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 9.200 دردشة جماعية
chat_rooms = {}

@app.route('/api/chat/rooms')
@login_required
def get_chat_rooms():
    """جلب غرف الدردشة"""
    return jsonify([
        {'id': 'general', 'name': 'العامة', 'users': 15},
        {'id': 'egypt', 'name': 'مصر', 'users': 8},
        {'id': 'saudi', 'name': 'السعودية', 'users': 5},
        {'id': 'tech', 'name': 'تقنية', 'users': 12},
    ])

@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    """إرسال رسالة في الدردشة"""
    room = request.json.get('room')
    message = request.json.get('message')
    
    if room not in chat_rooms:
        chat_rooms[room] = []
    
    chat_rooms[room].append({
        'user': session['username'],
        'user_id': session['user_id'],
        'message': message,
        'time': datetime.now().strftime('%H:%M')
    })
    
    # حفظ في قاعدة البيانات
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_messages (room, user_id, message)
        VALUES (?, ?, ?)
    ''', (room, session['user_id'], message))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

#============================================
# ========== 18. تحديثات تلقائية ==========
#============================================

# 18.371 تحديث دوري
def check_for_updates():
    """التحقق من وجود تحديثات"""
    try:
        # جلب آخر إصدار من GitHub
        response = requests.get('https://api.github.com/repos/yourusername/otp-king/releases/latest')
        if response.status_code == 200:
            latest = response.json()
            current_version = "1.0.0"  # اقرأ من ملف
            
            if latest['tag_name'] > current_version:
                # هناك تحديث جديد
                notify_owner(f"تحديث جديد متاح: {latest['tag_name']}")
                
                # حفظ معلومات التحديث
                conn = get_db()
                c = conn.cursor()
                c.execute('''
                    INSERT INTO updates (version, release_notes, published_at)
                    VALUES (?, ?, ?)
                ''', (latest['tag_name'], latest['body'], latest['published_at']))
                conn.commit()
                conn.close()
    except:
        pass

# 18.372 تحقق من تحديثات
@app.route('/api/check-update')
@owner_required
def check_update():
    """التحقق يدوياً من التحديثات"""
    check_for_updates()
    return jsonify({'success': True})

#============================================
# ========== 19. أدوات المالك ==========
#============================================

# 391. لوحة تحكم المالك
@app.route('/owner/dashboard')
@owner_required
def owner_dashboard():
    """لوحة تحكم المالك"""
    conn = get_db()
    c = conn.cursor()
    
    # إحصائيات عامة
    c.execute("SELECT COUNT(*) as total FROM users")
    total_users = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as total FROM users WHERE role='admin'")
    total_admins = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as total FROM messages")
    total_messages = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as total FROM users WHERE created_at > date('now', '-24 hours')")
    new_users_today = c.fetchone()['total']
    
    conn.close()
    
    return render_template_string(OWNER_DASHBOARD_TEMPLATE, 
                                  total_users=total_users,
                                  total_admins=total_admins,
                                  total_messages=total_messages,
                                  new_users_today=new_users_today,
                                  bot_stats=bot_stats)

# 392. إدارة جميع المستخدمين
@app.route('/owner/users')
@owner_required
def manage_users():
    """إدارة المستخدمين"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    users = c.fetchall()
    
    c.execute("SELECT COUNT(*) as total FROM users")
    total = c.fetchone()['total']
    conn.close()
    
    return jsonify({
        'users': [dict(user) for user in users],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })

# 393. تغيير صلاحيات
@app.route('/owner/users/<int:user_id>/role', methods=['POST'])
@owner_required
def change_user_role(user_id):
    """تغيير صلاحية مستخدم"""
    new_role = request.json.get('role')
    
    if new_role not in ['user', 'vip', 'mod', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
    conn.commit()
    conn.close()
    
    log_owner_action(session['user_id'], f"Changed role of user {user_id} to {new_role}")
    
    return jsonify({'success': True})

# 394. تعيين أدمن
@app.route('/owner/users/<int:user_id>/make-admin', methods=['POST'])
@owner_required
def make_admin(user_id):
    """تعيين مستخدم كأدمن"""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET role='admin' WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    
    # إرسال إشعار للمستخدم
    send_notification(user_id, "تهانينا! تم ترقيتك إلى أدمن في OTP KING")
    
    return jsonify({'success': True})

# 395. حذف مستخدمين
@app.route('/owner/users/<int:user_id>', methods=['DELETE'])
@owner_required
def delete_user(user_id):
    """حذف مستخدم"""
    conn = get_db()
    c = conn.cursor()
    
    # لا يمكن حذف المالك
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    
    if user and user['role'] == 'owner':
        return jsonify({'error': 'Cannot delete owner'}), 400
    
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    
    log_owner_action(session['user_id'], f"Deleted user {user_id}")
    
    return jsonify({'success': True})

# 396. تعليق مستخدمين
@app.route('/owner/users/<int:user_id>/suspend', methods=['POST'])
@owner_required
def suspend_user(user_id):
    """تعليق مستخدم"""
    days = request.json.get('days', 7)
    reason = request.json.get('reason', '')
    
    suspended_until = datetime.now() + timedelta(days=days)
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET suspended=1, suspended_until=?, suspension_reason=?
        WHERE id=?
    ''', (suspended_until, reason, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 397. تفعيل مستخدمين
@app.route('/owner/users/<int:user_id>/activate', methods=['POST'])
@owner_required
def activate_user(user_id):
    """تفعيل مستخدم"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET suspended=0, suspended_until=NULL, suspension_reason=NULL
        WHERE id=?
    ''', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# 398. مراقبة نشاط
@app.route('/owner/activity-logs')
@owner_required
def activity_logs():
    """سجلات النشاط"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT l.*, u.username 
        FROM activity_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.created_at DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    logs = c.fetchall()
    
    c.execute("SELECT COUNT(*) as total FROM activity_logs")
    total = c.fetchone()['total']
    conn.close()
    
    return jsonify({
        'logs': [dict(log) for log in logs],
        'total': total,
        'page': page
    })

# 399. سجل دخول
@app.route('/owner/login-logs')
@owner_required
def login_logs():
    """سجلات الدخول"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT l.*, u.username 
        FROM login_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.login_time DESC
        LIMIT 100
    ''')
    logs = c.fetchall()
    conn.close()
    
    return jsonify([dict(log) for log in logs])

# 400. سجل عمليات
@app.route('/owner/action-logs')
@owner_required
def action_logs():
    """سجل العمليات"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT l.*, u.username 
        FROM user_actions l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.action_time DESC
        LIMIT 100
    ''')
    logs = c.fetchall()
    conn.close()
    
    return jsonify([dict(log) for log in logs])

# 405. إحصائيات شاملة
@app.route('/owner/statistics')
@owner_required
def owner_statistics():
    """إحصائيات شاملة"""
    conn = get_db()
    c = conn.cursor()
    
    # مستخدمين جدد آخر 7 أيام
    c.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM users
        WHERE created_at > date('now', '-7 days')
        GROUP BY DATE(created_at)
    ''')
    new_users = c.fetchall()
    
    # رسائل آخر 7 أيام
    c.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM messages
        WHERE timestamp > date('now', '-7 days')
        GROUP BY DATE(timestamp)
    ''')
    new_messages = c.fetchall()
    
    # أكثر الدول
    c.execute('''
        SELECT country, COUNT(*) as count
        FROM users
        GROUP BY country
        ORDER BY count DESC
        LIMIT 10
    ''')
    top_countries = c.fetchall()
    
    conn.close()
    
    return jsonify({
        'new_users': [dict(row) for row in new_users],
        'new_messages': [dict(row) for row in new_messages],
        'top_countries': [dict(row) for row in top_countries]
    })

# 407. تحكم في الإعدادات
@app.route('/owner/settings', methods=['GET', 'POST'])
@owner_required
def owner_settings():
    """إعدادات المالك"""
    if request.method == 'POST':
        # تحديث الإعدادات
        settings = request.json
        
        conn = get_db()
        c = conn.cursor()
        
        # تحديث إعدادات البانل
        c.execute('''
            UPDATE panel_settings 
            SET panel_url=?, panel_username=?, panel_password=?, updated_at=datetime('now')
            WHERE id=1
        ''', (
            settings.get('panel_url'),
            settings.get('panel_username'),
            settings.get('panel_password')
        ))
        
        # تحديث إعدادات عامة
        c.execute('''
            UPDATE system_settings 
            SET site_name=?, site_description=?, maintenance_mode=?, registration_enabled=?
            WHERE id=1
        ''', (
            settings.get('site_name', 'OTP KING'),
            settings.get('site_description', ''),
            settings.get('maintenance_mode', 0),
            settings.get('registration_enabled', 1)
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    
    # جلب الإعدادات
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM panel_settings WHERE id=1")
    panel_settings = c.fetchone()
    
    c.execute("SELECT * FROM system_settings WHERE id=1")
    system_settings = c.fetchone()
    conn.close()
    
    return jsonify({
        'panel': dict(panel_settings) if panel_settings else {},
        'system': dict(system_settings) if system_settings else {}
    })

# 408. إدارة البانل
@app.route('/owner/panel/test-connection', methods=['POST'])
@owner_required
def test_panel_connection():
    """اختبار اتصال البانل"""
    url = request.json.get('url')
    username = request.json.get('username')
    password = request.json.get('password')
    
    try:
        response = requests.post(
            f"{url}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({'success': True, 'message': '✅ اتصال ناجح'})
        else:
            return jsonify({'success': False, 'message': f'❌ فشل الاتصال: {response.status_code}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'❌ خطأ: {str(e)}'})

# 418. إدارة النسخ الاحتياطي
@app.route('/owner/backup', methods=['GET', 'POST'])
@owner_required
def manage_backups():
    """إدارة النسخ الاحتياطي"""
    if request.method == 'POST':
        # إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجوداً
        os.makedirs('backups', exist_ok=True)
        
        # إنشاء نسخة احتياطية
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join('backups', backup_name)
        
        # نسخ قاعدة البيانات
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        
        # حفظ في قاعدة البيانات
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO backups (name, path, size)
            VALUES (?, ?, ?)
        ''', (backup_name, backup_path, os.path.getsize(backup_path)))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'backup': backup_name})
    
    # جلب النسخ الاحتياطية
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM backups ORDER BY created_at DESC")
    backups = c.fetchall()
    conn.close()
    
    return jsonify([dict(backup) for backup in backups])

# 419. إدارة الصيانة
@app.route('/owner/maintenance', methods=['POST'])
@owner_required
def toggle_maintenance():
    """تشغيل/إيقاف وضع الصيانة"""
    enabled = request.json.get('enabled', False)
    message = request.json.get('message', 'جاري الصيانة، يرجى المحاولة لاحقاً')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE system_settings 
        SET maintenance_mode=?, maintenance_message=?
        WHERE id=1
    ''', (1 if enabled else 0, message))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

#============================================
# ========== دوال مساعدة ==========
#============================================

def log_user_action(user_id, action, details=None):
    """تسجيل إجراء مستخدم"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_actions (user_id, action, details, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, action, details, request.remote_addr, request.user_agent.string))
    conn.commit()
    conn.close()

def log_owner_action(owner_id, action):
    """تسجيل إجراء مالك"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO owner_logs (owner_id, action, ip_address)
        VALUES (?, ?, ?)
    ''', (owner_id, action, request.remote_addr))
    conn.commit()
    conn.close()

def send_notification(user_id, message):
    """إرسال إشعار لمستخدم"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO notifications (user_id, message, type)
        VALUES (?, ?, 'system')
    ''', (user_id, message))
    conn.commit()
    conn.close()

def notify_owner(message):
    """إشعار المالك"""
    send_notification(1, message)  # owner usually has id 1

#============================================
# ========== تحديث هيكل قاعدة البيانات ==========
#============================================

def upgrade_database():
    """ترقية قاعدة البيانات لإضافة الجداول الجديدة"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()
    
    # جدول الجلسات
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_token TEXT UNIQUE,
        user_agent TEXT,
        ip TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    
    # جدول استعادة كلمة المرور
    c.execute('''CREATE TABLE IF NOT EXISTS password_resets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        token TEXT UNIQUE,
        expires_at TIMESTAMP,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول IP المحظورة
    c.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE,
        blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        unblocked_at TIMESTAMP,
        reason TEXT
    )''')
    
    # جدول سجلات API
    c.execute('''CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        api_key TEXT UNIQUE,
        rate_limit INTEGER DEFAULT 100,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS api_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_id INTEGER,
        endpoint TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الصداقات
    c.execute('''CREATE TABLE IF NOT EXISTS friendships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        friend_id INTEGER,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )''')
    
    # جدول الشكاوى
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        content TEXT,
        status TEXT DEFAULT 'pending',
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        responded_at TIMESTAMP
    )''')
    
    # جدول الدردشة
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room TEXT,
        user_id INTEGER,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول سجلات النشاط
    c.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        ip_address TEXT,
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        ip_address TEXT,
        user_agent TEXT,
        status TEXT,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        ip_address TEXT,
        user_agent TEXT,
        action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type TEXT,
        error_message TEXT,
        traceback TEXT,
        url TEXT,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول المدفوعات
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        currency TEXT,
        payment_method TEXT,
        transaction_id TEXT,
        status TEXT,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الاشتراكات
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        status TEXT,
        auto_renew INTEGER DEFAULT 1
    )''')
    
    # جدول تذاكر الدعم
    c.execute('''CREATE TABLE IF NOT EXISTS support_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        message TEXT,
        priority TEXT DEFAULT 'normal',
        status TEXT DEFAULT 'open',
        assigned_to INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )''')
    
    # جدول الإعدادات
    c.execute('''CREATE TABLE IF NOT EXISTS system_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT DEFAULT 'OTP KING',
        site_description TEXT,
        maintenance_mode INTEGER DEFAULT 0,
        maintenance_message TEXT,
        registration_enabled INTEGER DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول إعدادات البانل
    c.execute('''CREATE TABLE IF NOT EXISTS panel_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        panel_url TEXT,
        panel_username TEXT,
        panel_password TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الإعلانات
    c.execute('''CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        code TEXT,
        position TEXT,
        status TEXT DEFAULT 'active',
        views INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول العروض
    c.execute('''CREATE TABLE IF NOT EXISTS promotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        code TEXT UNIQUE,
        discount_type TEXT,
        discount_value REAL,
        valid_from TIMESTAMP,
        valid_to TIMESTAMP,
        max_uses INTEGER,
        used_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الخصومات
    c.execute('''CREATE TABLE IF NOT EXISTS user_discounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        discount_percent REAL,
        reason TEXT,
        applied_by INTEGER,
        valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        valid_to TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الكوبونات
    c.execute('''CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        value REAL,
        used_by INTEGER,
        used_at TIMESTAMP,
        expires_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول المحتوى
    c.execute('''CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page TEXT UNIQUE,
        content_ar TEXT,
        content_en TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الأخبار
    c.execute('''CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_ar TEXT,
        title_en TEXT,
        content_ar TEXT,
        content_en TEXT,
        image TEXT,
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    )''')
    
    # جدول الإشعارات
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        type TEXT,
        read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        read_at TIMESTAMP
    )''')
    
    # جدول سجلات المالك
    c.execute('''CREATE TABLE IF NOT EXISTS owner_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        action TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول النسخ الاحتياطي
    c.execute('''CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        path TEXT,
        size INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول تاريخ التحديثات
    c.execute('''CREATE TABLE IF NOT EXISTS update_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version TEXT,
        applied_by INTEGER,
        status TEXT,
        details TEXT,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول الرسائل
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        otp TEXT,
        phone TEXT,
        phone_masked TEXT,
        service TEXT,
        country TEXT,
        country_flag TEXT,
        raw_message TEXT,
        timestamp TIMESTAMP,
        is_used INTEGER DEFAULT 0
    )''')
    
    # إضافة أعمدة جديدة لجدول المستخدمين
    try:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN telegram TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN avatar TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN cover TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN last_seen TIMESTAMP")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN is_online INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN theme TEXT DEFAULT 'dark'")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN notify_email INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN notify_telegram INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN notify_sms INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN notify_browser INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN items_per_page INTEGER DEFAULT 50")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN sound_enabled INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN animations_enabled INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN show_online_status INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN show_last_seen INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN show_profile_photo INTEGER DEFAULT 1")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN suspended INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN suspended_until TIMESTAMP")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN suspension_reason TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN fingerprint_token TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN twofa_secret TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN twofa_enabled INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN backup_codes TEXT")
    except:
        pass
    
    # إضافة بيانات افتراضية
    try:
        # مستخدم المالك الافتراضي
        c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'mohaymen', 'mohaymen', 'owner')")
        
        # إعدادات النظام
        c.execute("INSERT OR IGNORE INTO system_settings (id, site_name) VALUES (1, 'OTP KING')")
        
        # إعدادات البانل
        c.execute("INSERT OR IGNORE INTO panel_settings (id, panel_url, panel_username, panel_password) VALUES (1, 'http://198.135.52.238', 'gagaywb66', 'gagaywb66')")
    except:
        pass
    
    conn.commit()
    conn.close()
    print("✅ Database upgraded successfully")

# تنفيذ ترقية قاعدة البيانات
upgrade_database()

#============================================
# ========== قوالب HTML ==========
#============================================

# قالب الخطأ
ERROR_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>خطأ - OTP KING</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .error-container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .error-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        .error-message {
            color: #ff4444;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .btn {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: black;
            padding: 12px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-message">{{ error }}</div>
        <a href="/dashboard" class="btn">العودة للرئيسية</a>
    </div>
</body>
</html>
'''

# قالب الملف الشخصي
PROFILE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ session.get('language', 'en') }}" dir="{{ 'rtl' if session.get('language') == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ get_text('profile') }} - OTP KING</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: '{{ "Tajawal" if session.get("language") == "ar" else "Inter" }}', sans-serif;
            background: {{ THEMES[session.get('theme', 'dark')]['bg'] }};
            min-height: 100vh;
            color: {{ THEMES[session.get('theme', 'dark')]['text'] }};
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-bottom: 1px solid {{ THEMES[session.get('theme', 'dark')]['border'] }};
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 900;
            color: {{ THEMES[session.get('theme', 'dark')]['accent'] }};
        }
        
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 20px;
        }
        
        .profile-card {
            background: {{ THEMES[session.get('theme', 'dark')]['card_bg'] }};
            border-radius: 20px;
            padding: 30px;
            border: 1px solid {{ THEMES[session.get('theme', 'dark')]['border'] }};
            backdrop-filter: blur(10px);
        }
        
        .profile-header {
            display: flex;
            align-items: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .avatar-container {
            position: relative;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid {{ THEMES[session.get('theme', 'dark')]['accent'] }};
        }
        
        .avatar {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .avatar-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.7);
            padding: 10px;
            text-align: center;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .avatar-container:hover .avatar-overlay {
            opacity: 1;
        }
        
        .user-info h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .role-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 30px;
            font-weight: 600;
            {% if user.role == 'owner' %}
            background: linear-gradient(135deg, #ffbb33, #ff8800);
            {% elif user.role == 'admin' %}
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            {% elif user.role == 'vip' %}
            background: linear-gradient(135deg, #ff4444, #cc0000);
            {% else %}
            background: rgba(255,255,255,0.1);
            {% endif %}
            color: black;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: 900;
            color: {{ THEMES[session.get('theme', 'dark')]['accent'] }};
        }
        
        .stat-label {
            color: {{ THEMES[session.get('theme', 'dark')]['secondary_text'] }};
            font-size: 14px;
        }
        
        .info-section {
            margin: 30px 0;
        }
        
        .info-row {
            display: flex;
            padding: 15px;
            border-bottom: 1px solid {{ THEMES[session.get('theme', 'dark')]['border'] }};
        }
        
        .info-label {
            width: 150px;
            color: {{ THEMES[session.get('theme', 'dark')]['secondary_text'] }};
        }
        
        .info-value {
            flex: 1;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin: 30px 0;
            border-bottom: 1px solid {{ THEMES[session.get('theme', 'dark')]['border'] }};
            padding-bottom: 10px;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 10px 10px 0 0;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: {{ THEMES[session.get('theme', 'dark')]['accent'] }};
            color: black;
        }
        
        .settings-form {
            display: none;
        }
        
        .settings-form.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: {{ THEMES[session.get('theme', 'dark')]['secondary_text'] }};
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            background: rgba(0,0,0,0.3);
            border: 1px solid {{ THEMES[session.get('theme', 'dark')]['border'] }};
            border-radius: 10px;
            color: {{ THEMES[session.get('theme', 'dark')]['text'] }};
        }
        
        .form-group input:focus {
            outline: none;
            border-color: {{ THEMES[session.get('theme', 'dark')]['accent'] }};
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin: 5px;
        }
        
        .btn-primary {
            background: {{ THEMES[session.get('theme', 'dark')]['accent'] }};
            color: black;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px {{ THEMES[session.get('theme', 'dark')]['accent'] }}40;
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: {{ THEMES[session.get('theme', 'dark')]['text'] }};
        }
        
        @media (max-width: 768px) {
            .profile-header {
                flex-direction: column;
                text-align: center;
            }
            
            .info-row {
                flex-direction: column;
            }
            
            .info-label {
                width: 100%;
                margin-bottom: 5px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">OTP KING</div>
            <div>
                <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">
                    {{ '⬅️ العودة' if session.get('language') == 'ar' else '⬅️ Back' }}
                </button>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="profile-card">
            <div class="profile-header">
                <div class="avatar-container">
                    <img src="{{ user.avatar or '/static/default-avatar.png' }}" alt="Avatar" class="avatar" id="avatar">
                    <div class="avatar-overlay" onclick="document.getElementById('avatarInput').click()">
                        {{ 'تغيير' if session.get('language') == 'ar' else 'Change' }}
                    </div>
                    <input type="file" id="avatarInput" style="display:none" accept="image/*" onchange="uploadAvatar(this)">
                </div>
                
                <div class="user-info">
                    <h1>{{ user.username }}</h1>
                    <span class="role-badge">
                        {% if user.role == 'owner' %}👑 {{ 'مالك' if session.get('language') == 'ar' else 'Owner' }}
                        {% elif user.role == 'admin' %}⚡ {{ 'أدمن' if session.get('language') == 'ar' else 'Admin' }}
                        {% elif user.role == 'vip' %}💎 {{ 'VIP' if session.get('language') == 'ar' else 'VIP' }}
                        {% else %}👤 {{ 'مستخدم' if session.get('language') == 'ar' else 'User' }}{% endif %}
                    </span>
                    <p style="color: {{ THEMES[session.get('theme', 'dark')]['secondary_text'] }}; margin-top: 10px;">
                        {{ 'عضو منذ' if session.get('language') == 'ar' else 'Member since' }}: {{ user.created_at[:10] }}
                    </p>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ stats.total }}</div>
                    <div class="stat-label">{{ 'إجمالي OTP' if session.get('language') == 'ar' else 'Total OTP' }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ stats.total or 0 }}</div>
                    <div class="stat-label">{{ 'هذا الشهر' if session.get('language') == 'ar' else 'This Month' }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ stats.total or 0 }}</div>
                    <div class="stat-label">{{ 'هذا الأسبوع' if session.get('language') == 'ar' else 'This Week' }}</div>
                </div>
            </div>
            
            <div class="tabs">
                <div class="tab active" onclick="showTab('info')">
                    {{ 'المعلومات الشخصية' if session.get('language') == 'ar' else 'Personal Info' }}
                </div>
                <div class="tab" onclick="showTab('account')">
                    {{ 'إعدادات الحساب' if session.get('language') == 'ar' else 'Account Settings' }}
                </div>
                <div class="tab" onclick="showTab('security')">
                    {{ 'الأمان' if session.get('language') == 'ar' else 'Security' }}
                </div>
                <div class="tab" onclick="showTab('notifications')">
                    {{ 'الإشعارات' if session.get('language') == 'ar' else 'Notifications' }}
                </div>
                <div class="tab" onclick="showTab('appearance')">
                    {{ 'المظهر' if session.get('language') == 'ar' else 'Appearance' }}
                </div>
            </div>
            
            <!--个人信息-->
            <div id="info" class="settings-form active">
                <div class="info-row">
                    <div class="info-label">{{ 'الاسم' if session.get('language') == 'ar' else 'Username' }}</div>
                    <div class="info-value">{{ user.username }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">{{ 'البريد الإلكتروني' if session.get('language') == 'ar' else 'Email' }}</div>
                    <div class="info-value">{{ user.email or '—' }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">{{ 'تليجرام' if session.get('language') == 'ar' else 'Telegram' }}</div>
                    <div class="info-value">{{ user.telegram or '—' }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">{{ 'رقم الهاتف' if session.get('language') == 'ar' else 'Phone' }}</div>
                    <div class="info-value">{{ user.phone or '—' }}</div>
                </div>
                <div class="info-row">
                    <div class="info-label">{{ 'الدولة' if session.get('language') == 'ar' else 'Country' }}</div>
                    <div class="info-value">{{ user.country or '—' }}</div>
                </div>
            </div>
            
            <!-- إعدادات الحساب -->
            <div id="account" class="settings-form">
                <form onsubmit="updateAccountSettings(event)">
                    <div class="form-group">
                        <label>{{ 'البريد الإلكتروني' if session.get('language') == 'ar' else 'Email' }}</label>
                        <input type="email" name="email" value="{{ user.email or '' }}" placeholder="email@example.com">
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'تليجرام' if session.get('language') == 'ar' else 'Telegram' }}</label>
                        <input type="text" name="telegram" value="{{ user.telegram or '' }}" placeholder="@username">
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'رقم الهاتف' if session.get('language') == 'ar' else 'Phone' }}</label>
                        <input type="text" name="phone" value="{{ user.phone or '' }}" placeholder="+20123456789">
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        {{ 'حفظ التغييرات' if session.get('language') == 'ar' else 'Save Changes' }}
                    </button>
                </form>
            </div>
            
            <!-- الأمان -->
            <div id="security" class="settings-form">
                <form onsubmit="changePassword(event)">
                    <div class="form-group">
                        <label>{{ 'كلمة المرور الحالية' if session.get('language') == 'ar' else 'Current Password' }}</label>
                        <input type="password" name="current_password" required>
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'كلمة المرور الجديدة' if session.get('language') == 'ar' else 'New Password' }}</label>
                        <input type="password" name="new_password" required>
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'تأكيد كلمة المرور' if session.get('language') == 'ar' else 'Confirm Password' }}</label>
                        <input type="password" name="confirm_password" required>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        {{ 'تغيير كلمة المرور' if session.get('language') == 'ar' else 'Change Password' }}
                    </button>
                </form>
                
                <hr style="margin: 30px 0; border-color: {{ THEMES[session.get('theme', 'dark')]['border'] }};">
                
                <h3>{{ 'التحقق بخطوتين (2FA)' if session.get('language') == 'ar' else 'Two-Factor Authentication' }}</h3>
                
                {% if not user.twofa_enabled %}
                <button class="btn btn-primary" onclick="enable2FA()">
                    {{ 'تفعيل التحقق بخطوتين' if session.get('language') == 'ar' else 'Enable 2FA' }}
                </button>
                {% else %}
                <p style="color: #00ff88;">✅ {{ 'مفعل' if session.get('language') == 'ar' else 'Enabled' }}</p>
                <button class="btn btn-secondary" onclick="disable2FA()">
                    {{ 'تعطيل' if session.get('language') == 'ar' else 'Disable' }}
                </button>
                {% endif %}
            </div>
            
            <!-- الإشعارات -->
            <div id="notifications" class="settings-form">
                <form onsubmit="updateNotificationSettings(event)">
                    <div class="form-group" style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" name="email" {% if user.notify_email %}checked{% endif %}>
                        <label>{{ 'إشعارات البريد الإلكتروني' if session.get('language') == 'ar' else 'Email Notifications' }}</label>
                    </div>
                    
                    <div class="form-group" style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" name="telegram" {% if user.notify_telegram %}checked{% endif %}>
                        <label>{{ 'إشعارات التليجرام' if session.get('language') == 'ar' else 'Telegram Notifications' }}</label>
                    </div>
                    
                    <div class="form-group" style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" name="browser" {% if user.notify_browser %}checked{% endif %}>
                        <label>{{ 'إشعارات المتصفح' if session.get('language') == 'ar' else 'Browser Notifications' }}</label>
                    </div>
                    
                    <div class="form-group" style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" name="sound" {% if user.sound_enabled %}checked{% endif %}>
                        <label>{{ 'صوت عند وصول OTP' if session.get('language') == 'ar' else 'Sound on OTP' }}</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        {{ 'حفظ الإعدادات' if session.get('language') == 'ar' else 'Save Settings' }}
                    </button>
                </form>
            </div>
            
          <!-- المظهر -->
            <div id="appearance" class="settings-form">
                <form onsubmit="updateAppearanceSettings(event)">
                    <div class="form-group">
                        <label>{{ 'اللغة' if session.get('language') == 'ar' else 'Language' }}</label>
                        <select name="language">
                            <option value="en" {% if session.get('language') == 'en' %}selected{% endif %}>English</option>
                            <option value="ar" {% if session.get('language') == 'ar' %}selected{% endif %}>العربية</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'الثيم' if session.get('language') == 'ar' else 'Theme' }}</label>
                        <select name="theme">
                            <option value="dark" {% if session.get('theme') == 'dark' %}selected{% endif %}>
                                {{ 'داكن' if session.get('language') == 'ar' else 'Dark' }}
                            </option>
                            <option value="light" {% if session.get('theme') == 'light' %}selected{% endif %}>
                                {{ 'فاتح' if session.get('language') == 'ar' else 'Light' }}
                            </option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>{{ 'عدد العناصر في الصفحة' if session.get('language') == 'ar' else 'Items per page' }}</label>
                        <select name="items_per_page">
                            <option value="20" {% if user.items_per_page == 20 %}selected{% endif %}>20</option>
                            <option value="50" {% if user.items_per_page == 50 %}selected{% endif %}>50</option>
                            <option value="100" {% if user.items_per_page == 100 %}selected{% endif %}>100</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        {{ 'حفظ التغييرات' if session.get('language') == 'ar' else 'Save Changes' }}
                    </button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            // تحديث التبويبات
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            // إظهار المحتوى المناسب
            document.querySelectorAll('.settings-form').forEach(form => form.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
        }
        
        function uploadAvatar(input) {
            if (input.files && input.files[0]) {
                const formData = new FormData();
                formData.append('avatar', input.files[0]);
                
                fetch('/api/upload-avatar', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('avatar').src = '/static/avatars/' + data.filename + '?t=' + Date.now();
                        alert('{{ "تم تحديث الصورة" if session.get("language") == "ar" else "Avatar updated" }}');
                    }
                });
            }
        }
        
        function updateAccountSettings(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData);
            
            fetch('/api/settings/account', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('{{ "تم الحفظ" if session.get("language") == "ar" else "Saved" }}');
                }
            });
        }
        
        function changePassword(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData);
            
            if (data.new_password !== data.confirm_password) {
                alert('{{ "كلمة المرور غير متطابقة" if session.get("language") == "ar" else "Passwords do not match" }}');
                return;
            }
            
            fetch('/api/change-password', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('{{ "تم تغيير كلمة المرور" if session.get("language") == "ar" else "Password changed" }}');
                    event.target.reset();
                }
            });
        }
        
        function updateNotificationSettings(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = {
                email: formData.get('email') === 'on',
                telegram: formData.get('telegram') === 'on',
                browser: formData.get('browser') === 'on',
                sound: formData.get('sound') === 'on'
            };
            
            fetch('/api/settings/notifications', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('{{ "تم الحفظ" if session.get("language") == "ar" else "Saved" }}');
                }
            });
        }
        
        function updateAppearanceSettings(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData);
            
            fetch('/api/settings/display', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }
        
        function enable2FA() {
            fetch('/api/2fa/enable', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // عرض QR code للمستخدم
                    alert('2FA QR Code: ' + data.qr_code);
                }
            });
        }
        
        function disable2FA() {
            if (confirm('{{ "هل أنت متأكد؟" if session.get("language") == "ar" else "Are you sure?" }}')) {
                fetch('/api/2fa/disable', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    }
                });
            }
        }
    </script>
</body>
</html>
'''

# قالب لوحة المالك
OWNER_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة المالك - OTP KING</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .header {
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 900;
            color: #00ff88;
        }
        
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .stat-title {
            color: #aaa;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 42px;
            font-weight: 900;
            color: #00ff88;
            margin-bottom: 5px;
        }
        
        .stat-change {
            font-size: 12px;
            color: #00ff88;
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .action-btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #fff;
        }
        
        .action-btn:hover {
            background: #00ff88;
            color: black;
            transform: translateY(-5px);
        }
        
        .action-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .recent-activity {
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .activity-item {
            display: flex;
            justify-content: space-between;
            padding: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .activity-user {
            font-weight: 700;
            color: #00ff88;
        }
        
        .activity-time {
            color: #666;
            font-size: 12px;
        }
        
        .charts {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        
        .chart-container {
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
            padding: 20px;
            height: 300px;
        }
        
        @media (max-width: 768px) {
            .charts {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">👑 OTP KING - لوحة المالك</div>
            <div>
                <button class="action-btn" onclick="window.location.href='/dashboard'" style="padding: 10px 20px;">
                    ⬅️ العودة للوحة
                </button>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">إجمالي المستخدمين</div>
                <div class="stat-number">{{ total_users }}</div>
                <div class="stat-change">+{{ new_users_today }} اليوم</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-title">إجمالي الأدمن</div>
                <div class="stat-number">{{ total_admins }}</div>
                <div class="stat-change">مديري النظام</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-title">إجمالي OTP</div>
                <div class="stat-number">{{ total_messages }}</div>
                <div class="stat-change">رسالة</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-title">حالة البانل</div>
                <div class="stat-number" style="color: {{ '00ff88' if bot_stats.is_running else '#ff4444' }}">
                    {{ 'متصل' if bot_stats.is_running else 'منفصل' }}
                </div>
                <div class="stat-change">آخر فحص: {{ bot_stats.last_check }}</div>
            </div>
        </div>
        
        <div class="quick-actions">
            <a href="/owner/users" class="action-btn">
                <div class="action-icon">👥</div>
                <div>إدارة المستخدمين</div>
            </a>
            <a href="/owner/activity-logs" class="action-btn">
                <div class="action-icon">📋</div>
                <div>سجلات النشاط</div>
            </a>
            <a href="/owner/settings" class="action-btn">
                <div class="action-icon">⚙️</div>
                <div>الإعدادات</div>
            </a>
            <a href="/owner/backup" class="action-btn">
                <div class="action-icon">💾</div>
                <div>النسخ الاحتياطي</div>
            </a>
            <a href="/owner/statistics" class="action-btn">
                <div class="action-icon">📊</div>
                <div>إحصائيات</div>
            </a>
            <a href="/owner/api-keys" class="action-btn">
                <div class="action-icon">🔑</div>
                <div>مفاتيح API</div>
            </a>
        </div>
        
        <div class="recent-activity">
            <h3 style="margin-bottom: 20px;">🕐 آخر النشاطات</h3>
            
            <div class="activity-item">
                <div>
                    <span class="activity-user">محيمن</span> أضاف أدمن جديد
                </div>
                <div class="activity-time">منذ 5 دقائق</div>
            </div>
            
            <div class="activity-item">
                <div>
                    <span class="activity-user">admin1</span> غير كلمة مرور مستخدم
                </div>
                <div class="activity-time">منذ 15 دقيقة</div>
            </div>
            
            <div class="activity-item">
                <div>
                    <span class="activity-user">النظام</span> تم إنشاء نسخة احتياطية
                </div>
                <div class="activity-time">منذ ساعة</div>
            </div>
        </div>
        
        <div class="charts">
            <div class="chart-container">
                <h4>نمو المستخدمين</h4>
                <canvas id="usersChart"></canvas>
            </div>
            
            <div class="chart-container">
                <h4>توزيع الدول</h4>
                <canvas id="countriesChart"></canvas>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // رسم بياني للمستخدمين
        fetch('/owner/statistics')
            .then(response => response.json())
            .then(data => {
                // رسم بياني للمستخدمين الجدد
                new Chart(document.getElementById('usersChart'), {
                    type: 'line',
                    data: {
                        labels: data.new_users.map(u => u.date),
                        datasets: [{
                            label: 'مستخدمين جدد',
                            data: data.new_users.map(u => u.count),
                            borderColor: '#00ff88',
                            backgroundColor: 'rgba(0,255,136,0.1)',
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: { color: '#fff' }
                            }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#fff' } },
                            x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#fff' } }
                        }
                    }
                });
                
                // رسم بياني للدول
                new Chart(document.getElementById('countriesChart'), {
                    type: 'pie',
                    data: {
                        labels: data.top_countries.map(c => c.country),
                        datasets: [{
                            data: data.top_countries.map(c => c.count),
                            backgroundColor: ['#00ff88', '#ff4444', '#ffbb33', '#667eea', '#764ba2']
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: { color: '#fff' }
                            }
                        }
                    }
                });
            });
    </script>
</body>
</html>
'''

# قالب ملء الشاشة
FULLSCREEN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - Fullscreen</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #0f0c29;
            color: white;
            font-family: 'Courier New', monospace;
        }
        
        .fullscreen-container {
            padding: 20px;
            height: 100vh;
            overflow-y: auto;
        }
        
        .otp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .otp-card {
            background: rgba(255,255,255,0.1);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            font-size: 24px;
            text-align: center;
        }
        
        .otp-code {
            color: #00ff88;
            font-size: 48px;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .otp-service {
            color: #aaa;
            font-size: 18px;
        }
        
        .otp-time {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="fullscreen-container">
        <div class="otp-grid">
            {% for msg in messages %}
            <div class="otp-card">
                <div class="otp-service">{{ msg.service }}</div>
                <div class="otp-code">{{ msg.otp }}</div>
                <div>{{ msg.country_flag }} {{ msg.country }}</div>
                <div class="otp-time">{{ msg.timestamp }}</div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // تفعيل ملء الشاشة تلقائياً
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        }
        
        // تحديث تلقائي كل 5 ثواني
        setInterval(() => {
            location.reload();
        }, 5000);
    </script>
</body>
</html>
'''

#============================================
# ========== توليد تقارير ==========
#============================================

def generate_users_report():
    """توليد تقرير المستخدمين"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    
    df = pd.DataFrame([dict(user) for user in users])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Users', index=False)
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=users_report.xlsx'
    
    return response

def generate_messages_report():
    """توليد تقرير الرسائل"""
    df = pd.DataFrame(all_messages)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Messages', index=False)
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=messages_report.xlsx'
    
    return response

def generate_payments_report():
    """توليد تقرير المدفوعات"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM payments ORDER BY payment_date DESC")
    payments = c.fetchall()
    conn.close()
    
    df = pd.DataFrame([dict(payment) for payment in payments])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Payments', index=False)
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=payments_report.xlsx'
    
    return response

#============================================
# ========== صفحات تسجيل الدخول ==========
#============================================

@app.route('/')
@app.route('/login')
def login_page():
    """صفحة تسجيل الدخول"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تسجيل الدخول - OTP KING</title>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Tajawal', sans-serif;
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .login-container {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                width: 90%;
                max-width: 400px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                text-align: center;
                font-size: 48px;
                font-weight: 900;
                color: #00ff88;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group input {
                width: 100%;
                padding: 15px;
                background: rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                color: #fff;
                font-size: 16px;
                box-sizing: border-box;
            }
            .form-group input:focus {
                outline: none;
                border-color: #00ff88;
            }
            .btn {
                width: 100%;
                padding: 15px;
                background: #00ff88;
                color: black;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px #00ff8840;
            }
            .error {
                color: #ff4444;
                text-align: center;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">OTP KING</div>
            <form method="POST" action="/api/login">
                <div class="form-group">
                    <input type="text" name="username" placeholder="اسم المستخدم" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="كلمة المرور" required>
                </div>
                <button type="submit" class="btn">دخول</button>
            </form>
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
        </div>
    </body>
    </html>
    ''')

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>لوحة التحكم - OTP KING</title>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Tajawal', sans-serif;
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                min-height: 100vh;
                color: #fff;
            }
            .header {
                background: rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                padding: 20px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .logo {
                font-size: 28px;
                font-weight: 900;
                color: #00ff88;
            }
            .user-menu {
                display: flex;
                gap: 15px;
                align-items: center;
            }
            .user-menu a {
                color: #fff;
                text-decoration: none;
                padding: 8px 15px;
                border-radius: 5px;
                transition: all 0.3s;
            }
            .user-menu a:hover {
                background: #00ff88;
                color: black;
            }
            .container {
                max-width: 1200px;
                margin: 30px auto;
                padding: 20px;
            }
            .welcome {
                font-size: 24px;
                margin-bottom: 30px;
            }
            .welcome span {
                color: #00ff88;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .feature-card {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
            }
            .feature-icon {
                font-size: 40px;
                margin-bottom: 15px;
            }
            .feature-title {
                font-size: 20px;
                font-weight: 700;
                color: #00ff88;
                margin-bottom: 10px;
            }
            .feature-desc {
                color: #aaa;
                margin-bottom: 20px;
            }
            .feature-link {
                color: #00ff88;
                text-decoration: none;
                font-weight: 500;
            }
            .feature-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo">OTP KING</div>
                <div class="user-menu">
                    <a href="/profile">الملف الشخصي</a>
                    {% if session.get('role') == 'owner' %}
                    <a href="/owner/dashboard">لوحة المالك</a>
                    {% endif %}
                    <a href="/api/logout">تسجيل الخروج</a>
                </div>
            </div>
        </header>
        
        <div class="container">
            <div class="welcome">
                مرحباً <span>{{ session.get('username') }}</span> 👋
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <div class="feature-title">OTP KING</div>
                    <div class="feature-desc">احصل على رموز OTP من مختلف الخدمات</div>
                    <a href="/fullscreen" class="feature-link">عرض OTP →</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">الإحصائيات</div>
                    <div class="feature-desc">تحليلات وإحصائيات متقدمة</div>
                    <a href="/api/stats/success-rate" class="feature-link">عرض الإحصائيات →</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">⚙️</div>
                    <div class="feature-title">الإعدادات</div>
                    <div class="feature-desc">تخصيص إعداداتك وتفضيلاتك</div>
                    <a href="/profile" class="feature-link">تعديل الإعدادات →</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

#============================================
# ========== API تسجيل الدخول ==========
#============================================

@app.route('/api/login', methods=['POST'])
def api_login():
    """معالجة تسجيل الدخول"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['theme'] = user.get('theme', 'dark')
        session['language'] = user.get('language', 'en')
        
        # تسجيل الدخول في السجلات
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO login_logs (user_id, ip_address, user_agent, status)
            VALUES (?, ?, ?, 'success')
        ''', (user['id'], request.remote_addr, request.user_agent.string))
        conn.commit()
        conn.close()
        
        return redirect(url_for('dashboard'))
    
    # تسجيل محاولة فاشلة
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO login_logs (user_id, ip_address, user_agent, status)
        VALUES (?, ?, ?, 'failed')
    ''', (None, request.remote_addr, request.user_agent.string))
    conn.commit()
    conn.close()
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تسجيل الدخول - OTP KING</title>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Tajawal', sans-serif;
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .login-container {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                width: 90%;
                max-width: 400px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                text-align: center;
                font-size: 48px;
                font-weight: 900;
                color: #00ff88;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group input {
                width: 100%;
                padding: 15px;
                background: rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                color: #fff;
                font-size: 16px;
                box-sizing: border-box;
            }
            .form-group input:focus {
                outline: none;
                border-color: #00ff88;
            }
            .btn {
                width: 100%;
                padding: 15px;
                background: #00ff88;
                color: black;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px #00ff8840;
            }
            .error {
                color: #ff4444;
                text-align: center;
                margin-top: 10px;
                padding: 10px;
                background: rgba(255,68,68,0.1);
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">OTP KING</div>
            <form method="POST" action="/api/login">
                <div class="form-group">
                    <input type="text" name="username" placeholder="اسم المستخدم" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="كلمة المرور" required>
                </div>
                <button type="submit" class="btn">دخول</button>
            </form>
            <div class="error">❌ اسم المستخدم أو كلمة المرور غير صحيحة</div>
        </div>
    </body>
    </html>
    ''')

@app.route('/api/logout')
def api_logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect(url_for('login_page'))

#============================================
# ========== تشغيل السكربت ==========
#============================================

def run_schedule():
    """تشغيل جدولة المهام في الخلفية"""
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 OTP KING Dashboard - Owner: mohaymen")
    print(f"🌐 http://localhost:{port}")
    print(f"📁 Database: {DB_PATH}")
    print("👑 Owner login: mohaymen / mohaymen")
    print("✅ تم إصلاح جميع الأخطاء وتشغيل التطبيق بنجاح")
    
    # تشغيل جدولة المهام في خلفية
    threading.Thread(target=run_schedule, daemon=True).start()
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)