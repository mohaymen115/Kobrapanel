#!/usrbin/env python3
# -*- coding: utf-8 -*-

"""
OTP Monitor Script - Console Version
يجلب ويعرض رموز OTP مباشرة في الطرفية
"""

import os
import requests
import re
import json
import time
import sys
from datetime import datetime
from dotenv import load_dotenv

# ============================================
# التحميل من .env والتكوين
# ============================================
load_dotenv()

# إعدادات الاتصال - غيرها حسب بياناتك
PANEL_URL = os.getenv('PANEL_URL', "http://198.135.52.238")
PANEL_USERNAME = os.getenv('PANEL_USERNAME', "gagaywb66")
PANEL_PASSWORD = os.getenv('PANEL_PASSWORD', "gagaywb66")
REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', 10))  # ثواني

# ============================================
# أعلام الدول (للزينة)
# ============================================
COUNTRY_FLAGS = {
    'venezuela': '🇻🇪', 've': '🇻🇪', 'brazil': '🇧🇷', 'br': '🇧🇷',
    'argentina': '🇦🇷', 'ar': '🇦🇷', 'colombia': '🇨🇴', 'co': '🇨🇴',
    'usa': '🇺🇸', 'us': '🇺🇸', 'canada': '🇨🇦', 'ca': '🇨🇦',
    'uk': '🇬🇧', 'gb': '🇬🇧', 'germany': '🇩🇪', 'de': '🇩🇪',
    'france': '🇫🇷', 'fr': '🇫🇷', 'egypt': '🇪🇬', 'eg': '🇪🇬',
    'saudi': '🇸🇦', 'sa': '🇸🇦', 'uae': '🇦🇪', 'ae': '🇦🇪',
    'morocco': '🇲🇦', 'ma': '🇲🇦', 'algeria': '🇩🇿', 'dz': '🇩🇿',
    'tunisia': '🇹🇳', 'tn': '🇹🇳', 'libya': '🇱🇾', 'ly': '🇱🇾',
    'jordan': '🇯🇴', 'jo': '🇯🇴', 'lebanon': '🇱🇧', 'lb': '🇱🇧',
    'palestine': '🇵🇸', 'ps': '🇵🇸', 'iraq': '🇮🇶', 'iq': '🇮🇶',
    'syria': '🇸🇾', 'sy': '🇸🇾', 'yemen': '🇾🇪', 'ye': '🇾🇪',
    'kuwait': '🇰🇼', 'kw': '🇰🇼', 'qatar': '🇶🇦', 'qa': '🇶🇦',
    'bahrain': '🇧🇭', 'bh': '🇧🇭', 'oman': '🇴🇲', 'om': '🇴🇲',
}

