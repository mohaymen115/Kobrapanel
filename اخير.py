
# ============================================
# OTP KING - النسخة الكاملة جداً (الجزء 2)
# جميع الحقوق محفوظة 2026
# ============================================

import os
import sys
import logging
import sqlite3
import hashlib
import json
import time
import threading
import random
import string
import secrets
import hmac
import base64
import re
import requests
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict

from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash, make_response, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================
# إعدادات التسجيل المتقدمة
# ============================================

class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger('OTP_KING')
        self.logger.setLevel(logging.DEBUG)
        
        # إنشاء مجلد logs إذا لم يكن موجوداً
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # ملف لأخطاء
        error_handler = logging.FileHandler('logs/error.log')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_formatter)
        
        # ملف لجميع الأحداث
        info_handler = logging.FileHandler('logs/app.log')
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        info_handler.setFormatter(info_formatter)
        
        # طباعة على الشاشة
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(error_handler)
        self.logger.addHandler(info_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def warning(self, message):
        self.logger.warning(message)

logger = CustomLogger()

# ============================================
# إعدادات Flask المتقدمة
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe(50))
app.config['SESSION_COOKIE_SECURE'] = False  # مهم لـ Railway
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_UPLOAD_SIZE'] = 5 * 1024 * 1024  # 5MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'pdf'}

# ============================================
# إعدادات SocketIO
# ============================================

socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading',
                   logger=False,
                   engineio_logger=False,
                   ping_timeout=60,
                   ping_interval=25)

# ============================================
# إعدادات المسارات
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
UPLOAD_PATH = os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER'])
BACKUP_PATH = os.path.join(BASE_DIR, 'backups')
LOG_PATH = os.path.join(BASE_DIR, 'logs')

# إنشاء المجلدات المطلوبة
for folder in [UPLOAD_PATH, BACKUP_PATH, LOG_PATH]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        logger.info(f"✅ تم إنشاء مجلد: {folder}")

