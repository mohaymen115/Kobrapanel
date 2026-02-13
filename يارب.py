
# ============================================
# OTP KING - النسخة الكاملة جداً (الجزء 1)
# ============================================

import os
import sys
import logging
import requests
import re
import hashlib
import json
import sqlite3
import time
import threading
import random
import string
import secrets
import hmac
import base64
import smtplib
import qrcode
import pyotp
import schedule
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash, make_response, send_file
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from user_agents import parse
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

load_dotenv()

# ============================================
# إعدادات التسجيل
# ============================================

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# إعدادات Flask
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'otp-king-super-secret-key-2026-very-long-and-secure'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_SECURE'] = False  # مهم لـ Railway
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}

# SocketIO للتحديثات المباشرة
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================
# إعدادات قاعدة البيانات
# ============================================

DB_PATH = 'database.db'
BACKUP_FOLDER = 'backups'
STATIC_FOLDER = 'static'
UPLOAD_FOLDER = 'static/uploads'
AVATAR_FOLDER = 'static/avatars'
SOUNDS_FOLDER = 'static/sounds'

# إنشاء المجلدات المطلوبة
for folder in [BACKUP_FOLDER, STATIC_FOLDER, UPLOAD_FOLDER, AVATAR_FOLDER, SOUNDS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ============================================
# المتغيرات العامة
# ============================================

all_messages = []
active_users = {}
bot_stats = {
    'is_running': True,
    'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_otps': 0,
    'online_users': 0,
    'start_time': datetime.now()
}

# ============================================
# دوال مساعدة
# ============================================

def get_db():
    """الحصول على اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def allowed_file(filename):
    """التحقق من صيغة الملف"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def log_error(error_type, error_message, traceback=None):
    """تسجيل الأخطاء"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO error_logs (error_type, error_message, traceback, url, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (error_type, error_message, traceback, request.path, session.get('user_id')))
        conn.commit()
        conn.close()
    except:
        pass

def send_notification(user_id, title, message, type='info'):
    """إرسال إشعار"""
    try:
        socketio.emit(f'notification_{user_id}', {
            'title': title,
            'message': message,
            'type': type,
            'time': datetime.now().strftime('%H:%M')
        })
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, message, type))
        conn.commit()
        conn.close()
    except:
        pass

def log_action(user_id, action, details=None):
    """تسجيل الإجراءات"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_actions (user_id, action, details, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, action, details, request.remote_addr, request.headers.get('User-Agent')))
        conn.commit()
        conn.close()
    except:
        pass

# ============================================
# Decorators
# ============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'unauthorized', 'redirect': url_for('login_page')}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        if session.get('role') not in ['admin', 'owner']:
            return render_template_string(ERROR_PAGE, error="⛔ هذه الصفحة للمشرفين فقط"), 403
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        if session.get('role') != 'owner':
            return render_template_string(ERROR_PAGE, error="⛔ هذه الصفحة للمالك فقط"), 403
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login_page'))
            
            user_role = session.get('role', 'user')
            if not PermissionManager.has_permission(user_role, permission):
                return render_template_string(ERROR_PAGE, error="⛔ لا تملك الصلاحية"), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================
# إدارة الصلاحيات
# ============================================

class PermissionManager:
    ROLES = {
        'owner': ['*'],
        'admin': [
            'view_dashboard', 'view_users', 'manage_users', 
            'view_stats', 'manage_panel', 'export_data',
            'view_logs', 'manage_settings', 'manage_ads'
        ],
        'mod': [
            'view_dashboard', 'view_users', 'view_stats',
            'view_logs', 'manage_messages'
        ],
        'vip': [
            'view_dashboard', 'view_advanced_stats', 'export_data',
            'no_ads', 'priority_support'
        ],
        'user': [
            'view_dashboard', 'view_basic_stats'
        ]
    }
    
    @staticmethod
    def has_permission(user_role, permission):
        if user_role == 'owner':
            return True
        if user_role not in PermissionManager.ROLES:
            return False
        return permission in PermissionManager.ROLES[user_role]
    
    @staticmethod
    def get_role_permissions(role):
        return PermissionManager.ROLES.get(role, [])

# ============================================
# إدارة الجلسات
# ============================================

class SessionManager:
    @staticmethod
    def create_session(user_id, user_agent, ip):
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=30)
        
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
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE user_sessions SET is_active=0 WHERE session_token=?", (session_token,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_sessions(user_id):
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

# ============================================
# المصادقة الثنائية (2FA)
# ============================================

class TwoFactorAuth:
    @staticmethod
    def generate_secret():
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code(username, secret):
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(username, issuer_name="OTP KING")
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        return base64.b64encode(buffered.getvalue()).decode()
    
    @staticmethod
    def verify_code(secret, code):
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    
    @staticmethod
    def generate_backup_codes():
        codes = []
        for _ in range(10):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            hashed = hashlib.sha256(code.encode()).hexdigest()
            codes.append({'code': code, 'hashed': hashed, 'used': False})
        return codes

# ============================================
# حظر IP
# ============================================