# ============================================
# ألوان للطرفية (تعمل على Linux/Mac و Windows 10+)
# ============================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    WHITE = '\033[97m'
    
    # خلفيات
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# ============================================
# فلتر لمنع تكرار نفس الرسالة
# ============================================
class OTPFilter:
    def __init__(self):
        self.seen_ids = set()
        self.max_size = 500  # حد أقصى للتخزين
    
    def is_new(self, msg_id):
        if msg_id in self.seen_ids:
            return False
        self.seen_ids.add(msg_id)
        # لو كبرت المجموعة ننظفها
        if len(self.seen_ids) > self.max_size:
            self.seen_ids = set(list(self.seen_ids)[-self.max_size//2:])
        return True
    
    def clear(self):
        self.seen_ids.clear()

otp_filter = OTPFilter()

# ============================================
# إخفاء جزء من الرقم
# ============================================
def mask_phone(phone):
    if not phone or phone == 'Unknown':
        return 'Unknown'
    phone = str(phone).strip()
    if len(phone) <= 6:
        return phone[:2] + '•••' + phone[-1:]
    if phone.startswith('+'):
        return f"{phone[:5]}•••{phone[-4:]}"
    return f"{phone[:4]}•••{phone[-4:]}"

# ============================================
# استخراج OTP من النص
# ============================================
def extract_otp(text):
    if not text:
        return 'N/A'
    
    patterns = [
        r'(\d{3}[-\s]?\d{3})',
        r'(\d{4}[-\s]?\d{4})',
        r'(?:code|kode|otp|رمز|كود)[:\s]*(\d{4,8})',
        r'(\d{6})',
        r'(\d{4,8})',
        r'(\d{3} \d{3})',
        r'(\d{4} \d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).replace(' ', '-')
    return 'N/A'

# ============================================
# كشف الخدمة من النص
# ============================================
def detect_service(text):
    if not text:
        return 'Unknown'
    
    services = {
        'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
        'facebook': 'Facebook', 'instagram': 'Instagram',
        'twitter': 'Twitter', 'google': 'Google',
        'tiktok': 'TikTok', 'snapchat': 'Snapchat',
        'paypal': 'PayPal', 'amazon': 'Amazon',
        'netflix': 'Netflix', 'spotify': 'Spotify',
        'tinder': 'Tinder', 'uber': 'Uber',
        'careem': 'Careem', 'talabat': 'Talabat',
    }
    
    text_lower = text.lower()
    for key, name in services.items():
        if key in text_lower:
            return name
    return 'SMS Service'

# ============================================
# الحصول على علم الدولة
# ============================================
def get_country_flag(country):
    if not country:
        return '🌍'
    country_lower = country.lower().strip()
    if country_lower in COUNTRY_FLAGS:
        return COUNTRY_FLAGS[country_lower]
    for key, flag in COUNTRY_FLAGS.items():
        if key in country_lower:
            return flag
    return '🌍'

# ============================================
# فورمات الرسالة
# ============================================
def format_message(msg):
    try:
        # محتوى الرسالة
        content = msg.get('content') or msg.get('message') or msg.get('text') or ''
        
        # استخراج OTP
        otp = extract_otp(content)
        
        # الرقم
        phone = msg.get('Number') or msg.get('number') or msg.get('phone') or 'Unknown'
        
        # الدولة
        country = msg.get('country') or msg.get('Country') or ''
        flag = get_country_flag(country)
        
        # الخدمة
        service = msg.get('service') or msg.get('Service') or msg.get('sender') or detect_service(content)
        
        # الوقت
        timestamp = msg.get('created_at') or msg.get('timestamp') or ''
        if timestamp:
            try:
                # محاولة تحويل الصيغ المختلفة
                if 'T' in str(timestamp):
                    dt = datetime.strptime(str(timestamp)[:19], '%Y-%m-%dT%H:%M:%S')
                else:
                    dt = datetime.strptime(str(timestamp)[:19], '%Y-%m-%d %H:%M:%S')
                timestamp = dt.strftime('%H:%M:%S')
            except:
                timestamp = datetime.now().strftime('%H:%M:%S')
        else:
            timestamp = datetime.now().strftime('%H:%M:%S')
        
        # ID فريد
        msg_id = msg.get('id') or msg.get('_id') or str(hash(content + phone + timestamp))
        
        return {
            'otp': otp,
            'phone': phone,
            'phone_masked': mask_phone(phone),
            'service': service,
            'country': country,
            'flag': flag,
            'timestamp': timestamp,
            'content': content[:150] + ('...' if len(content) > 150 else ''),
            'id': msg_id
        }
    except Exception as e:
        return None

# ============================================
# فئة الاتصال بالبانل
# ============================================
class PanelAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.logged_in = False
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        })
    
    def login(self):
        """تسجيل الدخول للبانل"""
        try:
            print(f"{Colors.YELLOW}🔐 جاري تسجيل الدخول إلى {self.base_url}...{Colors.RESET}")
            
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
                    print(f"{Colors.GREEN}✅ تم تسجيل الدخول بنجاح{Colors.RESET}")
                    return True
                elif 'access_token' in data:
                    self.token = data['access_token']
                    self.logged_in = True
                    self.session.headers['Authorization'] = f'Bearer {self.token}'
                    print(f"{Colors.GREEN}✅ تم تسجيل الدخول بنجاح{Colors.RESET}")
                    return True
                else:
                    print(f"{Colors.RED}❌ لا يوجد token في الرد: {data}{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ فشل تسجيل الدخول: {response.status_code}{Colors.RESET}")
                print(f"{Colors.RED}الرد: {response.text[:200]}{Colors.RESET}")
            
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}❌ خطأ في الاتصال: لا يمكن الوصول إلى {self.base_url}{Colors.RESET}")
            return False
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}❌ خطأ: انتهت مهلة الاتصال{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ خطأ في تسجيل الدخول: {str(e)}{Colors.RESET}")
            return False
    
    def fetch_messages(self):
        """جلب الرسائل من البانل"""
        if not self.logged_in:
            print(f"{Colors.YELLOW}⚠️ غير مسجل الدخول، جاري تسجيل الدخول...{Colors.RESET}")
            if not self.login():
                return []
        
        try:
            # تجربة مسارات مختلفة للـ API
            endpoints = [
                f"{self.base_url}/api/sms",
                f"{self.base_url}/api/messages",
                f"{self.base_url}/api/otp",
                f"{self.base_url}/api/inbox",
            ]
            
            for endpoint in endpoints:
                try:
                    response = self.session.get(
                        f"{endpoint}?limit=50",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        break
                except:
                    continue
            else:
                # إذا لم ينجح أي من المسارات، نجرب المسار الأصلي مرة أخرى
                response = self.session.get(
                    f"{self.base_url}/api/sms?limit=50",
                    timeout=10
                )
            
            if response.status_code == 401:
                print(f"{Colors.YELLOW}⚠️ التوكن منتهي، إعادة تسجيل الدخول...{Colors.RESET}")
                self.logged_in = False
                if not self.login():
                    return []
                response = self.session.get(
                    f"{self.base_url}/api/sms?limit=50",
                    timeout=10
                )
            
            if response.status_code != 200:
                print(f"{Colors.RED}❌ فشل جلب الرسائل: {response.status_code}{Colors.RESET}")
                return []
            
            try:
                data = response.json()
            except:
                print(f"{Colors.RED}❌ الرد ليس JSON صالح{Colors.RESET}")
                return []
            
            # استخراج الرسائل حسب نوع الرد
            messages = []
            if isinstance(data, list):
                messages = data
            elif isinstance(data, dict):
                # محاولة استخراج الرسائل من مفاتيح مختلفة
                messages = (data.get('sms') or data.get('messages') or 
                           data.get('data') or data.get('items') or [])
            else:
                messages = []
            
            # تنسيق الرسائل
            formatted = []
            for msg in messages:
                f = format_message(msg)
                if f and f['otp'] != 'N/A':  # فقط الرسائل التي تحتوي على OTP
                    formatted.append(f)
            
            return formatted
            
        except Exception as e:
            print(f"{Colors.RED}❌ خطأ في جلب الرسائل: {str(e)}{Colors.RESET}")
            return []

# ============================================
# طباعة رأس البرنامج
# ============================================
def print_header():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}║                📱 OTP MONITOR - CONSOLE                  ║{Colors.RESET}")
    print(f"{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}║                  النسخة المباشرة v1.0                     ║{Colors.RESET}")
    print(f"{Colors.BG_BLUE}{Colors.BOLD}{Colors.WHITE}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.CYAN}⏱️  آخر تحديث: {datetime.now().strftime('%H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.YELLOW}🔄 التحديث كل {REFRESH_INTERVAL} ثانية | اضغط Ctrl+C للخروج{Colors.RESET}")
    print(f"{Colors.MAGENTA}════════════════════════════════════════════════════════════{Colors.RESET}")

# ============================================
# طباعة رسالة OTP بشكل جميل
# ============================================
def print_otp_message(msg, index):
    print(f"\n{Colors.WHITE}{Colors.BG_MAGENTA} 🔔 رسالة جديدة رقم {index} في {msg['timestamp']} {Colors.RESET}")
    print(f"{Colors.CYAN}┌─────────────────────────────────────────────────────────────{Colors.RESET}")
    print(f"{Colors.YELLOW}│ {msg['flag']} الدولة   : {msg['country'] or 'غير معروفة'}{Colors.RESET}")
    print(f"{Colors.GREEN}│ 📞 الرقم    : {msg['phone_masked']}{Colors.RESET}")
    print(f"{Colors.BLUE}│ 🔧 الخدمة   : {msg['service']}{Colors.RESET}")
    print(f"{Colors.MAGENTA}│ 🔑 OTP      : {Colors.BOLD}{Colors.GREEN}{msg['otp']}{Colors.RESET}")
    print(f"{Colors.WHITE}│ 📝 النص     : {msg['content'][:100]}{Colors.RESET}")
    print(f"{Colors.CYAN}└─────────────────────────────────────────────────────────────{Colors.RESET}")

# ============================================
# حفظ في ملف
# ============================================
def save_to_file(msg):
    try:
        filename = f"otp_log_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"[{msg['timestamp']}] {msg['flag']} {msg['service']} - {msg['otp']} - {msg['phone']}\n")
            f.write(f"   {msg['content']}\n")
            f.write("-" * 50 + "\n")
    except:
        pass

# ============================================
# الدالة الرئيسية
# ============================================
def main():
    # إنشاء الاتصال
    api = PanelAPI(PANEL_URL, PANEL_USERNAME, PANEL_PASSWORD)
    
    print_header()
    print(f"{Colors.YELLOW}🔌 جاري الاتصال بالبانل...{Colors.RESET}")
    
    if not api.login():
        print(f"{Colors.RED}❌ فشل الاتصال بالبانل. تحقق من:{Colors.RESET}")
        print(f"{Colors.RED}   1. الرابط: {PANEL_URL}{Colors.RESET}")
        print(f"{Colors.RED}   2. اسم المستخدم: {PANEL_USERNAME}{Colors.RESET}")
        print(f"{Colors.RED}   3. كلمة المرور: {'*' * len(PANEL_PASSWORD)}{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 يمكنك تعديل البيانات في أول الملف أو في ملف .env{Colors.RESET}")
        sys.exit(1)
    
    # تخزين الرسائل
    all_messages = []
    total_otps = 0
    
    # محاولة جلب أولي
    try:
        print(f"{Colors.YELLOW}🔍 جاري جلب الرسائل...{Colors.RESET}")
        messages = api.fetch_messages()
        
        for msg in messages:
            if otp_filter.is_new(msg['id']):
                all_messages.insert(0, msg)
                total_otps += 1
                save_to_file(msg)
        
        if all_messages:
            print(f"{Colors.GREEN}✅ تم جلب {len(all_messages)} رسالة{Colors.RESET}")
            for i, msg in enumerate(all_messages[:5], 1):
                print_otp_message(msg, i)
        else:
            print(f"{Colors.YELLOW}⚠️ لا توجد رسائل OTP حالياً{Colors.RESET}")
    
    except Exception as e:
        print(f"{Colors.RED}❌ خطأ: {str(e)}{Colors.RESET}")
    
    # الحلقة الرئيسية
    try:
        cycle_count = 0
        while True:
            time.sleep(REFRESH_INTERVAL)
            cycle_count += 1
            
            print_header()
            print(f"{Colors.YELLOW}🔍 جاري التحقق من الرسائل الجديدة... (الدورة {cycle_count}){Colors.RESET}")
            
            messages = api.fetch_messages()
            new_count = 0
            
            for msg in messages:
                if otp_filter.is_new(msg['id']):
                    all_messages.insert(0, msg)
                    total_otps += 1
                    new_count += 1
                    save_to_file(msg)
            
            if new_count > 0:
                print(f"{Colors.GREEN}✅ تم استلام {new_count} رسالة جديدة{Colors.RESET}")
                # عرض الرسائل الجديدة
                for i in range(min(new_count, 5)):
                    print_otp_message(all_messages[i], i+1)
            else:
                print(f"{Colors.YELLOW}⏳ لا توجد رسائل جديدة{Colors.RESET}")
            
            # إحصائيات
            print(f"\n{Colors.CYAN}📊 الإحصائيات:{Colors.RESET}")
            print(f"   إجمالي OTP: {Colors.GREEN}{total_otps}{Colors.RESET}")
            print(f"   عدد الرسائل المخزنة: {len(all_messages)}")
            
            # عرض آخر 5 رسائل
            if all_messages:
                print(f"\n{Colors.MAGENTA}📋 آخر 5 رسائل:{Colors.RESET}")
                for i, msg in enumerate(all_messages[:5], 1):
                    print(f"   {i}. [{msg['timestamp']}] {msg['flag']} {msg['service']}: {Colors.GREEN}{msg['otp']}{Colors.RESET}")
            
            # معلومات إضافية
            uptime = datetime.now() - bot_start_time
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            print(f"\n{Colors.BLUE}⏰ وقت التشغيل: {hours}س {minutes}د{Colors.RESET}")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 تم إيقاف البرنامج. وداعاً!{Colors.RESET}")
        print(f"{Colors.GREEN}📊 إحصائيات الجلسة:{Colors.RESET}")
        print(f"   إجمالي OTP: {total_otps}")
        print(f"   الرسائل المخزنة: {len(all_messages)}")
        sys.exit(0)

# ============================================
# متغيرات عامة
# ============================================
bot_start_time = datetime.now()

# ============================================
# نقطة البداية
# ============================================
if __name__ == "__main__":
    # التحقق من وجود المكتبات المطلوبة
    try:
        import requests
        from dotenv import load_dotenv
    except ImportError as e:
        print("❌ المكتبات المطلوبة غير مثبتة!")
        print("📦 قم بتثبيتها باستخدام:")
        print("   pip install requests python-dotenv")
        sys.exit(1)
    
    main()