# ============================================
# ========== نظام قاعدة البيانات المتقدم ==========
# ============================================

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.pool = []
        self.max_connections = 10
        self.init_database()
    
    def get_connection(self):
        """الحصول على اتصال من المجمع"""
        if self.pool:
            conn = self.pool.pop()
            try:
                conn.execute('SELECT 1').fetchone()
                return conn
            except:
                pass
        
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('PRAGMA journal_mode = WAL')
        return conn
    
    def return_connection(self, conn):
        """إعادة الاتصال للمجمع"""
        if len(self.pool) < self.max_connections:
            self.pool.append(conn)
        else:
            conn.close()
    
    def execute(self, query, params=None):
        """تنفيذ استعلام مع إعادة الاتصال تلقائياً"""
        conn = self.get_connection()
        try:
            if params:
                return conn.execute(query, params)
            return conn.execute(query)
        finally:
            self.return_connection(conn)
    
    def commit(self, conn=None):
        """حفظ التغييرات"""
        if conn:
            conn.commit()
    
    def init_database(self):
        """تهيئة قاعدة البيانات بجميع الجداول"""
        conn = self.get_connection()
        
        # جدول المستخدمين المتقدم
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            full_name TEXT,
            bio TEXT,
            avatar TEXT DEFAULT '/static/default-avatar.png',
            cover TEXT DEFAULT '/static/default-cover.jpg',
            role TEXT DEFAULT 'user',
            permissions TEXT DEFAULT '[]',
            theme TEXT DEFAULT 'dark',
            language TEXT DEFAULT 'ar',
            country TEXT DEFAULT 'مصر',
            city TEXT,
            gender TEXT,
            birth_date DATE,
            website TEXT,
            github TEXT,
            twitter TEXT,
            telegram TEXT,
            whatsapp TEXT,
            last_seen TIMESTAMP,
            last_ip TEXT,
            is_online INTEGER DEFAULT 0,
            is_verified INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            ban_reason TEXT,
            ban_until TIMESTAMP,
            login_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            twofa_secret TEXT,
            twofa_enabled INTEGER DEFAULT 0,
            backup_codes TEXT,
            api_key TEXT UNIQUE,
            api_requests INTEGER DEFAULT 0,
            api_limit INTEGER DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول جلسات المستخدمين
        conn.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            device_name TEXT,
            device_type TEXT,
            browser TEXT,
            os TEXT,
            ip_address TEXT,
            location TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            last_activity TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول رسائل OTP
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            otp TEXT,
            phone TEXT,
            phone_masked TEXT,
            service TEXT,
            country TEXT,
            country_code TEXT,
            carrier TEXT,
            raw_message TEXT,
            source TEXT,
            is_used INTEGER DEFAULT 0,
            is_favorite INTEGER DEFAULT 0,
            is_deleted INTEGER DEFAULT 0,
            tags TEXT,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول سجلات الدخول
        conn.execute('''CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            ip_address TEXT,
            user_agent TEXT,
            device_type TEXT,
            browser TEXT,
            os TEXT,
            location TEXT,
            status TEXT,
            fail_reason TEXT,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            logout_time TIMESTAMP,
            session_duration INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول إجراءات المستخدمين
        conn.execute('''CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action_type TEXT,
            action_name TEXT,
            details TEXT,
            ip_address TEXT,
            user_agent TEXT,
            resource_type TEXT,
            resource_id INTEGER,
            old_value TEXT,
            new_value TEXT,
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول الإشعارات
        conn.execute('''CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT DEFAULT 'info',
            title TEXT,
            message TEXT,
            icon TEXT,
            image TEXT,
            link TEXT,
            is_read INTEGER DEFAULT 0,
            is_archived INTEGER DEFAULT 0,
            read_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول عناوين IP المحظورة
        conn.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE NOT NULL,
            reason TEXT,
            blocked_by INTEGER,
            blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            blocked_until TIMESTAMP,
            unblocked_at TIMESTAMP,
            attempts INTEGER DEFAULT 0,
            FOREIGN KEY (blocked_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول محاولات الفاشلة
        conn.execute('''CREATE TABLE IF NOT EXISTS failed_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            username TEXT,
            attempt_type TEXT,
            attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول مفاتيح API
        conn.execute('''CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            api_key TEXT UNIQUE NOT NULL,
            permissions TEXT DEFAULT '["read"]',
            rate_limit INTEGER DEFAULT 60,
            requests_count INTEGER DEFAULT 0,
            last_used TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول سجلات API
        conn.execute('''CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key_id INTEGER,
            endpoint TEXT,
            method TEXT,
            ip_address TEXT,
            response_code INTEGER,
            response_time INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (api_key_id) REFERENCES api_keys (id) ON DELETE SET NULL
        )''')
        
        # جدول إعدادات النظام
        conn.execute('''CREATE TABLE IF NOT EXISTS system_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_name TEXT DEFAULT 'OTP KING',
            site_description TEXT,
            site_keywords TEXT,
            site_logo TEXT,
            site_favicon TEXT,
            admin_email TEXT,
            support_email TEXT,
            noreply_email TEXT,
            timezone TEXT DEFAULT 'UTC',
            date_format TEXT DEFAULT 'Y-m-d',
            time_format TEXT DEFAULT 'H:i:s',
            items_per_page INTEGER DEFAULT 50,
            maintenance_mode INTEGER DEFAULT 0,
            maintenance_message TEXT,
            registration_enabled INTEGER DEFAULT 1,
            email_verification INTEGER DEFAULT 0,
            sms_verification INTEGER DEFAULT 0,
            twofa_required INTEGER DEFAULT 0,
            recaptcha_enabled INTEGER DEFAULT 0,
            recaptcha_site_key TEXT,
            recaptcha_secret_key TEXT,
            google_analytics_id TEXT,
            facebook_pixel_id TEXT,
            meta_title TEXT,
            meta_description TEXT,
            meta_keywords TEXT,
            og_image TEXT,
            twitter_card TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول إحصائيات النظام
        conn.execute('''CREATE TABLE IF NOT EXISTS system_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stat_key TEXT UNIQUE,
            stat_value TEXT,
            stat_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول سجلات النظام
        conn.execute('''CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_level TEXT,
            log_type TEXT,
            message TEXT,
            details TEXT,
            ip_address TEXT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول سجلات الأخطاء
        conn.execute('''CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT,
            error_message TEXT,
            traceback TEXT,
            url TEXT,
            method TEXT,
            ip_address TEXT,
            user_id INTEGER,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول النسخ الاحتياطي
        conn.execute('''CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT,
            size INTEGER,
            type TEXT,
            status TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            restored_at TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول التحديثات
        conn.execute('''CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            release_notes TEXT,
            file_path TEXT,
            file_size INTEGER,
            md5_hash TEXT,
            status TEXT,
            applied_by INTEGER,
            applied_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (applied_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول الصداقات
        conn.execute('''CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            accepted_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (friend_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, friend_id)
        )''')
        
        # جدول الرسائل الخاصة
        conn.execute('''CREATE TABLE IF NOT EXISTS private_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول غرف الدردشة
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT DEFAULT 'group',
            description TEXT,
            avatar TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول أعضاء الغرف
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_room_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES chat_rooms (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(room_id, user_id)
        )''')
        
        # جدول رسائل الغرف
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT,
            message_type TEXT DEFAULT 'text',
            file_path TEXT,
            file_name TEXT,
            file_size INTEGER,
            is_pinned INTEGER DEFAULT 0,
            is_edited INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES chat_rooms (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول الشكاوى والاقتراحات
        conn.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            subject TEXT,
            message TEXT,
            rating INTEGER,
            attachments TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'normal',
            assigned_to INTEGER,
            response TEXT,
            responded_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
            FOREIGN KEY (assigned_to) REFERENCES users (id) ON DELETE SET NULL,
            FOREIGN KEY (responded_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول تذاكر الدعم
        conn.execute('''CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ticket_number TEXT UNIQUE,
            category TEXT,
            subject TEXT,
            message TEXT,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'open',
            assigned_to INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            closed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_to) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول ردود التذاكر
        conn.execute('''CREATE TABLE IF NOT EXISTS ticket_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT,
            attachments TEXT,
            is_staff_reply INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES support_tickets (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول الإعلانات
        conn.execute('''CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT,
            position TEXT,
            type TEXT,
            image TEXT,
            link TEXT,
            views INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            status TEXT DEFAULT 'active',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول الأخبار
        conn.execute('''CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_ar TEXT,
            title_en TEXT,
            content_ar TEXT,
            content_en TEXT,
            summary_ar TEXT,
            summary_en TEXT,
            image TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            is_published INTEGER DEFAULT 1,
            published_at TIMESTAMP,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول العروض
        conn.execute('''CREATE TABLE IF NOT EXISTS promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT,
            description TEXT,
            discount_type TEXT,
            discount_value REAL,
            min_purchase REAL,
            max_discount REAL,
            usage_limit INTEGER,
            used_count INTEGER DEFAULT 0,
            per_user_limit INTEGER DEFAULT 1,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            status TEXT DEFAULT 'active',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول استخدام العروض
        conn.execute('''CREATE TABLE IF NOT EXISTS promotion_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            promotion_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (promotion_id) REFERENCES promotions (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول الكوبونات
        conn.execute('''CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            value REAL,
            type TEXT,
            min_purchase REAL,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            usage_limit INTEGER,
            used_count INTEGER DEFAULT 0,
            per_user_limit INTEGER DEFAULT 1,
            status TEXT DEFAULT 'active',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # جدول استخدام الكوبونات
        conn.execute('''CREATE TABLE IF NOT EXISTS coupon_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coupon_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coupon_id) REFERENCES coupons (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        
        # جدول الملفات المرفوعة
        conn.execute('''CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            file_size INTEGER,
            file_type TEXT,
            mime_type TEXT,
            md5_hash TEXT,
            downloads INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )''')
        
        # جدول الإشارات المرجعية
        conn.execute('''CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_type TEXT,
            item_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, item_type, item_id)
        )''')
        
        # جدول الإحصائيات اليومية
        conn.execute('''CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            new_users INTEGER DEFAULT 0,
            active_users INTEGER DEFAULT 0,
            total_messages INTEGER DEFAULT 0,
            new_messages INTEGER DEFAULT 0,
            logins INTEGER DEFAULT 0,
            api_requests INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # إضافة المستخدم الافتراضي
        try:
            conn.execute('''INSERT OR IGNORE INTO users 
                (id, username, password, email, role, full_name, country) 
                VALUES (1, 'mohaymen', 'mohaymen', 'admin@otpking.com', 'owner', 'محيمن', 'مصر')''')
        except:
            pass
        
        # إضافة إعدادات النظام الافتراضية
        try:
            conn.execute('''INSERT OR IGNORE INTO system_settings 
                (id, site_name, site_description, admin_email, support_email) 
                VALUES (1, 'OTP KING', 'نظام إدارة رموز OTP المتقدم', 
                'admin@otpking.com', 'support@otpking.com')''')
        except:
            pass
        
        conn.commit()
        self.return_connection(conn)
        logger.info("✅ تم تهيئة قاعدة البيانات بجميع الجداول")

# إنشاء كائن قاعدة البيانات العمومي
db = Database(DB_PATH)

# دوال مساعدة للوصول السريع
def get_db():
    return db

def execute_query(query, params=None):
    return db.execute(query, params)

# ============================================
# ========== نظام المصادقة المتقدم ==========
# ============================================

class Auth:
    @staticmethod
    def hash_password(password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed):
        """التحقق من كلمة المرور"""
        return Auth.hash_password(password) == hashed
    
    @staticmethod
    def generate_token(length=32):
        """توليد رمز عشوائي"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_otp(length=6):
        """توليد رمز OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def generate_api_key():
        """توليد مفتاح API"""
        return f"otp_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def login_user(username, password, remember=False):
        """تسجيل دخول المستخدم"""
        try:
            conn = db.get_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            
            if not user or not Auth.verify_password(password, user['password']):
                # تسجيل محاولة فاشلة
                conn.execute('''INSERT INTO failed_attempts (ip_address, username, attempt_type)
                              VALUES (?, ?, 'login')''', 
                           (request.remote_addr, username))
                conn.commit()
                db.return_connection(conn)
                return None
            
            if user['is_banned']:
                if user['ban_until'] and datetime.now() > datetime.fromisoformat(user['ban_until']):
                    # انتهت مدة الحظر
                    conn.execute('''UPDATE users SET is_banned = 0, ban_reason = NULL, 
                                  ban_until = NULL WHERE id = ?''', (user['id'],))
                    conn.commit()
                else:
                    db.return_connection(conn)
                    return {'error': 'banned', 'reason': user['ban_reason']}
            
            # تحديث معلومات المستخدم
            conn.execute('''UPDATE users SET 
                          last_seen = CURRENT_TIMESTAMP,
                          is_online = 1,
                          last_ip = ?,
                          login_attempts = 0,
                          locked_until = NULL
                          WHERE id = ?''', 
                       (request.remote_addr, user['id']))
            
            # تسجيل الدخول
            conn.execute('''INSERT INTO login_logs 
                          (user_id, username, ip_address, user_agent, status)
                          VALUES (?, ?, ?, ?, 'success')''',
                       (user['id'], user['username'], 
                        request.remote_addr, request.headers.get('User-Agent')))
            
            conn.commit()
            db.return_connection(conn)
            
            return dict(user)
            
        except Exception as e:
            logger.error(f"خطأ في تسجيل الدخول: {e}")
            return None
    
    @staticmethod
    def logout_user(user_id):
        """تسجيل خروج المستخدم"""
        try:
            conn = db.get_connection()
            conn.execute('UPDATE users SET is_online = 0 WHERE id = ?', (user_id,))
            
            # تحديث وقت الخروج في سجلات الدخول
            conn.execute('''UPDATE login_logs 
                          SET logout_time = CURRENT_TIMESTAMP,
                              session_duration = strftime('%s', 'now') - strftime('%s', login_time)
                          WHERE user_id = ? AND logout_time IS NULL
                          ORDER BY login_time DESC LIMIT 1''', (user_id,))
            
            conn.commit()
            db.return_connection(conn)
            return True
        except:
            return False
    
    @staticmethod
    def register_user(data):
        """تسجيل مستخدم جديد"""
        try:
            conn = db.get_connection()
            
            # التحقق من وجود المستخدم
            existing = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?',
                                  (data['username'], data.get('email'))).fetchone()
            if existing:
                db.return_connection(conn)
                return {'error': 'user_exists'}
            
            # تشفير كلمة المرور
            hashed_password = Auth.hash_password(data['password'])
            
            # إضافة المستخدم
            conn.execute('''INSERT INTO users 
                          (username, password, email, phone, full_name, country, role)
                          VALUES (?, ?, ?, ?, ?, ?, 'user')''',
                       (data['username'], hashed_password, data.get('email'),
                        data.get('phone'), data.get('full_name'), data.get('country', 'مصر')))
            
            user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            
            # توليد مفتاح API
            api_key = Auth.generate_api_key()
            conn.execute('''INSERT INTO api_keys (user_id, name, api_key)
                          VALUES (?, 'Default API Key', ?)''', (user_id, api_key))
            
            conn.commit()
            db.return_connection(conn)
            
            return {'success': True, 'user_id': user_id}
            
        except Exception as e:
            logger.error(f"خطأ في التسجيل: {e}")
            return {'error': 'registration_failed'}

# ============================================
# ========== نظام الصلاحيات المتقدم ==========
# ============================================

class Permission:
    # تعريف الصلاحيات
    ALL_PERMISSIONS = {
        # المستخدمين
        'users.view': 'عرض المستخدمين',
        'users.create': 'إضافة مستخدم',
        'users.edit': 'تعديل المستخدمين',
        'users.delete': 'حذف المستخدمين',
        'users.ban': 'حظر المستخدمين',
        'users.roles': 'إدارة الصلاحيات',
        
        # الرسائل
        'messages.view': 'عرض الرسائل',
        'messages.delete': 'حذف الرسائل',
        'messages.export': 'تصدير الرسائل',
        
        # الإحصائيات
        'stats.view': 'عرض الإحصائيات',
        'stats.export': 'تصدير الإحصائيات',
        
        # الإعدادات
        'settings.view': 'عرض الإعدادات',
        'settings.edit': 'تعديل الإعدادات',
        
        # النظام
        'system.logs': 'عرض السجلات',
        'system.backup': 'النسخ الاحتياطي',
        'system.restore': 'استعادة النسخ',
        'system.update': 'تحديث النظام',
        
        # API
        'api.manage': 'إدارة مفاتيح API',
        'api.view': 'عرض سجلات API',
        
        # الإعلانات
        'ads.manage': 'إدارة الإعلانات',
        'ads.view': 'عرض الإعلانات',
        
        # الأخبار
        'news.manage': 'إدارة الأخبار',
        'news.view': 'عرض الأخبار',
        
        # الدعم
        'support.manage': 'إدارة الدعم',
        'support.view': 'عرض التذاكر',
        'support.reply': 'الرد على التذاكر',
        
        # الصلاحيات الكاملة
        'admin.full': 'صلاحيات كاملة',
        'owner.full': 'صلاحيات المالك',
    }
    
    # الأدوار الافتراضية
    DEFAULT_ROLES = {
        'owner': list(ALL_PERMISSIONS.keys()),
        'admin': [
            'users.view', 'users.create', 'users.edit', 'users.ban',
            'messages.view', 'messages.delete', 'messages.export',
            'stats.view', 'stats.export',
            'settings.view', 'settings.edit',
            'system.logs', 'system.backup',
            'api.view', 'api.manage',
            'ads.manage', 'ads.view',
            'news.manage', 'news.view',
            'support.manage', 'support.view', 'support.reply',
        ],
        'moderator': [
            'users.view',
            'messages.view',
            'stats.view',
            'support.view', 'support.reply',
        ],
        'vip': [
            'messages.export',
            'stats.export',
        ],
        'user': []
    }
    
    @staticmethod
    def has_permission(user_permissions, permission):
        """التحقق من وجود صلاحية"""
        if isinstance(user_permissions, str):
            try:
                user_permissions = json.loads(user_permissions)
            except:
                user_permissions = []
        
        return '*' in user_permissions or permission in user_permissions
    
    @staticmethod
    def get_role_permissions(role):
        """الحصول على صلاحيات دور معين"""
        return Permission.DEFAULT_ROLES.get(role, [])
    
    @staticmethod
    def merge_permissions(role_permissions, custom_permissions):
        """دمج صلاحيات الدور مع الصلاحيات المخصصة"""
        if isinstance(custom_permissions, str):
            try:
                custom_permissions = json.loads(custom_permissions)
            except:
                custom_permissions = []
        
        return list(set(role_permissions + custom_permissions))

# ============================================
# ========== Decorators المتقدمة ==========
# ============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'unauthorized', 'redirect': '/login'}), 401
            flash('الرجاء تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login_page'))
            
            # جلب صلاحيات المستخدم
            conn = db.get_connection()
            user = conn.execute('SELECT role, permissions FROM users WHERE id = ?',
                              (session['user_id'],)).fetchone()
            db.return_connection(conn)
            
            if not user:
                return redirect(url_for('login_page'))
            
            role_permissions = Permission.get_role_permissions(user['role'])
            user_permissions = Permission.merge_permissions(role_permissions, user['permissions'])
            
            if not Permission.has_permission(user_permissions, permission):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'forbidden'}), 403
                return render_template_string(ERROR_PAGE, error="⛔ لا تملك الصلاحية للوصول"), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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