class IPBlocker:
    def __init__(self):
        self.blocked_ips = set()
        self.failed_attempts = {}
        self.max_attempts = 5
        self.block_time = 30  # دقيقة
    
    def add_failed_attempt(self, ip):
        now = datetime.now()
        
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = {'count': 0, 'first_attempt': now}
        
        self.failed_attempts[ip]['count'] += 1
        
        if self.failed_attempts[ip]['count'] >= self.max_attempts:
            if now - self.failed_attempts[ip]['first_attempt'] < timedelta(minutes=10):
                self.block_ip(ip, f"{self.max_attempts} محاولات فاشلة")
                return True
            else:
                self.failed_attempts[ip] = {'count': 1, 'first_attempt': now}
        
        return False
    
    def block_ip(self, ip, reason="محاولات متكررة"):
        self.blocked_ips.add(ip)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO blocked_ips (ip_address, reason, blocked_until)
            VALUES (?, ?, datetime('now', '+? minutes'))
        ''', (ip, reason, self.block_time))
        conn.commit()
        conn.close()
        
        logger.warning(f"🚫 تم حظر IP: {ip} - {reason}")
    
    def is_blocked(self, ip):
        if ip in self.blocked_ips:
            return True
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT * FROM blocked_ips 
            WHERE ip_address=? AND (blocked_until > datetime('now') OR blocked_until IS NULL)
        ''', (ip,))
        blocked = c.fetchone()
        conn.close()
        
        if blocked:
            self.blocked_ips.add(ip)
            return True
        
        return False
    
    def unblock_ip(self, ip):
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE blocked_ips 
            SET unblocked_at=datetime('now') 
            WHERE ip_address=? AND unblocked_at IS NULL
        ''', (ip,))
        conn.commit()
        conn.close()

ip_blocker = IPBlocker()
```

الجزء 2: الثيمات والترجمة

```python
# ============================================
# الثيمات
# ============================================

THEMES = {
    'dark': {
        'name': 'داكن',
        'name_en': 'Dark',
        'bg': 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
        'card_bg': 'rgba(255,255,255,0.08)',
        'card_hover': 'rgba(255,255,255,0.12)',
        'text': '#fff',
        'text_secondary': '#aaa',
        'accent': '#00ff88',
        'accent_hover': '#00cc6a',
        'danger': '#ff4444',
        'warning': '#ffbb33',
        'info': '#33b5e5',
        'border': 'rgba(255,255,255,0.1)',
        'shadow': '0 8px 32px rgba(0,0,0,0.4)'
    },
    'light': {
        'name': 'فاتح',
        'name_en': 'Light',
        'bg': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'card_bg': 'rgba(255,255,255,0.9)',
        'card_hover': 'rgba(255,255,255,0.95)',
        'text': '#333',
        'text_secondary': '#666',
        'accent': '#0077ff',
        'accent_hover': '#0055cc',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8',
        'border': 'rgba(0,0,0,0.1)',
        'shadow': '0 8px 32px rgba(0,0,0,0.1)'
    },
    'blue': {
        'name': 'أزرق',
        'name_en': 'Blue',
        'bg': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
        'card_bg': 'rgba(255,255,255,0.1)',
        'card_hover': 'rgba(255,255,255,0.15)',
        'text': '#fff',
        'text_secondary': '#ccc',
        'accent': '#64b5f6',
        'accent_hover': '#42a5f5',
        'danger': '#ff4444',
        'warning': '#ffbb33',
        'info': '#4fc3f7',
        'border': 'rgba(255,255,255,0.2)',
        'shadow': '0 8px 32px rgba(0,0,0,0.3)'
    },
    'purple': {
        'name': 'بنفسجي',
        'name_en': 'Purple',
        'bg': 'linear-gradient(135deg, #654ea3 0%, #eaafc8 100%)',
        'card_bg': 'rgba(255,255,255,0.1)',
        'card_hover': 'rgba(255,255,255,0.15)',
        'text': '#fff',
        'text_secondary': '#eee',
        'accent': '#d291bc',
        'accent_hover': '#c06b9f',
        'danger': '#ff4444',
        'warning': '#ffbb33',
        'info': '#9b59b6',
        'border': 'rgba(255,255,255,0.2)',
        'shadow': '0 8px 32px rgba(0,0,0,0.3)'
    },
    'green': {
        'name': 'أخضر',
        'name_en': 'Green',
        'bg': 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        'card_bg': 'rgba(255,255,255,0.1)',
        'card_hover': 'rgba(255,255,255,0.15)',
        'text': '#fff',
        'text_secondary': '#eee',
        'accent': '#f1c40f',
        'accent_hover': '#f39c12',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db',
        'border': 'rgba(255,255,255,0.2)',
        'shadow': '0 8px 32px rgba(0,0,0,0.3)'
    }
}

# ============================================
# الترجمة
# ============================================

TRANSLATIONS = {
    'ar': {
        # عام
        'app_name': 'OTP KING',
        'dashboard': 'لوحة التحكم',
        'home': 'الرئيسية',
        'profile': 'الملف الشخصي',
        'settings': 'الإعدادات',
        'logout': 'تسجيل الخروج',
        'login': 'تسجيل الدخول',
        'register': 'تسجيل جديد',
        'search': 'بحث',
        'filter': 'تصفية',
        'export': 'تصدير',
        'import': 'استيراد',
        'refresh': 'تحديث',
        'save': 'حفظ',
        'cancel': 'إلغاء',
        'delete': 'حذف',
        'edit': 'تعديل',
        'add': 'إضافة',
        'create': 'إنشاء',
        'update': 'تحديث',
        'confirm': 'تأكيد',
        'back': 'رجوع',
        'next': 'التالي',
        'previous': 'السابق',
        'loading': 'جاري التحميل...',
        'error': 'خطأ',
        'success': 'نجاح',
        'warning': 'تحذير',
        'info': 'معلومات',
        
        # OTP
        'total_otps': 'إجمالي OTP',
        'new_otp': 'OTP جديد',
        'otp_code': 'رمز OTP',
        'phone': 'رقم الهاتف',
        'service': 'الخدمة',
        'country': 'الدولة',
        'timestamp': 'الوقت',
        'copy': 'نسخ',
        'copied': 'تم النسخ',
        'no_messages': 'لا توجد رسائل',
        'waiting': 'في انتظار OTP...',
        'last_check': 'آخر فحص',
        'force_check': 'فحص يدوي',
        'clear_all': 'مسح الكل',
        
        # الحالة
        'online': 'متصل',
        'offline': 'غير متصل',
        'away': 'بعيد',
        'busy': 'مشغول',
        'last_seen': 'آخر ظهور',
        'member_since': 'عضو منذ',
        
        # الإعدادات
        'language': 'اللغة',
        'theme': 'الثيم',
        'notifications': 'الإشعارات',
        'sound': 'الصوت',
        'privacy': 'الخصوصية',
        'security': 'الأمان',
        'account': 'الحساب',
        
        # المستخدمين
        'username': 'اسم المستخدم',
        'password': 'كلمة المرور',
        'email': 'البريد الإلكتروني',
        'phone_number': 'رقم الهاتف',
        'role': 'الصلاحية',
        'status': 'الحالة',
        'actions': 'الإجراءات',
        'block': 'حظر',
        'unblock': 'إلغاء الحظر',
        'suspend': 'تعليق',
        'activate': 'تفعيل',
        
        # الإحصائيات
        'statistics': 'الإحصائيات',
        'charts': 'الرسوم البيانية',
        'daily': 'يومي',
        'weekly': 'أسبوعي',
        'monthly': 'شهري',
        'yearly': 'سنوي',
        'total_users': 'إجمالي المستخدمين',
        'active_users': 'المستخدمين النشطين',
        'new_users': 'مستخدمين جدد',
        'success_rate': 'نسبة النجاح',
        'top_countries': 'أكثر الدول',
        'top_services': 'أكثر الخدمات',
        
        # الأخطاء
        'error_403': 'غير مصرح بالوصول',
        'error_404': 'الصفحة غير موجودة',
        'error_500': 'خطأ في الخادم',
        'error_429': 'طلبات كثيرة جداً',
        
        # الوقت
        'just_now': 'الآن',
        'minutes_ago': 'منذ {} دقيقة',
        'hours_ago': 'منذ {} ساعة',
        'days_ago': 'منذ {} يوم',
        'weeks_ago': 'منذ {} أسبوع',
        'months_ago': 'منذ {} شهر',
        'years_ago': 'منذ {} سنة',
        
        # أيام الأسبوع
        'monday': 'الإثنين',
        'tuesday': 'الثلاثاء',
        'wednesday': 'الأربعاء',
        'thursday': 'الخميس',
        'friday': 'الجمعة',
        'saturday': 'السبت',
        'sunday': 'الأحد',
        
        # شهور السنة
        'january': 'يناير',
        'february': 'فبراير',
        'march': 'مارس',
        'april': 'أبريل',
        'may': 'مايو',
        'june': 'يونيو',
        'july': 'يوليو',
        'august': 'أغسطس',
        'september': 'سبتمبر',
        'october': 'أكتوبر',
        'november': 'نوفمبر',
        'december': 'ديسمبر',
    },
    
    'en': {
        # General
        'app_name': 'OTP KING',
        'dashboard': 'Dashboard',
        'home': 'Home',
        'profile': 'Profile',
        'settings': 'Settings',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import',
        'refresh': 'Refresh',
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'create': 'Create',
        'update': 'Update',
        'confirm': 'Confirm',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'info': 'Info',
        
        # OTP
        'total_otps': 'Total OTPs',
        'new_otp': 'New OTP',
        'otp_code': 'OTP Code',
        'phone': 'Phone',
        'service': 'Service',
        'country': 'Country',
        'timestamp': 'Time',
        'copy': 'Copy',
        'copied': 'Copied',
        'no_messages': 'No messages',
        'waiting': 'Waiting for OTP...',
        'last_check': 'Last Check',
        'force_check': 'Force Check',
        'clear_all': 'Clear All',
        
        # Status
        'online': 'Online',
        'offline': 'Offline',
        'away': 'Away',
        'busy': 'Busy',
        'last_seen': 'Last Seen',
        'member_since': 'Member Since',
        
        # Settings
        'language': 'Language',
        'theme': 'Theme',
        'notifications': 'Notifications',
        'sound': 'Sound',
        'privacy': 'Privacy',
        'security': 'Security',
        'account': 'Account',
        
        # Users
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'phone_number': 'Phone Number',
        'role': 'Role',
        'status': 'Status',
        'actions': 'Actions',
        'block': 'Block',
        'unblock': 'Unblock',
        'suspend': 'Suspend',
        'activate': 'Activate',
        
        # Statistics
        'statistics': 'Statistics',
        'charts': 'Charts',
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'yearly': 'Yearly',
        'total_users': 'Total Users',
        'active_users': 'Active Users',
        'new_users': 'New Users',
        'success_rate': 'Success Rate',
        'top_countries': 'Top Countries',
        'top_services': 'Top Services',
        
        # Errors
        'error_403': 'Access Denied',
        'error_404': 'Page Not Found',
        'error_500': 'Server Error',
        'error_429': 'Too Many Requests',
        
        # Time
        'just_now': 'Just now',
        'minutes_ago': '{} minutes ago',
        'hours_ago': '{} hours ago',
        'days_ago': '{} days ago',
        'weeks_ago': '{} weeks ago',
        'months_ago': '{} months ago',
        'years_ago': '{} years ago',
        
        # Week days
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',
        
        # Months
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
    }
}

def get_text(key, **kwargs):
    """الحصول على النص حسب اللغة"""
    lang = session.get('language', 'ar')
    text = TRANSLATIONS.get(lang, {}).get(key, key)
    
    if kwargs:
        text = text.format(**kwargs)
    
    return text

# ============================================
# معالج الطلبات
# ============================================

@app.before_request
def before_request_handler():
    """معالج الطلبات قبل التنفيذ"""
    
    # التحقق من حظر IP
    if ip_blocker.is_blocked(request.remote_addr):
        return render_template_string(ERROR_PAGE, error=get_text('error_429')), 429
    
    # تحديث آخر ظهور
    if 'user_id' in session:
        try:
            conn = get_db()
            c = conn.cursor()
            c.execute('''
                UPDATE users 
                SET last_seen=datetime('now'), is_online=1 
                WHERE id=?
            ''', (session['user_id'],))
            conn.commit()
            conn.close()
            
            # تحديث إحصائيات المستخدمين النشطين
            active_users[session['user_id']] = time.time()
        except:
            pass
    
    # مسارات عامة
    public_paths = ['/', '/login', '/api/login', '/register', '/api/register', 
                    '/static/', '/api/public', '/health', '/favicon.ico']
    
    for path in public_paths:
        if request.path.startswith(path):
            if request.path in ['/', '/login'] and 'user_id' in session:
                return redirect(url_for('dashboard'))
            return
    
    # التحقق من وضع الصيانة
    if request.path.startswith('/owner') and session.get('role') == 'owner':
        return
    
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT maintenance_mode FROM system_settings WHERE id=1")
        setting = c.fetchone()
        conn.close()
        
        if setting and setting['maintenance_mode'] and 'user_id' not in session:
            return render_template_string(MAINTENANCE_PAGE), 503
    except:
        pass

@app.after_request
def after_request_handler(response):
    """معالج الطلبات بعد التنفيذ"""
    
    # إضافة headers أمنية
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

# ============================================
# مسار الصحة
# ============================================

@app.route('/health')
def health_check():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': str(datetime.now() - bot_stats['start_time']),
        'version': '2.0.0'
    })
```

الجزء 3: صفحات HTML الرئيسية

```python
# ============================================
# قوالب HTML
# ============================================

LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول - OTP KING</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        /* خلفية متحركة */
        .bg-bubbles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }
        
        .bg-bubbles li {
            position: absolute;
            list-style: none;
            display: block;
            width: 40px;
            height: 40px;
            background-color: rgba(255, 255, 255, 0.15);
            bottom: -160px;
            animation: square 25s infinite;
            transition-timing-function: linear;
            border-radius: 50%;
        }
        
        .bg-bubbles li:nth-child(1) {
            left: 10%;
            width: 80px;
            height: 80px;
            animation-delay: 0s;
        }
        
        .bg-bubbles li:nth-child(2) {
            left: 20%;
            width: 40px;
            height: 40px;
            animation-delay: 2s;
            animation-duration: 17s;
        }
        
        .bg-bubbles li:nth-child(3) {
            left: 25%;
            width: 120px;
            height: 120px;
            animation-delay: 4s;
        }
        
        .bg-bubbles li:nth-child(4) {
            left: 40%;
            width: 60px;
            height: 60px;
            animation-duration: 22s;
            background-color: rgba(255, 255, 255, 0.25);
        }
        
        .bg-bubbles li:nth-child(5) {
            left: 70%;
            width: 100px;
            height: 100px;
            animation-delay: 0s;
        }
        
        .bg-bubbles li:nth-child(6) {
            left: 80%;
            width: 70px;
            height: 70px;
            animation-delay: 3s;
        }
        
        @keyframes square {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(-1000px) rotate(720deg);
                opacity: 0;
            }
        }
        
        /* حاوية تسجيل الدخول */
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 50px 40px;
            width: 90%;
            max-width: 450px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 10;
            animation: slideUp 0.6s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* الشعار */
        .logo {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo h1 {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .logo p {
            color: #666;
            font-size: 16px;
        }
        
        /* حقول الإدخال */
        .input-group {
            margin-bottom: 25px;
            position: relative;
        }
        
        .input-group i {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
            font-size: 18px;
            transition: all 0.3s;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px 50px 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            font-family: 'Tajawal', sans-serif;
            transition: all 0.3s;
            background: white;
        }
        
        .input-group input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            outline: none;
        }
        
        .input-group input:focus + i {
            color: #667eea;
        }
        
        /* تذكرني */
        .remember {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
        }
        
        .remember label {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            cursor: pointer;
        }
        
        .remember input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: #667eea;
        }
        
        .forgot-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .forgot-link:hover {
            color: #764ba2;
        }
        
        /* زر تسجيل الدخول */
        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 25px;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .login-btn:active {
            transform: translateY(0);
        }
        
        /* معلومات التجربة */
        .demo-info {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .demo-info p {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .demo-info .demo-account {
            background: white;
            padding: 10px;
            border-radius: 8px;
            font-family: monospace;
            color: #333;
        }
        
        .demo-info .demo-account span {
            color: #667eea;
            font-weight: bold;
        }
        
        /* حقوق النشر */
        .copyright {
            text-align: center;
            margin-top: 30px;
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
        }
        
        /* رسائل الخطأ */
        .error-message {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            border-right: 4px solid #c33;
            animation: shake 0.5s;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        /* مؤشر التحميل */
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* أيقونات */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    </style>
</head>
<body>
    <ul class="bg-bubbles">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </ul>
    
    <div class="login-container">
        <div class="logo">
            <h1>👑 OTP KING</h1>
            <p>نظام إدارة رموز OTP المتقدم</p>
        </div>
        
        {% if error %}
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            {{ error }}
        </div>
        {% endif %}
        
        <form method="POST" action="/api/login" id="loginForm">
            <div class="input-group">
                <i class="fas fa-user"></i>
                <input type="text" name="username" placeholder="اسم المستخدم" required autofocus>
            </div>
            
            <div class="input-group">
                <i class="fas fa-lock"></i>
                <input type="password" name="password" placeholder="كلمة المرور" required>
            </div>
            
            <div class="remember">
                <label>
                    <input type="checkbox" name="remember"> تذكرني
                </label>
                <a href="#" class="forgot-link">نسيت كلمة المرور؟</a>
            </div>
            
            <button type="submit" class="login-btn" id="loginBtn">
                <span>تسجيل الدخول</span>
                <i class="fas fa-arrow-left" style="margin-right: 10px;"></i>
            </button>
            
            <div class="loading" id="loading">
                <div class="loading-spinner"></div>
                <p style="margin-top: 10px; color: #666;">جاري التحقق...</p>
            </div>
        </form>
        
        <div class="demo-info">
            <p><i class="fas fa-info-circle"></i> معلومات الدخول التجريبي:</p>
            <div class="demo-account">
                <span>👤 اسم المستخدم:</span> mohaymen<br>
                <span>🔑 كلمة المرور:</span> mohaymen
            </div>
        </div>
    </div>
    
    <div class="copyright">
        © 2026 OTP KING - جميع الحقوق محفوظة
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            const btn = document.getElementById('loginBtn');
            const loading = document.getElementById('loading');
            
            btn.style.display = 'none';
            loading.style.display = 'block';
        });
    </script>
</body>
</html>
'''