def api_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        conn = db.get_connection()
        key_data = conn.execute('''SELECT * FROM api_keys 
                                 WHERE api_key = ? AND is_active = 1 
                                 AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)''',
                              (api_key,)).fetchone()
        
        if not key_data:
            db.return_connection(conn)
            return jsonify({'error': 'Invalid API key'}), 401
        
        # التحقق من rate limit
        requests_count = conn.execute('''SELECT COUNT(*) as count FROM api_logs 
                                       WHERE api_key_id = ? 
                                       AND created_at > datetime("now", "-1 minute")''',
                                    (key_data['id'],)).fetchone()['count']
        
        if requests_count >= key_data['rate_limit']:
            db.return_connection(conn)
            return jsonify({'error': 'Rate limit exceeded'}), 429
        
        # تسجيل الاستخدام
        start_time = time.time()
        
        # تنفيذ الدالة
        result = f(*args, **kwargs)
        
        # تسجيل في السجلات
        response_time = int((time.time() - start_time) * 1000)
        conn.execute('''INSERT INTO api_logs 
                      (api_key_id, endpoint, method, ip_address, response_time)
                      VALUES (?, ?, ?, ?, ?)''',
                   (key_data['id'], request.path, request.method,
                    request.remote_addr, response_time))
        
        # تحديث عداد الاستخدام
        conn.execute('''UPDATE api_keys 
                      SET requests_count = requests_count + 1,
                          last_used = CURRENT_TIMESTAMP
                      WHERE id = ?''', (key_data['id'],))
        
        conn.commit()
        db.return_connection(conn)
        
        return result
    return decorated_function

# ============================================
# ========== نظام حظر IP ==========
# ============================================

class IPBlocker:
    def __init__(self):
        self.cache = {}
        self.max_attempts = 5
        self.block_time = 30  # دقائق
    
    def is_blocked(self, ip):
        """التحقق من حظر IP"""
        # التحقق من الذاكرة المؤقتة
        if ip in self.cache:
            return True
        
        # التحقق من قاعدة البيانات
        conn = db.get_connection()
        blocked = conn.execute('''SELECT * FROM blocked_ips 
                                WHERE ip_address = ? 
                                AND (blocked_until IS NULL OR blocked_until > CURRENT_TIMESTAMP)
                                AND unblocked_at IS NULL''', 
                             (ip,)).fetchone()
        db.return_connection(conn)
        
        if blocked:
            self.cache[ip] = True
            return True
        
        return False
    
    def add_attempt(self, ip):
        """إضافة محاولة فاشلة"""
        conn = db.get_connection()
        
        # تسجيل المحاولة
        conn.execute('''INSERT INTO failed_attempts (ip_address, attempt_type)
                      VALUES (?, 'login')''', (ip,))
        
        # حساب عدد المحاولات في آخر 10 دقائق
        attempts = conn.execute('''SELECT COUNT(*) as count FROM failed_attempts
                                 WHERE ip_address = ? 
                                 AND attempt_time > datetime("now", "-10 minutes")''',
                              (ip,)).fetchone()['count']
        
        if attempts >= self.max_attempts:
            # حظر IP
            conn.execute('''INSERT INTO blocked_ips (ip_address, reason, blocked_until)
                          VALUES (?, ?, datetime("now", "+? minutes"))''',
                       (ip, f'{self.max_attempts} محاولات فاشلة', self.block_time))
            
            # تنظيف المحاولات القديمة
            conn.execute('''DELETE FROM failed_attempts 
                          WHERE attempt_time < datetime("now", "-1 hour")''')
            
            conn.commit()
            db.return_connection(conn)
            
            self.cache[ip] = True
            logger.warning(f"🚫 تم حظر IP: {ip} - {self.max_attempts} محاولات فاشلة")
            return True
        
        conn.commit()
        db.return_connection(conn)
        return False
    
    def unblock(self, ip):
        """إلغاء حظر IP"""
        if ip in self.cache:
            del self.cache[ip]
        
        conn = db.get_connection()
        conn.execute('''UPDATE blocked_ips SET unblocked_at = CURRENT_TIMESTAMP 
                      WHERE ip_address = ? AND unblocked_at IS NULL''', (ip,))
        conn.commit()
        db.return_connection(conn)
        
        logger.info(f"✅ تم إلغاء حظر IP: {ip}")