DASHBOARD_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - OTP KING</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        /* الشريط العلوي */
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 15px 0;
        }
        
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-links {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .nav-links a {
            color: #333;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 8px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .nav-links a:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .nav-links a i {
            font-size: 16px;
        }
        
        .user-badge {
            background: #f0f0f0;
            padding: 8px 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .user-badge .role {
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 20px;
            font-size: 12px;
        }
        
        /* الحاوية الرئيسية */
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        
        /* بطاقة الترحيب */
        .welcome-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .welcome-text h2 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .welcome-text p {
            color: #666;
        }
        
        .online-badge {
            background: #28a745;
            color: white;
            padding: 8px 20px;
            border-radius: 30px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        
        .online-badge i {
            font-size: 10px;
        }
        
        /* إحصائيات سريعة */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            border-radius: 50%;
            transform: translate(30px, -30px);
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
        }
        
        .stat-icon i {
            font-size: 24px;
            color: white;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 900;
            color: #333;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
        }
        
        .stat-change {
            margin-top: 10px;
            font-size: 12px;
            color: #28a745;
        }
        
        /* شبكة الميزات */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
            transition: all 0.3s;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }
        
        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        .feature-icon i {
            font-size: 30px;
            color: white;
        }
        
        .feature-card h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 20px;
        }
        
        .feature-card p {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .feature-link {
            color: #667eea;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        /* النشاطات الأخيرة */
        .activity-section {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .section-header h3 {
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .view-all {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .activity-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .activity-item {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 12px;
            transition: all 0.3s;
        }
        
        .activity-item:hover {
            background: #f0f0f0;
        }
        
        .activity-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .activity-content {
            flex: 1;
        }
        
        .activity-text {
            color: #333;
            margin-bottom: 5px;
        }
        
        .activity-time {
            color: #999;
            font-size: 12px;
        }
        
        /* أيقونات */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">👑 OTP KING</div>
            <div class="nav-links">
                <a href="/dashboard"><i class="fas fa-home"></i> الرئيسية</a>
                <a href="/profile"><i class="fas fa-user"></i> الملف الشخصي</a>
                {% if session.get('role') == 'owner' %}
                <a href="/owner/dashboard"><i class="fas fa-crown"></i> لوحة المالك</a>
                {% endif %}
                <div class="user-badge">
                    <i class="fas fa-user"></i>
                    <span>{{ session.get('username') }}</span>
                    <span class="role">{{ session.get('role') }}</span>
                </div>
                <a href="/api/logout"><i class="fas fa-sign-out-alt"></i> خروج</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="welcome-card">
            <div class="welcome-text">
                <h2>مرحباً {{ session.get('username') }} 👋</h2>
                <p>نرحب بك في لوحة تحكم OTP KING المتطورة</p>
            </div>
            <div class="online-badge">
                <i class="fas fa-circle"></i> متصل الآن
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-key"></i>
                </div>
                <div class="stat-value">0</div>
                <div class="stat-label">إجمالي OTP</div>
                <div class="stat-change">
                    <i class="fas fa-arrow-up"></i> +0 اليوم
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-value">1</div>
                <div class="stat-label">المستخدمين</div>
                <div class="stat-change">
                    <i class="fas fa-check-circle"></i> نشط
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-value">100%</div>
                <div class="stat-label">نسبة النجاح</div>
                <div class="stat-change">
                    <i class="fas fa-star"></i> ممتاز
                </div>
            </div>
        </div>
        
        <div class="features-grid">
            <a href="/fullscreen" class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-eye"></i>
                </div>
                <h3>عرض OTP</h3>
                <p>شاهد رموز OTP الواردة في الوقت الفعلي بواجهة ملء الشاشة</p>
                <div class="feature-link">
                    <span>عرض الآن</span>
                    <i class="fas fa-arrow-left"></i>
                </div>
            </a>
            
            <a href="/api/stats/success-rate" class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h3>الإحصائيات</h3>
                <p>تحليلات وإحصائيات متقدمة عن أداء النظام والخدمات</p>
                <div class="feature-link">
                    <span>عرض الإحصائيات</span>
                    <i class="fas fa-arrow-left"></i>
                </div>
            </a>
            
            <a href="/profile" class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-cog"></i>
                </div>
                <h3>الإعدادات</h3>
                <p>تخصيص إعداداتك الشخصية وتفضيلاتك في النظام</p>
                <div class="feature-link">
                    <span>تعديل الإعدادات</span>
                    <i class="fas fa-arrow-left"></i>
                </div>
            </a>
        </div>
        
        <div class="activity-section">
            <div class="section-header">
                <h3>
                    <i class="fas fa-history"></i>
                    آخر النشاطات
                </h3>
                <a href="#" class="view-all">عرض الكل <i class="fas fa-arrow-left"></i></a>
            </div>
            
            <div class="activity-list">
                <div class="activity-item">
                    <div class="activity-avatar">ن</div>
                    <div class="activity-content">
                        <div class="activity-text">تم تسجيل الدخول بنجاح</div>
                        <div class="activity-time">منذ لحظات</div>
                    </div>
                </div>
                
                <div class="activity-item">
                    <div class="activity-avatar">ن</div>
                    <div class="activity-content">
                        <div class="activity-text">تم تحديث الإعدادات</div>
                        <div class="activity-time">منذ ساعة</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .error-container {
            text-align: center;
            background: rgba(255,255,255,0.95);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 400px;
            width: 90%;
        }
        .error-icon {
            font-size: 80px;
            margin-bottom: 20px;
            color: #ff4444;
        }
        .error-message {
            color: #333;
            font-size: 24px;
            margin-bottom: 30px;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
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

MAINTENANCE_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>صيانة - OTP KING</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .maintenance-container {
            text-align: center;
            background: rgba(255,255,255,0.95);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 90%;
        }
        .icon {
            font-size: 80px;
            margin-bottom: 20px;
            color: #ffbb33;
        }
        h1 {
            color: #333;
            margin-bottom: 15px;
        }
        p {
            color: #666;
            margin-bottom: 30px;
            line-height: 1.8;
        }
        .loader {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="maintenance-container">
        <div class="icon">🔧</div>
        <h1>جاري الصيانة</h1>
        <p>نحن نعمل على تحسين النظام. سنعود قريباً!</p>
        <div class="loader"></div>
    </div>
</body>
</html>
'''
```

الجزء 4: مسارات API وإدارة قاعدة البيانات

```python
# ============================================
# مسارات API
# ============================================

@app.route('/api/login', methods=['POST'])
def api_login():
    """تسجيل الدخول"""
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'
    
    # التحقق من الكابتشا
    # captcha_id = request.form.get('captcha_id')
    # captcha_answer = request.form.get('captcha_answer')
    # if not CaptchaGenerator.verify_captcha(captcha_id, captcha_answer):
    #     return render_template_string(LOGIN_PAGE, error="❌ رمز التحقق غير صحيح")
    
    # التحقق من حظر IP
    if ip_blocker.is_blocked(request.remote_addr):
        return render_template_string(LOGIN_PAGE, error="❌ تم حظر عنوان IP الخاص بك مؤقتاً")
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    if user and user['password'] == password:  # في الإنتاج استخدم check_password_hash
        # إعادة تعيين محاولات الفاشلة
        if request.remote_addr in ip_blocker.failed_attempts:
            del ip_blocker.failed_attempts[request.remote_addr]
        
        # إنشاء الجلسة
        session.permanent = remember
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['theme'] = user.get('theme', 'dark')
        session['language'] = user.get('language', 'ar')
        
        # تسجيل الدخول
        c.execute('''
            INSERT INTO login_logs (user_id, ip_address, user_agent, status)
            VALUES (?, ?, ?, 'success')
        ''', (user['id'], request.remote_addr, request.headers.get('User-Agent')))
        
        # إنشاء جلسة جديدة
        session_token = SessionManager.create_session(
            user['id'],
            request.headers.get('User-Agent'),
            request.remote_addr
        )
        
        conn.commit()
        conn.close()
        
        # إرسال إشعار
        send_notification(user['id'], 'مرحباً بعودتك', f'تم تسجيل الدخول بنجاح من {request.remote_addr}')
        
        return redirect(url_for('dashboard'))
    
    # تسجيل محاولة فاشلة
    ip_blocker.add_failed_attempt(request.remote_addr)
    
    c.execute('''
        INSERT INTO login_logs (user_id, ip_address, user_agent, status)
        VALUES (?, ?, ?, 'failed')
    ''', (None, request.remote_addr, request.headers.get('User-Agent')))
    conn.commit()
    conn.close()
    
    return render_template_string(LOGIN_PAGE, error="❌ اسم المستخدم أو كلمة المرور غير صحيحة")

@app.route('/api/logout')
def api_logout():
    """تسجيل الخروج"""
    if 'user_id' in session:
        # تسجيل الخروج
        log_action(session['user_id'], 'logout', 'تسجيل الخروج')
        
        # إنهاء الجلسة
        # SessionManager.terminate_session(session.get('session_token'))
        
        # تحديث حالة الاتصال
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE users SET is_online=0 WHERE id=?", (session['user_id'],))
        conn.commit()
        conn.close()
        
        # إزالة من المستخدمين النشطين
        if session['user_id'] in active_users:
            del active_users[session['user_id']]
    
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/api/register', methods=['POST'])
def api_register():
    """تسجيل مستخدم جديد"""
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    
    if not username or not password:
        return jsonify({'error': 'الرجاء إدخال جميع الحقول'}), 400
    
    conn = get_db()
    c = conn.cursor()
    
    # التحقق من وجود المستخدم
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
    
    # إنشاء المستخدم الجديد
    c.execute('''
        INSERT INTO users (username, password, email, role)
        VALUES (?, ?, ?, 'user')
    ''', (username, password, email))
    
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'تم التسجيل بنجاح',
        'user_id': user_id
    })

@app.route('/api/user/status')
@login_required
def get_user_status():
    """الحصول على حالة المستخدم"""
    return jsonify({
        'online': True,
        'last_seen': datetime.now().isoformat(),
        'session_info': {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
    })

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    """تغيير كلمة المرور"""
    current = request.json.get('current_password')
    new = request.json.get('new_password')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE id=?", (session['user_id'],))
    user = c.fetchone()
    
    if user and user['password'] == current:
        c.execute("UPDATE users SET password=? WHERE id=?", (new, session['user_id']))
        conn.commit()
        conn.close()
        
        log_action(session['user_id'], 'change_password', 'تغيير كلمة المرور')
        
        return jsonify({'success': True, 'message': 'تم تغيير كلمة المرور بنجاح'})
    
    conn.close()
    return jsonify({'error': 'كلمة المرور الحالية غير صحيحة'}), 400

# ============================================
# مسارات الصفحات
# ============================================

@app.route('/')
@app.route('/login')
def login_page():
    """صفحة تسجيل الدخول"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template_string(LOGIN_PAGE)

@app.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم"""
    return render_template_string(DASHBOARD_PAGE)

@app.route('/profile')
@login_required
def profile():
    """الملف الشخصي"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT u.*, 
               (SELECT COUNT(*) FROM messages WHERE user_id=u.id) as total_otps,
               (SELECT COUNT(*) FROM user_actions WHERE user_id=u.id) as total_actions
        FROM users u
        WHERE u.id=?
    ''', (session['user_id'],))
    user = c.fetchone()
    
    # جلسات المستخدم
    c.execute('''
        SELECT * FROM user_sessions 
        WHERE user_id=? AND is_active=1 
        ORDER BY created_at DESC
    ''', (session['user_id'],))
    sessions = c.fetchall()
    
    conn.close()
    
    return render_template_string(PROFILE_PAGE, user=user, sessions=sessions)

@app.route('/fullscreen')
@login_required
def fullscreen_mode():
    """وضع ملء الشاشة"""
    return render_template_string(FULLSCREEN_PAGE, messages=all_messages)

# ============================================
# مسارات API للبيانات
# ============================================

@app.route('/api/stats/success-rate')
@login_required
def success_rate():
    """نسبة نجاح OTP"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as total FROM messages")
    total = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as used FROM messages WHERE is_used=1")
    used = c.fetchone()['used']
    
    conn.close()
    
    rate = (used / total * 100) if total > 0 else 0
    
    return jsonify({
        'total': total,
        'used': used,
        'rate': round(rate, 2)
    })

@app.route('/api/stats/daily')
@login_required
def daily_stats():
    """إحصائيات يومية"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM messages
        WHERE timestamp > date('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    ''')
    daily = c.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in daily])

@app.route('/api/stats/countries')
@login_required
def countries_stats():
    """إحصائيات الدول"""
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
    
    return jsonify([dict(row) for row in countries])

@app.route('/api/stats/services')
@login_required
def services_stats():
    """إحصائيات الخدمات"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT service, COUNT(*) as count
        FROM messages
        GROUP BY service
        ORDER BY count DESC
        LIMIT 10
    ''')
    services = c.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in services])

@app.route('/api/messages/recent')
@login_required
def recent_messages():
    """آخر الرسائل"""
    limit = request.args.get('limit', 50, type=int)
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM messages 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    messages = c.fetchall()
    conn.close()
    
    return jsonify([dict(msg) for msg in messages])

# ============================================
# مسارات التصدير
# ============================================

@app.route('/api/export/excel')
@login_required
def export_excel():
    """تصدير Excel"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    messages = c.fetchall()
    conn.close()
    
    df = pd.DataFrame([dict(msg) for msg in messages])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='OTP Data', index=False)
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=otp_data.xlsx'
    
    log_action(session['user_id'], 'export_excel', f'تصدير {len(messages)} رسالة')
    
    return response

@app.route('/api/export/json')
@login_required
def export_json():
    """تصدير JSON"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    messages = c.fetchall()
    conn.close()
    
    log_action(session['user_id'], 'export_json', f'تصدير {len(messages)} رسالة')
    
    return jsonify([dict(msg) for msg in messages])

@app.route('/api/export/csv')
@login_required
def export_csv():
    """تصدير CSV"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    messages = c.fetchall()
    conn.close()
    
    df = pd.DataFrame([dict(msg) for msg in messages])
    
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=otp_data.csv'
    
    return response

# ============================================
# مسارات البحث
# ============================================

@app.route('/api/search', methods=['POST'])
@login_required
def search_messages():
    """بحث في الرسائل"""
    query = request.json.get('query', '')
    
    if not query or len(query) < 3:
        return jsonify({'results': []})
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM messages 
        WHERE otp LIKE ? OR phone LIKE ? OR service LIKE ? OR country LIKE ? OR raw_message LIKE ?
        ORDER BY timestamp DESC
        LIMIT 100
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    
    results = c.fetchall()
    conn.close()
    
    return jsonify({
        'query': query,
        'count': len(results),
        'results': [dict(r) for r in results]
    })

# ============================================
# إعدادات المستخدم
# ============================================

@app.route('/api/settings/theme', methods=['POST'])
@login_required
def update_theme():
    """تحديث الثيم"""
    theme = request.json.get('theme')
    
    if theme not in THEMES:
        return jsonify({'error': 'ثيم غير موجود'}), 400
    
    session['theme'] = theme
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET theme=? WHERE id=?", (theme, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/settings/language', methods=['POST'])
@login_required
def update_language():
    """تحديث اللغة"""
    language = request.json.get('language')
    
    if language not in ['ar', 'en']:
        return jsonify({'error': 'لغة غير مدعومة'}), 400
    
    session['language'] = language
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET language=? WHERE id=?", (language, session['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/settings/notifications', methods=['POST'])
@login_required
def update_notifications():
    """تحديث إعدادات الإشعارات"""
    settings = request.json
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        UPDATE users 
        SET notify_email=?, notify_telegram=?, notify_browser=?, sound_enabled=?
        WHERE id=?
    ''', (
        settings.get('email', 0),
        settings.get('telegram', 0),
        settings.get('browser', 1),
        settings.get('sound', 1),
        session['user_id']
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ============================================
# مسارات المالك
# ============================================

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
    
    c.execute("SELECT COUNT(*) as total FROM users WHERE date(created_at) = date('now')")
    new_users_today = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as total FROM messages WHERE date(timestamp) = date('now')")
    new_messages_today = c.fetchone()['total']
    
    c.execute("SELECT COUNT(*) as total FROM users WHERE is_online=1")
    online_users = c.fetchone()['total']
    
    conn.close()
    
    return render_template_string(OWNER_PAGE, **locals())

@app.route('/owner/users')
@owner_required
def owner_users():
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
        'users': [dict(u) for u in users],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })

@app.route('/owner/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@owner_required
def manage_user(user_id):
    """إدارة مستخدم معين"""
    if request.method == 'GET':
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT u.*, 
                   (SELECT COUNT(*) FROM messages WHERE user_id=u.id) as total_otps,
                   (SELECT COUNT(*) FROM user_actions WHERE user_id=u.id) as total_actions,
                   (SELECT COUNT(*) FROM user_sessions WHERE user_id=u.id AND is_active=1) as active_sessions
            FROM users u
            WHERE u.id=?
        ''', (user_id,))
        user = c.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        return jsonify(dict(user))
    
    elif request.method == 'PUT':
        data = request.json
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE users 
            SET role=?, email=?, phone=?, suspended=?
            WHERE id=?
        ''', (
            data.get('role', 'user'),
            data.get('email'),
            data.get('phone'),
            data.get('suspended', 0),
            user_id
        ))
        conn.commit()
        conn.close()
        
        log_owner_action(session['user_id'], f'تحديث المستخدم {user_id}')
        
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        conn = get_db()
        c = conn.cursor()
        
        # التحقق من عدم حذف المالك
        c.execute("SELECT role FROM users WHERE id=?", (user_id,))
        user = c.fetchone()
        
        if user and user['role'] == 'owner':
            conn.close()
            return jsonify({'error': 'لا يمكن حذف المالك'}), 400
        
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        
        log_owner_action(session['user_id'], f'حذف المستخدم {user_id}')
        
        return jsonify({'success': True})

@app.route('/owner/stats')
@owner_required
def owner_stats():
    """إحصائيات شاملة للمالك"""
    conn = get_db()
    c = conn.cursor()
    
    # مستخدمين جدد آخر 30 يوم
    c.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM users
        WHERE created_at > date('now', '-30 days')
        GROUP BY DATE(created_at)
    ''')
    users_chart = c.fetchall()
    
    # رسائل آخر 30 يوم
    c.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM messages
        WHERE timestamp > date('now', '-30 days')
        GROUP BY DATE(timestamp)
    ''')
    messages_chart = c.fetchall()
    
    # أكثر الدول
    c.execute('''
        SELECT country, COUNT(*) as count
        FROM users
        WHERE country IS NOT NULL
        GROUP BY country
        ORDER BY count DESC
        LIMIT 10
    ''')
    top_countries = c.fetchall()
    
    # أكثر الخدمات
    c.execute('''
        SELECT service, COUNT(*) as count
        FROM messages
        GROUP BY service
        ORDER BY count DESC
        LIMIT 10
    ''')
    top_services = c.fetchall()
    
    conn.close()
    
    return jsonify({
        'users_chart': [dict(row) for row in users_chart],
        'messages_chart': [dict(row) for row in messages_chart],
        'top_countries': [dict(row) for row in top_countries],
        'top_services': [dict(row) for row in top_services]
    })

@app.route('/owner/logs')
@owner_required
def owner_logs():
    """سجلات النظام"""
    log_type = request.args.get('type', 'all')
    limit = request.args.get('limit', 100, type=int)
    
    conn = get_db()
    c = conn.cursor()
    
    if log_type == 'login':
        c.execute('''
            SELECT l.*, u.username 
            FROM login_logs l
            LEFT JOIN users u ON l.user_id = u.id
            ORDER BY l.login_time DESC
            LIMIT ?
        ''', (limit,))
    elif log_type == 'actions':
        c.execute('''
            SELECT a.*, u.username 
            FROM user_actions a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.action_time DESC
            LIMIT ?
        ''', (limit,))
    elif log_type == 'errors':
        c.execute('''
            SELECT * FROM error_logs 
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
    else:
        c.execute('''
            SELECT 'login' as type, l.login_time as time, l.status, u.username, l.ip_address
            FROM login_logs l
            LEFT JOIN users u ON l.user_id = u.id
            UNION ALL
            SELECT 'action' as type, a.action_time as time, a.action as status, u.username, a.ip_address
            FROM user_actions a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY time DESC
            LIMIT ?
        ''', (limit,))
    
    logs = c.fetchall()
    conn.close()
    
    return jsonify([dict(log) for log in logs])

@app.route('/owner/settings', methods=['GET', 'PUT'])
@owner_required
def owner_system_settings():
    """إعدادات النظام"""
    if request.method == 'GET':
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM system_settings WHERE id=1")
        settings = c.fetchone()
        conn.close()
        
        return jsonify(dict(settings) if settings else {})
    
    elif request.method == 'PUT':
        data = request.json
        
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE system_settings 
            SET site_name=?, maintenance_mode=?, maintenance_message=?, registration_enabled=?
            WHERE id=1
        ''', (
            data.get('site_name', 'OTP KING'),
            data.get('maintenance_mode', 0),
            data.get('maintenance_message', ''),
            data.get('registration_enabled', 1)
        ))
        conn.commit()
        conn.close()
        
        log_owner_action(session['user_id'], 'تحديث إعدادات النظام')
        
        return jsonify({'success': True})

@app.route('/owner/backup', methods=['POST'])
@owner_required
def create_backup():
    """إنشاء نسخة احتياطية"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'backup_{timestamp}.db'
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)
    
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
    
    log_owner_action(session['user_id'], f'إنشاء نسخة احتياطية: {backup_name}')
    
    return jsonify({
        'success': True,
        'backup': backup_name,
        'size': os.path.getsize(backup_path)
    })

@app.route('/owner/backups')
@owner_required
def list_backups():
    """قائمة النسخ الاحتياطية"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM backups ORDER BY created_at DESC")
    backups = c.fetchall()
    conn.close()
    
    return jsonify([dict(b) for b in backups])

@app.route('/owner/restore/<backup_name>', methods=['POST'])
@owner_required
def restore_backup(backup_name):
    """استعادة نسخة احتياطية"""
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)
    
    if not os.path.exists(backup_path):
        return jsonify({'error': 'الملف غير موجود'}), 404
    
    # إنشاء نسخة احتياطية قبل الاستعادة
    create_backup()
    
    # استعادة قاعدة البيانات
    import shutil
    shutil.copy2(backup_path, DB_PATH)
    
    log_owner_action(session['user_id'], f'استعادة نسخة: {backup_name}')
    
    return jsonify({'success': True})

# ============================================
# WebSocket للأشعارات المباشرة
# ============================================

@socketio.on('connect')
def handle_connect():
    """عند اتصال WebSocket"""
    if 'user_id' in session:
        emit('connected', {'status': 'مرحباً'})

@socketio.on('disconnect')
def handle_disconnect():
    """عند قطع WebSocket"""
    pass

@socketio.on('join_room')
def handle_join_room(room):
    """الانضمام لغرفة"""
    if 'user_id' in session:
        join_room(room)
        emit('joined', {'room': room})

# ============================================
# معالجة الأخطاء
# ============================================

@app.errorhandler(404)
def not_found_error(error):
    """صفحة غير موجودة"""
    return render_template_string(ERROR_PAGE, error="الصفحة غير موجودة"), 404

@app.errorhandler(403)
def forbidden_error(error):
    """ممنوع الوصول"""
    return render_template_string(ERROR_PAGE, error="غير مصرح بالوصول"), 403

@app.errorhandler(500)
def internal_error(error):
    """خطأ داخلي"""
    log_error('500', str(error))
    return render_template_string(ERROR_PAGE, error="خطأ داخلي في الخادم"), 500

@app.errorhandler(429)
def too_many_requests(error):
    """طلبات كثيرة"""
    return render_template_string(ERROR_PAGE, error="طلبات كثيرة جداً"), 429

# ============================================
# تهيئة قاعدة البيانات
# ============================================

def init_database():
    """تهيئة قاعدة البيانات مع جميع الجداول"""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        role TEXT DEFAULT 'user',
        theme TEXT DEFAULT 'dark',
        language TEXT DEFAULT 'ar',
        avatar TEXT,
        cover TEXT,
        country TEXT,
        last_seen TIMESTAMP,
        is_online INTEGER DEFAULT 0,
        suspended INTEGER DEFAULT 0,
        suspended_until TIMESTAMP,
        notify_email INTEGER DEFAULT 0,
        notify_telegram INTEGER DEFAULT 0,
        notify_browser INTEGER DEFAULT 1,
        sound_enabled INTEGER DEFAULT 1,
        twofa_secret TEXT,
        twofa_enabled INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_used INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول جلسات المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_token TEXT UNIQUE,
        user_agent TEXT,
        ip TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول سجلات الدخول
    c.execute('''CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        ip_address TEXT,
        user_agent TEXT,
        status TEXT,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول إجراءات المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS user_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        ip_address TEXT,
        user_agent TEXT,
        action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول سجلات الأخطاء
    c.execute('''CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type TEXT,
        error_message TEXT,
        traceback TEXT,
        url TEXT,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول عناوين IP المحظورة
    c.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE,
        reason TEXT,
        blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        blocked_until TIMESTAMP,
        unblocked_at TIMESTAMP
    )''')
    
    # جدول مفاتيح API
    c.execute('''CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        api_key TEXT UNIQUE,
        rate_limit INTEGER DEFAULT 100,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول سجلات API
    c.execute('''CREATE TABLE IF NOT EXISTS api_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_id INTEGER,
        endpoint TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (api_key_id) REFERENCES api_keys(id)
    )''')
    
    # جدول الإشعارات
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        message TEXT,
        type TEXT DEFAULT 'info',
        read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        read_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # جدول إعدادات النظام
    c.execute('''CREATE TABLE IF NOT EXISTS system_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT DEFAULT 'OTP KING',
        site_description TEXT,
        maintenance_mode INTEGER DEFAULT 0,
        maintenance_message TEXT,
        registration_enabled INTEGER DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # جدول النسخ الاحتياطي
    c.execute('''CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        path TEXT,
        size INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # إضافة المستخدم الافتراضي
    try:
        c.execute('''
            INSERT OR IGNORE INTO users 
            (id, username, password, role, email, theme, language) 
            VALUES (1, 'mohaymen', 'mohaymen', 'owner', 'admin@otpking.com', 'dark', 'ar')
        ''')
    except:
        pass
    
    # إضافة إعدادات النظام الافتراضية
    try:
        c.execute('''
            INSERT OR IGNORE INTO system_settings 
            (id, site_name, site_description, registration_enabled) 
            VALUES (1, 'OTP KING', 'نظام إدارة رموز OTP المتقدم', 1)
        ''')
    except:
        pass
    
    conn.commit()
    conn.close()
    print("✅ تم تهيئة قاعدة البيانات بنجاح مع جميع الجداول")

# تهيئة قاعدة البيانات
init_database()

# ============================================
# دوال مساعدة للمالك
# ============================================

def log_owner_action(owner_id, action):
    """تسجيل إجراءات المالك"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO owner_logs (owner_id, action, ip_address)
            VALUES (?, ?, ?)
        ''', (owner_id, action, request.remote_addr))
        conn.commit()
        conn.close()
    except:
        pass

# ============================================
# تشغيل المهام المجدولة
# ============================================

def cleanup_old_sessions():
    """تنظيف الجلسات القديمة"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE user_sessions 
            SET is_active=0 
            WHERE expires_at < datetime('now') OR last_activity < datetime('now', '-7 days')
        ''')
        conn.commit()
        conn.close()
        logger.info("✅ تم تنظيف الجلسات القديمة")
    except Exception as e:
        logger.error(f"❌ خطأ في تنظيف الجلسات: {e}")

def update_online_status():
    """تحديث حالة الاتصال"""
    try:
        # المستخدمين الذين لم يظهروا منذ 5 دقائق
        timeout = time.time() - 300  # 5 دقائق
        
        offline_users = []
        for user_id, last_seen in list(active_users.items()):
            if last_seen < timeout:
                offline_users.append(user_id)
                del active_users[user_id]
        
        if offline_users:
            conn = get_db()
            c = conn.cursor()
            placeholders = ','.join(['?'] * len(offline_users))
            c.execute(f'UPDATE users SET is_online=0 WHERE id IN ({placeholders})', offline_users)
            conn.commit()
            conn.close()
        
        # تحديث إحصائيات المستخدمين النشطين
        bot_stats['online_users'] = len(active_users)
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث الحالة: {e}")

def create_daily_backup():
    """إنشاء نسخة احتياطية يومية"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d')
        backup_name = f'daily_backup_{timestamp}.db'
        backup_path = os.path.join(BACKUP_FOLDER, backup_name)
        
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        
        # حذف النسخ الأقدم من 30 يوم
        import glob
        for old_backup in glob.glob(os.path.join(BACKUP_FOLDER, 'daily_backup_*')):
            if os.path.getctime(old_backup) < time.time() - 30 * 86400:
                os.remove(old_backup)
        
        logger.info(f"✅ تم إنشاء نسخة احتياطية يومية: {backup_name}")
    except Exception as e:
        logger.error(f"❌ خطأ في النسخ الاحتياطي: {e}")

# جدولة المهام
schedule.every(1).hours.do(cleanup_old_sessions)
schedule.every(5).minutes.do(update_online_status)
schedule.every().day.at("00:00").do(create_daily_backup)

def run_scheduler():
    """تشغيل المجدول في الخلفية"""
    while True:
        schedule.run_pending()
        time.sleep(60)

# بدء المجدول في Thread منفصل
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# ============================================
# تشغيل التطبيق
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("🚀 OTP KING - النسخة الكاملة والمدمجة")
    print("="*60)
    print(f"🌐 الرابط المحلي: http://localhost:{port}")
    print(f"📁 قاعدة البيانات: {DB_PATH}")
    print(f"📁 مجلد النسخ الاحتياطي: {BACKUP_FOLDER}")
    print("👤 مستخدم المالك: mohaymen / mohaymen")
    print("="*60)
    print("✅ جميع الأنظمة جاهزة:")
    print("   ✓ نظام المصادقة الثنائية (2FA)")
    print("   ✓ إدارة الجلسات والأجهزة")
    print("   ✓ حماية IP وحظر المتطفلين")
    print("   ✓ نسخ احتياطي تلقائي")
    print("   ✓ WebSocket للإشعارات المباشرة")
    print("   ✓ 5 ثيمات مختلفة")
    print("   ✓ ترجمة عربي/إنجليزي")
    print("="*60 + "\n")
    
    # تشغيل التطبيق
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)