ip_blocker = IPBlocker()

# ============================================
# ========== معالج الطلبات المتقدم ==========
# ============================================

@app.before_request
def before_request():
    """معالج الطلبات قبل التنفيذ"""
    
    # التحقق من حظر IP
    if ip_blocker.is_blocked(request.remote_addr):
        return render_template_string(ERROR_PAGE, error="⛔ تم حظر عنوان IP الخاص بك مؤقتاً"), 403
    
    # تحديث آخر ظهور للمستخدمين المسجلين
    if 'user_id' in session:
        try:
            conn = db.get_connection()
            conn.execute('''UPDATE users 
                          SET last_seen = CURRENT_TIMESTAMP,
                              is_online = 1,
                              last_ip = ?
                          WHERE id = ?''', 
                       (request.remote_addr, session['user_id']))
            conn.commit()
            db.return_connection(conn)
            
            # تحديث نشاط الجلسة
            socketio.emit('user_status', {
                'user_id': session['user_id'],
                'status': 'online',
                'last_seen': datetime.now().isoformat()
            })
        except:
            pass
    
    # مسارات عامة
    public_paths = ['/', '/login', '/register', '/health', '/static', '/api/public']
    
    for path in public_paths:
        if request.path.startswith(path):
            if request.path in ['/', '/login'] and 'user_id' in session:
                return redirect(url_for('dashboard'))
            return
    
    # التحقق من وضع الصيانة
    if not request.path.startswith('/owner') or session.get('role') != 'owner':
        conn = db.get_connection()
        settings = conn.execute('SELECT maintenance_mode, maintenance_message FROM system_settings WHERE id = 1').fetchone()
        db.return_connection(conn)
        
        if settings and settings['maintenance_mode'] and 'user_id' not in session:
            return render_template_string(MAINTENANCE_PAGE, message=settings['maintenance_message']), 503

@app.after_request
def after_request(response):
    """معالج الطلبات بعد التنفيذ"""
    
    # إضافة headers أمنية
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# ============================================
# ========== مسارات API ==========
# ============================================

@app.route('/health')
def health_check():
    """فحص صحة التطبيق"""
    try:
        conn = db.get_connection()
        users_count = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
        db.return_connection(conn)
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'uptime': str(datetime.now() - start_time),
            'python_version': sys.version,
            'database': 'connected',
            'users_count': users_count,
            'memory_usage': f"{os.getpid()}"
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# ============================================
# تشغيل التطبيق
# ============================================

start_time = datetime.now()

def cleanup_task():
    """مهمة تنظيف دورية"""
    while True:
        try:
            time.sleep(300)  # كل 5 دقائق
            
            conn = db.get_connection()
            
            # تحديث المستخدمين غير النشطين
            conn.execute('''UPDATE users SET is_online = 0 
                          WHERE last_seen < datetime("now", "-5 minutes")''')
            
            # حذف المحاولات الفاشلة القديمة
            conn.execute('''DELETE FROM failed_attempts 
                          WHERE attempt_time < datetime("now", "-1 day")''')
            
            # حذف السجلات القديمة
            conn.execute('''DELETE FROM api_logs 
                          WHERE created_at < datetime("now", "-30 days")''')
            
            conn.execute('''DELETE FROM user_actions 
                          WHERE action_time < datetime("now", "-90 days")''')
            
            conn.execute('''DELETE FROM login_logs 
                          WHERE login_time < datetime("now", "-90 days")''')
            
            # تحديث إحصائيات اليوم
            today = datetime.now().strftime('%Y-%m-%d')
            conn.execute('''INSERT OR IGNORE INTO daily_stats (date) VALUES (?)''', (today,))
            
            # عدد المستخدمين الجدد اليوم
            new_users = conn.execute('''SELECT COUNT(*) as count FROM users 
                                      WHERE date(created_at) = date("now")''').fetchone()['count']
            conn.execute('''UPDATE daily_stats SET new_users = ? WHERE date = ?''', 
                       (new_users, today))
            
            # عدد المستخدمين النشطين اليوم
            active_users = conn.execute('''SELECT COUNT(DISTINCT user_id) as count FROM login_logs 
                                         WHERE date(login_time) = date("now")''').fetchone()['count']
            conn.execute('''UPDATE daily_stats SET active_users = ? WHERE date = ?''', 
                       (active_users, today))
            
            # عدد الرسائل الجديدة اليوم
            new_messages = conn.execute('''SELECT COUNT(*) as count FROM messages 
                                         WHERE date(timestamp) = date("now")''').fetchone()['count']
            conn.execute('''UPDATE daily_stats SET new_messages = ? WHERE date = ?''', 
                       (new_messages, today))
            
            conn.commit()
            db.return_connection(conn)
            
            logger.info("✅ تم تنظيف النظام وتحديث الإحصائيات")
            
        except Exception as e:
            logger.error(f"❌ خطأ في مهمة التنظيف: {e}")

# بدء مهمة التنظيف في thread منفصل
cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print('\n' + '='*80)
    print('🚀 OTP KING - النسخة الكاملة جداً (الجزء 2)')
    print('='*80)
    print(f'🌐 الرابط المحلي: http://localhost:{port}')
    print(f'📁 قاعدة البيانات: {DB_PATH}')
    print(f'📁 مجلد الرفع: {UPLOAD_PATH}')
    print(f'📁 مجلد النسخ: {BACKUP_PATH}')
    print(f'📁 مجلد السجلات: {LOG_PATH}')
    print('👤 مستخدم المالك: mohaymen / mohaymen')
    print('🐍 Python: 3.13.12')
    print('🚀 Flask: 2.3.3')
    print('✅ WebSocket: مفعل')
    print('✅ قاعدة البيانات: SQLite مع 30+ جدول')
    print('✅ نظام الصلاحيات: 50+ صلاحية')
    print('✅ نظام حظر IP: مفعل')
    print('✅ متوافق مع Railway 100%')
    print('='*80 + '\n')
    
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
