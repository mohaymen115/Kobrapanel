
# =====================================================
# OTP KING - ULTIMATE FINAL MERGED VERSION
# (ALL FILES MERGED TOGETHER)
# =====================================================


# ============================================
# OTP KING - FINAL MERGED VERSION
# (main.py + templates.py in one file)
# ============================================

"""
TM SMS PANEL - HTML Templates
Version: 2.0
"""

#============================================
# CSS Styles المشتركة
#============================================

BASE_CSS = '''
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-primary: #06060a;
        --bg-secondary: #0c0c12;
        --bg-card: #12121a;
        --bg-card-hover: #1a1a24;
        --bg-input: #0a0a10;
        --accent: #8b5cf6;
        --accent-light: #a78bfa;
        --accent-dark: #7c3aed;
        --accent-glow: rgba(139, 92, 246, 0.25);
        --success: #10b981;
        --success-glow: rgba(16, 185, 129, 0.25);
        --warning: #f59e0b;
        --danger: #ef4444;
        --danger-glow: rgba(239, 68, 68, 0.25);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border: #1e1e2d;
        --border-light: #2a2a3d;
    }
    
    body {
        font-family: 'Cairo', 'Segoe UI', system-ui, -apple-system, sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
        min-height: 100vh;
        direction: rtl;
        line-height: 1.6;
    }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-secondary); }
    ::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }
    
    a { text-decoration: none; color: inherit; }
    
    /* ===== HEADER ===== */
    .header {
        background: rgba(12, 12, 18, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
        padding: 14px 24px;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .header-content {
        max-width: 1600px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, var(--accent), var(--accent-light));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 20px var(--accent-glow);
    }
    
    .logo-text {
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, #fff, var(--accent-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Navigation */
    .nav {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .nav-link {
        padding: 10px 18px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text-secondary);
        font-size: 13px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover {
        background: var(--bg-card-hover);
        color: var(--text-primary);
        border-color: var(--accent);
        transform: translateY(-2px);
    }
    
    .nav-link.active {
        background: linear-gradient(135deg, var(--accent), var(--accent-dark));
        color: white;
        border-color: transparent;
        box-shadow: 0 4px 15px var(--accent-glow);
    }
    
    .nav-link.danger {
        color: var(--danger);
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    .nav-link.danger:hover {
        background: var(--danger);
        color: white;
        border-color: var(--danger);
    }
    
    /* User Badge */
    .user-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .user-badge {
        background: var(--bg-card);
        border: 1px solid var(--border);
        padding: 10px 18px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #ec4899, #f97316);
        border: none;
        color: white;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    }
    
    /* ===== CONTAINER ===== */
    .container {
        max-width: 1600px;
        margin: 0 auto;
        padding: 24px;
    }
    
    /* ===== CARDS ===== */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border);
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* ===== STATS GRID ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 28px;
    }
    
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent-light));
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: var(--accent);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .stat-icon {
        font-size: 40px;
        margin-bottom: 12px;
        display: block;
    }
    
    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--accent-light);
        display: block;
    }
    
    .stat-label {
        font-size: 13px;
        color: var(--text-muted);
        margin-top: 6px;
    }
    
    /* ===== BUTTONS ===== */
    .btn {
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        font-family: inherit;
        font-size: 14px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--accent), var(--accent-dark));
        color: white;
        box-shadow: 0 4px 15px var(--accent-glow);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px var(--accent-glow);
    }
    
    .btn-secondary {
        background: var(--bg-card-hover);
        color: var(--text-primary);
        border: 1px solid var(--border);
    }
    
    .btn-secondary:hover {
        border-color: var(--accent);
        background: var(--bg-card);
    }
    
    .btn-success {
        background: var(--success);
        color: white;
    }
    
    .btn-warning {
        background: var(--warning);
        color: black;
    }
    
    .btn-danger {
        background: var(--danger);
        color: white;
    }
    
    .btn-sm {
        padding: 8px 14px;
        font-size: 12px;
        border-radius: 8px;
    }
    
    .btn-lg {
        padding: 16px 32px;
        font-size: 16px;
    }
    
    /* ===== FORMS ===== */
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 10px;
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
    }
    
    .form-control {
        width: 100%;
        padding: 14px 18px;
        border: 2px solid var(--border);
        border-radius: 12px;
        background: var(--bg-input);
        color: var(--text-primary);
        font-size: 15px;
        font-family: inherit;
        transition: all 0.3s;
    }
    
    .form-control:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 4px var(--accent-glow);
    }
    
    .form-control::placeholder {
        color: var(--text-muted);
    }
    
    textarea.form-control {
        min-height: 120px;
        resize: vertical;
    }
    
    /* ===== TABLES ===== */
    .table-container {
        overflow-x: auto;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
    }
    
    th, td {
        padding: 16px;
        text-align: right;
        border-bottom: 1px solid var(--border);
    }
    
    th {
        background: var(--bg-secondary);
        color: var(--accent-light);
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    tr:hover {
        background: var(--bg-card-hover);
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    /* ===== BADGES ===== */
    .badge {
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-danger {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .badge-primary {
        background: rgba(139, 92, 246, 0.15);
        color: var(--accent-light);
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    /* ===== COUNTRIES GRID - تصميم محسن ===== */
    .countries-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 24px;
    }
    
    .country-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }
    
    .country-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, var(--accent), var(--accent-light));
        opacity: 0;
        transition: opacity 0.4s;
        z-index: 0;
    }
    
    .country-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: var(--accent);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.25);
    }
    
    .country-card:hover::before {
        opacity: 0.05;
    }
    
    .country-card-inner {
        position: relative;
        z-index: 1;
    }
    
    .country-flag {
        font-size: 80px;
        margin-bottom: 20px;
        display: block;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
        transition: transform 0.4s;
    }
    
    .country-card:hover .country-flag {
        transform: scale(1.15) rotate(5deg);
    }
    
    .country-name {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 6px;
        color: var(--text-primary);
    }
    
    .country-code {
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 24px;
        font-weight: 500;
    }
    
    .country-stats {
        display: flex;
        justify-content: center;
        gap: 32px;
        padding-top: 24px;
        border-top: 1px solid var(--border);
    }
    
    .country-stat {
        text-align: center;
    }
    
    .country-stat-value {
        font-size: 28px;
        font-weight: 700;
        display: block;
        line-height: 1.2;
    }
    
    .country-stat-value.available {
        color: var(--success);
        text-shadow: 0 0 20px var(--success-glow);
    }
    
    .country-stat-value.used {
        color: var(--danger);
    }
    
    .country-stat-value.total {
        color: var(--accent-light);
    }
    
    .country-stat-label {
        font-size: 11px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* ===== NUMBERS LIST ===== */
    .numbers-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
        gap: 16px;
    }
    
    .number-item {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s;
    }
    
    .number-item:hover {
        border-color: var(--accent);
        background: var(--bg-card-hover);
        transform: translateX(-5px);
    }
    
    .number-item.used {
        opacity: 0.5;
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    .number-display {
        font-size: 22px;
        font-weight: 600;
        font-family: 'Courier New', monospace;
        color: var(--text-primary);
        direction: ltr;
        text-align: left;
        letter-spacing: 1px;
    }
    
    .number-status {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 6px;
    }
    
    .number-actions {
        display: flex;
        gap: 8px;
        flex-shrink: 0;
    }
    
    /* ===== OTP MESSAGES - تصميم محسن مع إظهار الدولة والرقم ===== */
    .otp-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
        gap: 24px;
    }
    
    .otp-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        overflow: hidden;
        transition: all 0.3s;
    }
    
    .otp-card:hover {
        border-color: var(--accent);
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    .otp-header {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card));
        padding: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--border);
    }
    
    .otp-country-info {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .otp-flag {
        font-size: 48px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .otp-country-details {
        text-align: right;
    }
    
    .otp-country-name {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    
    .otp-phone {
        font-size: 16px;
        color: var(--accent-light);
        font-family: 'Courier New', monospace;
        direction: ltr;
        display: inline-block;
        background: rgba(139, 92, 246, 0.1);
        padding: 4px 12px;
        border-radius: 8px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .otp-service {
        background: linear-gradient(135deg, var(--accent), var(--accent-dark));
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 600;
        color: white;
        box-shadow: 0 4px 15px var(--accent-glow);
    }
    
    .otp-body {
        padding: 28px;
    }
    
    .otp-code-box {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(167, 139, 250, 0.05));
        border: 2px solid var(--accent);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .otp-code-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    .otp-code-label {
        position: relative;
        font-size: 12px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 12px;
    }
    
    .otp-code-value {
        position: relative;
        font-size: 48px;
        font-weight: 700;
        color: var(--accent-light);
        letter-spacing: 8px;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 40px var(--accent-glow);
    }
    
    .otp-copy-btn {
        position: relative;
        margin-top: 20px;
        background: var(--accent);
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s;
        font-family: inherit;
    }
    
    .otp-copy-btn:hover {
        background: var(--accent-light);
        transform: scale(1.05);
    }
    
    .otp-message {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        font-size: 14px;
        color: var(--text-secondary);
        direction: ltr;
        text-align: left;
        line-height: 1.7;
        max-height: 120px;
        overflow-y: auto;
    }
    
    .otp-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid var(--border);
    }
    
    .otp-time {
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .otp-id {
        font-size: 11px;
        color: var(--text-muted);
        font-family: monospace;
        direction: ltr;
    }
    
    /* ===== MODAL ===== */
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(8px);
        z-index: 2000;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .modal.active {
        display: flex;
    }
    
    .modal-content {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 36px;
        width: 100%;
        max-width: 540px;
        max-height: 90vh;
        overflow-y: auto;
        animation: modalSlide 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes modalSlide {
        from {
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 28px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border);
    }
    
    .modal-title {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .close-btn {
        background: var(--bg-card-hover);
        border: 1px solid var(--border);
        color: var(--text-primary);
        font-size: 20px;
        cursor: pointer;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }
    
    .close-btn:hover {
        background: var(--danger);
        border-color: var(--danger);
        transform: rotate(90deg);
    }
    
    /* ===== ALERTS ===== */
    .alert {
        padding: 18px 24px;
        border-radius: 14px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        animation: alertSlide 0.4s ease;
    }
    
    @keyframes alertSlide {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid var(--success);
        color: var(--success);
    }
    
    .alert-danger {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid var(--danger);
        color: var(--danger);
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid var(--warning);
        color: var(--warning);
    }
    
    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 80px 20px;
    }
    
    .empty-icon {
        font-size: 100px;
        margin-bottom: 24px;
        opacity: 0.3;
        filter: grayscale(100%);
    }
    
    .empty-title {
        font-size: 28px;
        color: var(--text-secondary);
        margin-bottom: 12px;
    }
    
    .empty-text {
        color: var(--text-muted);
        margin-bottom: 28px;
        font-size: 16px;
    }
    
    /* ===== SEARCH ===== */
    .search-box {
        position: relative;
        max-width: 400px;
    }
    
    .search-box input {
        width: 100%;
        padding: 14px 20px 14px 50px;
        background: var(--bg-input);
        border: 2px solid var(--border);
        border-radius: 14px;
        color: var(--text-primary);
        font-size: 15px;
        font-family: inherit;
    }
    
    .search-box input:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 4px var(--accent-glow);
    }
    
    .search-icon {
        position: absolute;
        left: 18px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-muted);
        font-size: 18px;
    }
    
    /* ===== FILE UPLOAD ===== */
    .file-upload {
        border: 2px dashed var(--border);
        border-radius: 16px;
        padding: 48px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        background: var(--bg-secondary);
    }
    
    .file-upload:hover {
        border-color: var(--accent);
        background: var(--bg-card-hover);
    }
    
    .file-upload-icon {
        font-size: 56px;
        margin-bottom: 18px;
        color: var(--accent-light);
    }
    
    .file-upload-text {
        color: var(--text-secondary);
    }
    
    .file-upload-text strong {
        color: var(--accent-light);
    }
    
    /* ===== API KEY BOX ===== */
    .api-key-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
        position: relative;
        direction: ltr;
        text-align: left;
    }
    
    .api-key-value {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: var(--accent-light);
        word-break: break-all;
        padding-left: 80px;
    }
    
    .api-key-copy {
        position: absolute;
        top: 50%;
        left: 12px;
        transform: translateY(-50%);
        background: var(--accent);
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        color: white;
        font-size: 12px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .api-key-copy:hover {
        background: var(--accent-light);
    }
    
    /* ===== CODE BLOCK ===== */
    .code-block {
        background: #0d0d14;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 20px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: var(--text-secondary);
        direction: ltr;
        text-align: left;
        margin: 16px 0;
    }
    
    .code-block .method { color: #c792ea; font-weight: bold; }
    .code-block .url { color: #82aaff; }
    .code-block .string { color: #c3e88d; }
    .code-block .key { color: #f78c6c; }
    .code-block .comment { color: #546e7a; font-style: italic; }
    
    /* ===== STATUS DOT ===== */
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-left: 8px;
    }
    
    .status-dot.online {
        background: var(--success);
        box-shadow: 0 0 10px var(--success);
        animation: pulse 2s infinite;
    }
    
    .status-dot.offline {
        background: var(--danger);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ===== BACK BUTTON ===== */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        color: var(--text-secondary);
        margin-bottom: 24px;
        padding: 12px 0;
        font-size: 14px;
        transition: color 0.3s;
    }
    
    .back-btn:hover {
        color: var(--accent-light);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .header-content { flex-direction: column; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .countries-grid { grid-template-columns: 1fr; }
        .numbers-grid { grid-template-columns: 1fr; }
        .otp-grid { grid-template-columns: 1fr; }
        .otp-code-value { font-size: 32px; letter-spacing: 4px; }
        .country-flag { font-size: 60px; }
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
'''

#============================================
# Login Template
#============================================

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - تسجيل الدخول</title>
    ''' + BASE_CSS + '''
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: radial-gradient(ellipse at top, #12121a 0%, #06060a 50%);
        }
        
        .login-wrapper {
            width: 100%;
            max-width: 440px;
            padding: 20px;
        }
        
        .login-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 32px;
            padding: 56px 44px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .login-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-light), var(--accent));
        }
        
        .login-logo {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, var(--accent), var(--accent-light));
            border-radius: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 52px;
            margin: 0 auto 32px;
            box-shadow: 0 15px 50px var(--accent-glow);
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .login-title {
            font-size: 34px;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, var(--accent-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .login-subtitle {
            color: var(--text-muted);
            margin-bottom: 40px;
            font-size: 15px;
        }
        
        .login-form .form-control {
            text-align: right;
            padding: 18px 22px;
            font-size: 16px;
        }
        
        .login-btn {
            width: 100%;
            padding: 18px;
            font-size: 18px;
            margin-top: 10px;
        }
        
        .login-footer {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
            font-size: 12px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-logo">📱</div>
            <h1 class="login-title">TM SMS PANEL</h1>
            <p class="login-subtitle">لوحة التحكم الاحترافية لإدارة الرسائل</p>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST" class="login-form">
                <div class="form-group">
                    <input type="text" name="username" class="form-control" placeholder="👤  اسم المستخدم" required autofocus>
                </div>
                <div class="form-group">
                    <input type="password" name="password" class="form-control" placeholder="🔑  كلمة المرور" required>
                </div>
                <button type="submit" class="btn btn-primary login-btn">
                    🚀 تسجيل الدخول
                </button>
            </form>
            
            <div class="login-footer">
                © 2024 TM SMS PANEL - جميع الحقوق محفوظة
            </div>
        </div>
    </div>
</body>
</html>
'''

#============================================
# Dashboard Template
#============================================

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - الرئيسية</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">📱</div>
                <span class="logo-text">TM SMS PANEL</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link active">🏠 الرئيسية</a>
                <a href="{{ url_for('numbers_page') }}" class="nav-link">📞 الأرقام</a>
                <a href="{{ url_for('otp_messages') }}" class="nav-link">📨 رسائل OTP</a>
                {% if current_user.role == 'admin' %}
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ لوحة التحكم</a>
                {% endif %}
            </nav>
            
            <div class="user-info">
                <div class="user-badge {{ 'admin-badge' if current_user.role == 'admin' else '' }}">
                    {{ '👑' if current_user.role == 'admin' else '👤' }}
                    {{ current_user.username }}
                </div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon">🌍</span>
                <span class="stat-value">{{ total_countries }}</span>
                <div class="stat-label">الدول المتاحة</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">📱</span>
                <span class="stat-value">{{ total_numbers }}</span>
                <div class="stat-label">إجمالي الأرقام</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">✅</span>
                <span class="stat-value">{{ available_numbers }}</span>
                <div class="stat-label">أرقام متاحة</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">📨</span>
                <span class="stat-value">{{ total_otp }}</span>
                <div class="stat-label">رسائل OTP</div>
            </div>
        </div>
        
        <!-- Countries -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">🌍 الدول المتاحة</h2>
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span class="badge badge-primary">
                        <span class="status-dot {{ 'online' if stats.is_running else 'offline' }}"></span>
                        {{ stats.scraper_status }}
                    </span>
                    {% if current_user.role == 'admin' %}
                    <a href="{{ url_for('manage_countries') }}" class="btn btn-primary btn-sm">➕ إدارة الدول</a>
                    {% endif %}
                </div>
            </div>
            
            {% if countries %}
            <div class="countries-grid">
                {% for country in countries %}
                <a href="{{ url_for('country_numbers', country_id=country.id) }}" class="country-card">
                    <div class="country-card-inner">
                        <span class="country-flag">{{ country.flag }}</span>
                        <div class="country-name">{{ country.name }}</div>
                        <div class="country-code">{{ country.code }}</div>
                        <div class="country-stats">
                            <div class="country-stat">
                                <span class="country-stat-value available">{{ country.available or 0 }}</span>
                                <div class="country-stat-label">متاح</div>
                            </div>
                            <div class="country-stat">
                                <span class="country-stat-value used">{{ (country.total or 0) - (country.available or 0) }}</span>
                                <div class="country-stat-label">مستخدم</div>
                            </div>
                            <div class="country-stat">
                                <span class="country-stat-value total">{{ country.total or 0 }}</span>
                                <div class="country-stat-label">الإجمالي</div>
                            </div>
                        </div>
                    </div>
                </a>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-icon">🌍</div>
                <div class="empty-title">لا توجد دول مضافة</div>
                <p class="empty-text">{{ 'قم بإضافة دول من لوحة التحكم' if current_user.role == 'admin' else 'تواصل مع المدير لإضافة دول' }}</p>
                {% if current_user.role == 'admin' %}
                <a href="{{ url_for('manage_countries') }}" class="btn btn-primary btn-lg">➕ إضافة أول دولة</a>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

#============================================
# Numbers Page Template
#============================================

NUMBERS_PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - الأرقام</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">📱</div>
                <span class="logo-text">TM SMS PANEL</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('numbers_page') }}" class="nav-link active">📞 الأرقام</a>
                <a href="{{ url_for('otp_messages') }}" class="nav-link">📨 رسائل OTP</a>
                {% if current_user.role == 'admin' %}
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ لوحة التحكم</a>
                {% endif %}
            </nav>
            
            <div class="user-info">
                <div class="user-badge {{ 'admin-badge' if current_user.role == 'admin' else '' }}">
                    {{ '👑' if current_user.role == 'admin' else '👤' }}
                    {{ current_user.username }}
                </div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">🌍 اختر الدولة لعرض الأرقام</h2>
            </div>
            
            {% if countries %}
            <div class="countries-grid">
                {% for country in countries %}
                <a href="{{ url_for('country_numbers', country_id=country.id) }}" class="country-card">
                    <div class="country-card-inner">
                        <span class="country-flag">{{ country.flag }}</span>
                        <div class="country-name">{{ country.name }}</div>
                        <div class="country-code">{{ country.code }}</div>
                        <div class="country-stats">
                            <div class="country-stat">
                                <span class="country-stat-value available">{{ country.available or 0 }}</span>
                                <div class="country-stat-label">متاح</div>
                            </div>
                            <div class="country-stat">
                                <span class="country-stat-value used">{{ country.used or 0 }}</span>
                                <div class="country-stat-label">مستخدم</div>
                            </div>
                        </div>
                    </div>
                </a>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-title">لا توجد دول متاحة</div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

#============================================
# Country Numbers Template
#============================================

COUNTRY_NUMBERS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - {{ country.name }}</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">📱</div>
                <span class="logo-text">TM SMS PANEL</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('numbers_page') }}" class="nav-link active">📞 الأرقام</a>
                <a href="{{ url_for('otp_messages') }}" class="nav-link">📨 رسائل OTP</a>
                {% if current_user.role == 'admin' %}
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ لوحة التحكم</a>
                {% endif %}
            </nav>
            
            <div class="user-info">
                <div class="user-badge {{ 'admin-badge' if current_user.role == 'admin' else '' }}">
                    {{ '👑' if current_user.role == 'admin' else '👤' }}
                    {{ current_user.username }}
                </div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <a href="{{ url_for('numbers_page') }}" class="back-btn">← العودة للدول</a>
        
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">
                    <span style="font-size: 40px;">{{ country.flag }}</span>
                    أرقام {{ country.name }}
                </h2>
                <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                    <span class="badge badge-success">✅ {{ available_count }} متاح</span>
                    <span class="badge badge-danger">❌ {{ used_count }} مستخدم</span>
                    {% if current_user.role == 'admin' %}
                    <button class="btn btn-primary btn-sm" onclick="openModal('addModal')">➕ إضافة أرقام</button>
                    {% endif %}
                </div>
            </div>
            
            <!-- Filter -->
            <div style="margin-bottom: 24px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center;">
                <div class="search-box" style="flex: 1; min-width: 280px;">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchInput" placeholder="بحث عن رقم..." onkeyup="filterNumbers()">
                </div>
                <select id="statusFilter" class="form-control" style="width: auto; min-width: 160px;" onchange="filterNumbers()">
                    <option value="all">📋 جميع الأرقام</option>
                    <option value="available">✅ متاح فقط</option>
                    <option value="used">❌ مستخدم فقط</option>
                </select>
            </div>
            
            {% if numbers %}
            <div class="numbers-grid" id="numbersList">
                {% for n in numbers %}
                <div class="number-item {{ 'used' if n.status == 'used' else '' }}" 
                     data-status="{{ n.status }}" 
                     data-phone="{{ n.phone_number }}">
                    <div>
                        <div class="number-display">{{ n.phone_number }}</div>
                        <div class="number-status">
                            {% if n.status == 'available' %}
                            <span style="color: var(--success);">✅ متاح للاستخدام</span>
                            {% else %}
                            <span style="color: var(--danger);">❌ مستخدم</span>
                            {% if n.used_at %} - {{ n.used_at[:16] }}{% endif %}
                            {% endif %}
                        </div>
                    </div>
                    <div class="number-actions">
                        <button class="btn btn-secondary btn-sm" onclick="copyNumber('{{ n.phone_number }}', this)">📋 نسخ</button>
                        {% if current_user.role == 'admin' %}
                        <form method="POST" action="{{ url_for('change_number_status', number_id=n.id, status='used' if n.status == 'available' else 'available') }}" style="display:inline;">
                            <button type="submit" class="btn btn-sm {{ 'btn-warning' if n.status == 'available' else 'btn-success' }}">
                                {{ '❌' if n.status == 'available' else '✅' }}
                            </button>
                        </form>
                        <form method="POST" action="{{ url_for('delete_number', number_id=n.id) }}" style="display:inline;" onsubmit="return confirm('حذف هذا الرقم؟');">
                            <button type="submit" class="btn btn-danger btn-sm">🗑️</button>
                        </form>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-icon">📱</div>
                <div class="empty-title">لا توجد أرقام</div>
                {% if current_user.role == 'admin' %}
                <button class="btn btn-primary btn-lg" onclick="openModal('addModal')">➕ إضافة أرقام</button>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
    
    {% if current_user.role == 'admin' %}
    <!-- Add Numbers Modal -->
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">➕ إضافة أرقام جديدة</h3>
                <button class="close-btn" onclick="closeModal('addModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_numbers', country_id=country.id) }}" enctype="multipart/form-data">
                <div class="form-group">
                    <label>📄 ملف الأرقام (.txt)</label>
                    <div class="file-upload" onclick="document.getElementById('fileInput').click()">
                        <div class="file-upload-icon">📁</div>
                        <div class="file-upload-text">
                            <strong>اضغط لاختيار ملف</strong><br>
                            <small>كل رقم في سطر منفصل</small>
                        </div>
                        <input type="file" id="fileInput" name="file" accept=".txt" style="display:none;" onchange="showFileName(this)">
                    </div>
                    <div id="fileName" style="margin-top: 12px; color: var(--accent-light); text-align: center;"></div>
                </div>
                
                <div class="form-group">
                    <label>✏️ أو أدخل الأرقام يدوياً (كل رقم في سطر)</label>
                    <textarea name="numbers_text" class="form-control" rows="6" placeholder="+1234567890&#10;+0987654321&#10;..." style="direction: ltr; text-align: left;"></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">➕ إضافة الأرقام</button>
            </form>
        </div>
    </div>
    {% endif %}

    <script>
        function copyNumber(text, btn) {
            navigator.clipboard.writeText(text);
            const original = btn.innerHTML;
            btn.innerHTML = '✅ تم';
            btn.style.background = 'var(--success)';
            setTimeout(() => {
                btn.innerHTML = original;
                btn.style.background = '';
            }, 1500);
        }
        
        function filterNumbers() {
            const search = document.getElementById('searchInput').value.toLowerCase();
            const status = document.getElementById('statusFilter').value;
            
            document.querySelectorAll('.number-item').forEach(item => {
                const phone = item.dataset.phone.toLowerCase();
                const itemStatus = item.dataset.status;
                
                const matchSearch = phone.includes(search);
                const matchStatus = status === 'all' || itemStatus === status;
                
                item.style.display = (matchSearch && matchStatus) ? 'flex' : 'none';
            });
        }
        
        function openModal(id) {
            document.getElementById(id).classList.add('active');
        }
        
        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }
        
        function showFileName(input) {
            const name = input.files[0]?.name;
            document.getElementById('fileName').textContent = name ? '📄 ' + name : '';
        }
        
        // Close modal on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', e => {
                if (e.target === modal) modal.classList.remove('active');
            });
        });
    </script>
</body>
</html>
'''

#============================================
# OTP Messages Template (محسن مع إظهار الدولة والرقم)
#============================================

OTP_MESSAGES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - رسائل OTP</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">📱</div>
                <span class="logo-text">TM SMS PANEL</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('numbers_page') }}" class="nav-link">📞 الأرقام</a>
                <a href="{{ url_for('otp_messages') }}" class="nav-link active">📨 رسائل OTP</a>
                {% if current_user.role == 'admin' %}
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ لوحة التحكم</a>
                {% endif %}
            </nav>
            
            <div class="user-info">
                <div class="user-badge {{ 'admin-badge' if current_user.role == 'admin' else '' }}">
                    {{ '👑' if current_user.role == 'admin' else '👤' }}
                    {{ current_user.username }}
                </div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">📨 رسائل OTP الواردة</h2>
                <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                    <span class="badge badge-primary">
                        <span class="status-dot {{ 'online' if stats.is_running else 'offline' }}"></span>
                        {{ messages|length }} رسالة
                    </span>
                    <button class="btn btn-primary btn-sm" onclick="location.reload()">🔄 تحديث</button>
                    {% if current_user.role == 'admin' %}
                    <form method="POST" action="{{ url_for('clear_otp') }}" style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('مسح جميع الرسائل؟')">🗑️ مسح الكل</button>
                    </form>
                    {% endif %}
                </div>
            </div>
            
            {% if messages %}
            <div class="otp-grid">
                {% for msg in messages %}
                <div class="otp-card">
                    <div class="otp-header">
                        <div class="otp-country-info">
                            <span class="otp-flag">{{ msg.country_flag or '🌍' }}</span>
                            <div class="otp-country-details">
                                <div class="otp-country-name">{{ msg.country_name or msg.country or 'غير معروف' }}</div>
                                <span class="otp-phone">{{ msg.phone_number or 'غير معروف' }}</span>
                            </div>
                        </div>
                        <span class="otp-service">{{ msg.service or 'SMS' }}</span>
                    </div>
                    
                    <div class="otp-body">
                        <div class="otp-code-box">
                            <div class="otp-code-label">🔐 كود التحقق</div>
                            <div class="otp-code-value">{{ msg.otp_code or msg.otp or 'N/A' }}</div>
                            <button class="otp-copy-btn" onclick="copyOTP('{{ msg.otp_code or msg.otp or '' }}', this)">
                                📋 نسخ الكود
                            </button>
                        </div>
                        
                        <div class="otp-message">{{ msg.raw_message or 'لا توجد رسالة' }}</div>
                        
                        <div class="otp-footer">
                            <span class="otp-time">⏰ {{ msg.received_at or msg.timestamp or 'غير معروف' }}</span>
                            <span class="otp-id">#{{ msg.id or msg.message_id or '' }}</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-title">لا توجد رسائل OTP</div>
                <p class="empty-text">في انتظار استقبال رسائل جديدة...</p>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        function copyOTP(code, btn) {
            if (!code || code === 'N/A') return;
            
            navigator.clipboard.writeText(code.replace(/-/g, ''));
            const original = btn.innerHTML;
            btn.innerHTML = '✅ تم النسخ!';
            btn.style.background = 'var(--success)';
            
            setTimeout(() => {
                btn.innerHTML = original;
                btn.style.background = '';
            }, 2000);
        }
        
        // Auto refresh every 15 seconds
        setTimeout(() => location.reload(), 15000);
    </script>
</body>
</html>
'''

#============================================
# Admin Panel Template
#============================================

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - لوحة التحكم</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">⚙️</div>
                <span class="logo-text">لوحة التحكم</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('manage_countries') }}" class="nav-link">🌍 الدول</a>
                <a href="{{ url_for('manage_users') }}" class="nav-link">👥 المستخدمين</a>
                <a href="{{ url_for('api_settings') }}" class="nav-link">🔗 API</a>
                <a href="{{ url_for('admin_panel') }}" class="nav-link active">⚙️ الإعدادات</a>
            </nav>
            
            <div class="user-info">
                <div class="user-badge admin-badge">👑 {{ current_user.username }}</div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-icon">👥</span>
                <span class="stat-value">{{ stats.users }}</span>
                <div class="stat-label">المستخدمين</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">🌍</span>
                <span class="stat-value">{{ stats.countries }}</span>
                <div class="stat-label">الدول</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">📱</span>
                <span class="stat-value">{{ stats.numbers }}</span>
                <div class="stat-label">الأرقام</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">✅</span>
                <span class="stat-value">{{ stats.available }}</span>
                <div class="stat-label">متاح</div>
            </div>
            <div class="stat-card">
                <span class="stat-icon">📨</span>
                <span class="stat-value">{{ stats.messages }}</span>
                <div class="stat-label">رسائل OTP</div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">⚡ إجراءات سريعة</h2>
            </div>
            <div style="display: flex; gap: 14px; flex-wrap: wrap;">
                <a href="{{ url_for('manage_countries') }}" class="btn btn-primary">🌍 إدارة الدول</a>
                <a href="{{ url_for('manage_users') }}" class="btn btn-primary">👥 إدارة المستخدمين</a>
                <a href="{{ url_for('api_settings') }}" class="btn btn-secondary">🔗 إعدادات API</a>
                <button class="btn btn-secondary" onclick="fetch('/api/refresh').then(() => location.reload())">🔄 تحديث الرسائل</button>
            </div>
        </div>
        
        <!-- Activity Log -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">📋 سجل النشاطات</h2>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>الوقت</th>
                            <th>المستخدم</th>
                            <th>الإجراء</th>
                            <th>التفاصيل</th>
                            <th>IP</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for a in activities %}
                        <tr>
                            <td>{{ a.timestamp[:16] if a.timestamp else '-' }}</td>
                            <td>{{ a.username or 'النظام' }}</td>
                            <td>{{ a.action }}</td>
                            <td>{{ a.details or '-' }}</td>
                            <td style="direction: ltr; text-align: left;">{{ a.ip_address or '-' }}</td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" style="text-align: center; color: var(--text-muted); padding: 40px;">
                                لا توجد نشاطات مسجلة
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
'''

#============================================
# Manage Countries Template
#============================================

MANAGE_COUNTRIES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - إدارة الدول</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">🌍</div>
                <span class="logo-text">إدارة الدول</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('manage_countries') }}" class="nav-link active">🌍 الدول</a>
                <a href="{{ url_for('manage_users') }}" class="nav-link">👥 المستخدمين</a>
                <a href="{{ url_for('api_settings') }}" class="nav-link">🔗 API</a>
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ الإعدادات</a>
            </nav>
            
            <div class="user-info">
                <div class="user-badge admin-badge">👑 {{ current_user.username }}</div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">🌍 الدول المضافة</h2>
                <button class="btn btn-primary" onclick="openModal('addModal')">➕ إضافة دولة جديدة</button>
            </div>
            
            {% if countries %}
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>العلم</th>
                            <th>الاسم</th>
                            <th>الكود</th>
                            <th>إجمالي الأرقام</th>
                            <th>متاح</th>
                            <th>الحالة</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for c in countries %}
                        <tr>
                            <td style="font-size: 32px;">{{ c.flag }}</td>
                            <td style="font-weight: 600;">{{ c.name }}</td>
                            <td>{{ c.code }}</td>
                            <td>{{ c.total or 0 }}</td>
                            <td><span class="badge badge-success">{{ c.available or 0 }}</span></td>
                            <td>
                                <span class="badge {{ 'badge-success' if c.is_active else 'badge-danger' }}">
                                    {{ '✅ نشط' if c.is_active else '❌ موقوف' }}
                                </span>
                            </td>
                            <td>
                                <a href="{{ url_for('country_numbers', country_id=c.id) }}" class="btn btn-secondary btn-sm">📱</a>
                                <button class="btn btn-sm" style="background: var(--accent); color: white;" onclick="editCountry({{ c.id }}, '{{ c.name }}', '{{ c.code }}', '{{ c.flag }}')">✏️</button>
                                <form method="POST" action="{{ url_for('toggle_country', country_id=c.id) }}" style="display:inline;">
                                    <button type="submit" class="btn btn-sm {{ 'btn-warning' if c.is_active else 'btn-success' }}">
                                        {{ '⏸️' if c.is_active else '▶️' }}
                                    </button>
                                </form>
                                <form method="POST" action="{{ url_for('delete_country', country_id=c.id) }}" style="display:inline;" onsubmit="return confirm('حذف هذه الدولة وجميع أرقامها؟');">
                                    <button type="submit" class="btn btn-danger btn-sm">🗑️</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state">
                <div class="empty-icon">🌍</div>
                <div class="empty-title">لا توجد دول</div>
                <p class="empty-text">ابدأ بإضافة أول دولة</p>
                <button class="btn btn-primary btn-lg" onclick="openModal('addModal')">➕ إضافة دولة</button>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Add Country Modal -->
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">➕ إضافة دولة جديدة</h3>
                <button class="close-btn" onclick="closeModal('addModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_country') }}" enctype="multipart/form-data">
                <div class="form-group">
                    <label>🏷️ اسم الدولة</label>
                    <input type="text" name="name" class="form-control" placeholder="مثال: مصر" required>
                </div>
                <div class="form-group">
                    <label>🔤 كود الدولة (حرفين أو ثلاثة)</label>
                    <input type="text" name="code" class="form-control" placeholder="EG" required maxlength="5" style="text-transform: uppercase;">
                </div>
                <div class="form-group">
                    <label>🎌 علم الدولة (Emoji)</label>
                    <input type="text" name="flag" class="form-control" placeholder="🇪🇬" value="🌍">
                    <small style="color: var(--text-muted); margin-top: 6px; display: block;">
                        انسخ العلم من <a href="https://emojipedia.org/flags" target="_blank" style="color: var(--accent-light);">emojipedia.org/flags</a>
                    </small>
                </div>
                <div class="form-group">
                    <label>📄 ملف الأرقام (.txt) - اختياري</label>
                    <input type="file" name="numbers_file" class="form-control" accept=".txt">
                </div>
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">➕ إضافة الدولة</button>
            </form>
        </div>
    </div>
    
    <!-- Edit Country Modal -->
    <div class="modal" id="editModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">✏️ تعديل الدولة</h3>
                <button class="close-btn" onclick="closeModal('editModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('edit_country') }}">
                <input type="hidden" name="country_id" id="edit_id">
                <div class="form-group">
                    <label>🏷️ اسم الدولة</label>
                    <input type="text" name="name" id="edit_name" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>🔤 كود الدولة</label>
                    <input type="text" name="code" id="edit_code" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>🎌 علم الدولة</label>
                    <input type="text" name="flag" id="edit_flag" class="form-control">
                </div>
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">💾 حفظ التعديلات</button>
            </form>
        </div>
    </div>

    <script>
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        
        function editCountry(id, name, code, flag) {
            document.getElementById('edit_id').value = id;
            document.getElementById('edit_name').value = name;
            document.getElementById('edit_code').value = code;
            document.getElementById('edit_flag').value = flag;
            openModal('editModal');
        }
        
        document.querySelectorAll('.modal').forEach(m => {
            m.addEventListener('click', e => { if (e.target === m) m.classList.remove('active'); });
        });
    </script>
</body>
</html>
'''

#============================================
# Manage Users Template
#============================================

MANAGE_USERS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - إدارة المستخدمين</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">👥</div>
                <span class="logo-text">إدارة المستخدمين</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('manage_countries') }}" class="nav-link">🌍 الدول</a>
                <a href="{{ url_for('manage_users') }}" class="nav-link active">👥 المستخدمين</a>
                <a href="{{ url_for('api_settings') }}" class="nav-link">🔗 API</a>
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ الإعدادات</a>
            </nav>
            
            <div class="user-info">
                <div class="user-badge admin-badge">👑 {{ current_user.username }}</div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">👥 المستخدمين</h2>
                <button class="btn btn-primary" onclick="openModal('addModal')">➕ إضافة مستخدم</button>
            </div>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>اسم المستخدم</th>
                            <th>البريد</th>
                            <th>الصلاحية</th>
                            <th>الحالة</th>
                            <th>آخر دخول</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for u in users %}
                        <tr>
                            <td>{{ u.id }}</td>
                            <td style="font-weight: 600;">{{ u.username }}</td>
                            <td>{{ u.email or '-' }}</td>
                            <td>
                                <span class="badge {{ 'badge-danger' if u.role == 'admin' else 'badge-primary' }}">
                                    {{ '👑 مدير' if u.role == 'admin' else '👤 مستخدم' }}
                                </span>
                            </td>
                            <td>
                                <span class="badge {{ 'badge-success' if u.is_active else 'badge-danger' }}">
                                    {{ '✅ نشط' if u.is_active else '❌ موقوف' }}
                                </span>
                            </td>
                            <td>{{ u.last_login[:16] if u.last_login else 'لم يسجل دخول' }}</td>
                            <td>
                                {% if u.id != current_user.id %}
                                <button class="btn btn-sm" style="background: var(--accent); color: white;" onclick="editUser({{ u.id }}, '{{ u.username }}', '{{ u.email or '' }}', '{{ u.role }}')">✏️</button>
                                <form method="POST" action="{{ url_for('toggle_user', user_id=u.id) }}" style="display:inline;">
                                    <button type="submit" class="btn btn-sm {{ 'btn-warning' if u.is_active else 'btn-success' }}">
                                        {{ '⏸️' if u.is_active else '▶️' }}
                                    </button>
                                </form>
                                <form method="POST" action="{{ url_for('delete_user', user_id=u.id) }}" style="display:inline;" onsubmit="return confirm('حذف هذا المستخدم؟');">
                                    <button type="submit" class="btn btn-danger btn-sm">🗑️</button>
                                </form>
                                {% else %}
                                <span style="color: var(--text-muted);">أنت</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Add User Modal -->
    <div class="modal" id="addModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">➕ إضافة مستخدم جديد</h3>
                <button class="close-btn" onclick="closeModal('addModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_user') }}">
                <div class="form-group">
                    <label>👤 اسم المستخدم</label>
                    <input type="text" name="username" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>📧 البريد الإلكتروني (اختياري)</label>
                    <input type="email" name="email" class="form-control">
                </div>
                <div class="form-group">
                    <label>🔑 كلمة المرور</label>
                    <input type="password" name="password" class="form-control" required minlength="6">
                </div>
                <div class="form-group">
                    <label>🔑 تأكيد كلمة المرور</label>
                    <input type="password" name="confirm_password" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>👑 الصلاحية</label>
                    <select name="role" class="form-control">
                        <option value="user">👤 مستخدم عادي</option>
                        <option value="admin">👑 مدير</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">➕ إنشاء الحساب</button>
            </form>
        </div>
    </div>
    
    <!-- Edit User Modal -->
    <div class="modal" id="editModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">✏️ تعديل المستخدم</h3>
                <button class="close-btn" onclick="closeModal('editModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('edit_user') }}">
                <input type="hidden" name="user_id" id="edit_user_id">
                <div class="form-group">
                    <label>👤 اسم المستخدم</label>
                    <input type="text" name="username" id="edit_username" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>📧 البريد الإلكتروني</label>
                    <input type="email" name="email" id="edit_email" class="form-control">
                </div>
                <div class="form-group">
                    <label>🔑 كلمة مرور جديدة (اتركها فارغة للإبقاء)</label>
                    <input type="password" name="password" class="form-control">
                </div>
                <div class="form-group">
                    <label>👑 الصلاحية</label>
                    <select name="role" id="edit_role" class="form-control">
                        <option value="user">👤 مستخدم عادي</option>
                        <option value="admin">👑 مدير</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">💾 حفظ التعديلات</button>
            </form>
        </div>
    </div>

    <script>
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        
        function editUser(id, username, email, role) {
            document.getElementById('edit_user_id').value = id;
            document.getElementById('edit_username').value = username;
            document.getElementById('edit_email').value = email;
            document.getElementById('edit_role').value = role;
            openModal('editModal');
        }
        
        document.querySelectorAll('.modal').forEach(m => {
            m.addEventListener('click', e => { if (e.target === m) m.classList.remove('active'); });
        });
    </script>
</body>
</html>
'''

#============================================
# API Settings Template (للمدير فقط)
#============================================

API_SETTINGS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TM SMS PANEL - إعدادات API</title>
    ''' + BASE_CSS + '''
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="{{ url_for('dashboard') }}" class="logo">
                <div class="logo-icon">🔗</div>
                <span class="logo-text">إعدادات API</span>
            </a>
            
            <nav class="nav">
                <a href="{{ url_for('dashboard') }}" class="nav-link">🏠 الرئيسية</a>
                <a href="{{ url_for('manage_countries') }}" class="nav-link">🌍 الدول</a>
                <a href="{{ url_for('manage_users') }}" class="nav-link">👥 المستخدمين</a>
                <a href="{{ url_for('api_settings') }}" class="nav-link active">🔗 API</a>
                <a href="{{ url_for('admin_panel') }}" class="nav-link">⚙️ الإعدادات</a>
            </nav>
            
            <div class="user-info">
                <div class="user-badge admin-badge">👑 {{ current_user.username }}</div>
                <a href="{{ url_for('logout') }}" class="nav-link danger">🚪</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- API Key Section -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">🔑 مفتاح API الخاص بك</h2>
                <form method="POST" action="{{ url_for('regenerate_api_key') }}">
                    <button type="submit" class="btn btn-warning btn-sm" onclick="return confirm('سيتم إلغاء المفتاح القديم. متأكد؟')">
                        🔄 إعادة توليد
                    </button>
                </form>
            </div>
            
            <div class="api-key-box">
                <button class="api-key-copy" onclick="copyApiKey()">📋 نسخ</button>
                <code class="api-key-value" id="apiKeyValue">{{ current_user.api_key or 'لم يتم توليد مفتاح' }}</code>
            </div>
            
            <p style="margin-top: 16px; color: var(--text-muted); font-size: 13px;">
                ⚠️ <strong>هام:</strong> حافظ على سرية هذا المفتاح! يُستخدم للوصول إلى API النظام وربط بوتات تليجرام.
            </p>
        </div>
        
        <!-- Telegram Bots Section -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">🤖 بوتات تليجرام</h2>
                <button class="btn btn-primary btn-sm" onclick="openModal('addBotModal')">➕ إضافة بوت</button>
            </div>
            
            <p style="margin-bottom: 20px; color: var(--text-secondary);">
                أضف بوتات تليجرام لاستقبال رسائل OTP تلقائياً عند وصولها.
            </p>
            
            {% if telegram_bots %}
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>الاسم</th>
                            <th>Chat ID</th>
                            <th>الحالة</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for bot in telegram_bots %}
                        <tr>
                            <td style="font-weight: 600;">{{ bot.name }}</td>
                            <td style="direction: ltr; font-family: monospace;">{{ bot.chat_id }}</td>
                            <td>
                                <span class="badge {{ 'badge-success' if bot.is_active else 'badge-danger' }}">
                                    {{ '✅ نشط' if bot.is_active else '❌ موقوف' }}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-secondary btn-sm" onclick="testBot({{ bot.id }})">🧪 تجربة</button>
                                <form method="POST" action="{{ url_for('toggle_telegram_bot', bot_id=bot.id) }}" style="display:inline;">
                                    <button type="submit" class="btn btn-sm {{ 'btn-warning' if bot.is_active else 'btn-success' }}">
                                        {{ '⏸️' if bot.is_active else '▶️' }}
                                    </button>
                                </form>
                                <form method="POST" action="{{ url_for('delete_telegram_bot', bot_id=bot.id) }}" style="display:inline;" onsubmit="return confirm('حذف هذا البوت؟');">
                                    <button type="submit" class="btn btn-danger btn-sm">🗑️</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state" style="padding: 40px;">
                <div class="empty-icon" style="font-size: 60px;">🤖</div>
                <div class="empty-title" style="font-size: 20px;">لا توجد بوتات مضافة</div>
                <p class="empty-text">أضف بوت تليجرام لاستقبال إشعارات OTP</p>
            </div>
            {% endif %}
        </div>
        
        <!-- API Documentation -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">📚 توثيق API</h2>
            </div>
            
            <!-- Authentication -->
            <h3 style="color: var(--accent-light); margin-bottom: 14px; font-size: 18px;">🔐 المصادقة (Authentication)</h3>
            <p style="color: var(--text-secondary); margin-bottom: 12px;">أضف مفتاح API في Header الطلب:</p>
            <div class="code-block">
                <span class="key">X-API-Key:</span> <span class="string">YOUR_API_KEY_HERE</span>
            </div>
            
            <!-- Receive OTP -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">📨 إرسال رسالة OTP للنظام</h3>
            <p style="color: var(--text-secondary); margin-bottom: 12px;">استخدم هذا الـ Endpoint لإرسال رسائل OTP:</p>
            <div class="code-block">
<span class="method">POST</span> <span class="url">{{ base_url }}/api/v1/otp/receive</span>

<span class="comment">// Headers:</span>
<span class="key">Content-Type:</span> <span class="string">application/json</span>
<span class="key">X-API-Key:</span> <span class="string">YOUR_API_KEY</span>

<span class="comment">// Body (JSON):</span>
{
    <span class="key">"phone_number"</span>: <span class="string">"+1234567890"</span>,
    <span class="key">"message"</span>: <span class="string">"Your verification code is 123456"</span>,
    <span class="key">"country"</span>: <span class="string">"United States"</span>,        <span class="comment">// اختياري</span>
    <span class="key">"country_flag"</span>: <span class="string">"🇺🇸"</span>,              <span class="comment">// اختياري</span>
    <span class="key">"service"</span>: <span class="string">"WhatsApp"</span>,              <span class="comment">// اختياري</span>
    <span class="key">"otp_code"</span>: <span class="string">"123456"</span>,               <span class="comment">// اختياري - يُستخرج تلقائياً</span>
    <span class="key">"sender"</span>: <span class="string">"WhatsApp"</span>                <span class="comment">// اختياري</span>
}
            </div>
            
            <!-- Get Messages -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">📋 جلب رسائل OTP</h3>
            <div class="code-block">
<span class="method">GET</span> <span class="url">{{ base_url }}/api/v1/otp/messages?limit=50&offset=0</span>

<span class="comment">// Response:</span>
{
    <span class="key">"success"</span>: true,
    <span class="key">"total"</span>: 150,
    <span class="key">"count"</span>: 50,
    <span class="key">"messages"</span>: [...]
}
            </div>
            
            <!-- Get Latest -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">🔔 جلب آخر رسالة</h3>
            <div class="code-block">
<span class="method">GET</span> <span class="url">{{ base_url }}/api/v1/otp/latest</span>
            </div>
            
            <!-- Stats -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">📊 إحصائيات النظام</h3>
            <div class="code-block">
<span class="method">GET</span> <span class="url">{{ base_url }}/api/v1/stats</span>
            </div>
            
            <!-- Countries -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">🌍 قائمة الدول</h3>
            <div class="code-block">
<span class="method">GET</span> <span class="url">{{ base_url }}/api/v1/countries</span>
            </div>
            
            <!-- Python Example -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">🐍 مثال Python</h3>
            <div class="code-block">
<span class="key">import</span> requests

API_KEY = <span class="string">"{{ current_user.api_key or 'YOUR_API_KEY' }}"</span>
BASE_URL = <span class="string">"{{ base_url }}"</span>

headers = {
    <span class="string">"X-API-Key"</span>: API_KEY,
    <span class="string">"Content-Type"</span>: <span class="string">"application/json"</span>
}

<span class="comment"># إرسال رسالة OTP جديدة</span>
data = {
    <span class="string">"phone_number"</span>: <span class="string">"+1234567890"</span>,
    <span class="string">"message"</span>: <span class="string">"Your code is 123456"</span>,
    <span class="string">"service"</span>: <span class="string">"WhatsApp"</span>
}

response = requests.post(
    f<span class="string">"{BASE_URL}/api/v1/otp/receive"</span>,
    headers=headers,
    json=data
)

print(response.json())

<span class="comment"># جلب آخر الرسائل</span>
response = requests.get(
    f<span class="string">"{BASE_URL}/api/v1/otp/messages"</span>,
    headers=headers
)

print(response.json())
            </div>
            
            <!-- Node.js Example -->
            <h3 style="color: var(--accent-light); margin: 28px 0 14px; font-size: 18px;">🟢 مثال Node.js</h3>
            <div class="code-block">
<span class="key">const</span> axios = require(<span class="string">'axios'</span>);

<span class="key">const</span> API_KEY = <span class="string">'{{ current_user.api_key or 'YOUR_API_KEY' }}'</span>;
<span class="key">const</span> BASE_URL = <span class="string">'{{ base_url }}'</span>;

<span class="comment">// إرسال رسالة OTP</span>
axios.post(`${BASE_URL}/api/v1/otp/receive`, {
    phone_number: <span class="string">'+1234567890'</span>,
    message: <span class="string">'Your code is 123456'</span>
}, {
    headers: { <span class="string">'X-API-Key'</span>: API_KEY }
})
.then(res => console.log(res.data))
.catch(err => console.error(err));
            </div>
        </div>
    </div>
    
    <!-- Add Bot Modal -->
    <div class="modal" id="addBotModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">➕ إضافة بوت تليجرام</h3>
                <button class="close-btn" onclick="closeModal('addBotModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_telegram_bot') }}">
                <div class="form-group">
                    <label>📝 اسم البوت (للتعريف)</label>
                    <input type="text" name="name" class="form-control" placeholder="مثال: بوت الإشعارات الرئيسي" required>
                </div>
                <div class="form-group">
                    <label>🔑 Bot Token</label>
                    <input type="text" name="bot_token" class="form-control" placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz" required style="direction: ltr; text-align: left;">
                    <small style="color: var(--text-muted); margin-top: 6px; display: block;">
                        احصل عليه من <a href="https://t.me/BotFather" target="_blank" style="color: var(--accent-light);">@BotFather</a>
                    </small>
                </div>
                <div class="form-group">
                    <label>💬 Chat ID</label>
                    <input type="text" name="chat_id" class="form-control" placeholder="-1001234567890" required style="direction: ltr; text-align: left;">
                    <small style="color: var(--text-muted); margin-top: 6px; display: block;">
                        ID المحادثة أو الجروب أو القناة. احصل عليه من <a href="https://t.me/userinfobot" target="_blank" style="color: var(--accent-light);">@userinfobot</a>
                    </small>
                </div>
                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">➕ إضافة البوت</button>
            </form>
        </div>
    </div>

    <script>
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }
        
        function copyApiKey() {
            const key = document.getElementById('apiKeyValue').textContent;
            navigator.clipboard.writeText(key);
            alert('✅ تم نسخ مفتاح API!');
        }
        
        function testBot(botId) {
            fetch('/admin/telegram/test/' + botId)
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ تم إرسال رسالة تجريبية بنجاح!');
                    } else {
                        alert('❌ فشل الإرسال: ' + (data.error || 'خطأ غير معروف'));
                    }
                })
                .catch(e => alert('❌ خطأ في الاتصال: ' + e));
        }
        
        document.querySelectorAll('.modal').forEach(m => {
            m.addEventListener('click', e => { if (e.target === m) m.classList.remove('active'); });
        });
    </script>
</body>
</html>
'''

# ============================================
# MAIN APPLICATION
# ============================================

"""
TM SMS PANEL - Professional SMS OTP Management System
Version: 2.0 - Fixed Phone Number Display
"""

import os
import logging
import requests
import re
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template_string, jsonify, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import threading
import time
import secrets
import uuid

# استيراد القوالب من ملف منفصل
from templates import *

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.permanent_session_lifetime = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#============================================
# Configuration
#============================================

PANEL_URL = os.environ.get('PANEL_URL', 'http://198.135.52.238')
PANEL_USERNAME = os.environ.get('PANEL_USERNAME', 'Tarek11Mohamed')
PANEL_PASSWORD = os.environ.get('PANEL_PASSWORD', 'Tarek11Mohamed')
DATABASE = 'tm_sms_panel.db'

all_messages = []
MAX_MESSAGES = 100000

bot_stats = {
    'start_time': datetime.now(),
    'total_otps': 0,
    'last_check': 'Never',
    'is_running': False,
    'scraper_status': 'Initializing...'
}

scraper = None

#============================================
# أكواد الدول للتعرف التلقائي
#============================================

COUNTRY_CODES = {
    '1': ('United States', 'US', '🇺🇸'),
    '7': ('Russia', 'RU', '🇷🇺'),
    '20': ('Egypt', 'EG', '🇪🇬'),
    '27': ('South Africa', 'ZA', '🇿🇦'),
    '30': ('Greece', 'GR', '🇬🇷'),
    '31': ('Netherlands', 'NL', '🇳🇱'),
    '32': ('Belgium', 'BE', '🇧🇪'),
    '33': ('France', 'FR', '🇫🇷'),
    '34': ('Spain', 'ES', '🇪🇸'),
    '36': ('Hungary', 'HU', '🇭🇺'),
    '39': ('Italy', 'IT', '🇮🇹'),
    '40': ('Romania', 'RO', '🇷🇴'),
    '41': ('Switzerland', 'CH', '🇨🇭'),
    '43': ('Austria', 'AT', '🇦🇹'),
    '44': ('United Kingdom', 'GB', '🇬🇧'),
    '45': ('Denmark', 'DK', '🇩🇰'),
    '46': ('Sweden', 'SE', '🇸🇪'),
    '47': ('Norway', 'NO', '🇳🇴'),
    '48': ('Poland', 'PL', '🇵🇱'),
    '49': ('Germany', 'DE', '🇩🇪'),
    '51': ('Peru', 'PE', '🇵🇪'),
    '52': ('Mexico', 'MX', '🇲🇽'),
    '53': ('Cuba', 'CU', '🇨🇺'),
    '54': ('Argentina', 'AR', '🇦🇷'),
    '55': ('Brazil', 'BR', '🇧🇷'),
    '56': ('Chile', 'CL', '🇨🇱'),
    '57': ('Colombia', 'CO', '🇨🇴'),
    '58': ('Venezuela', 'VE', '🇻🇪'),
    '60': ('Malaysia', 'MY', '🇲🇾'),
    '61': ('Australia', 'AU', '🇦🇺'),
    '62': ('Indonesia', 'ID', '🇮🇩'),
    '63': ('Philippines', 'PH', '🇵🇭'),
    '64': ('New Zealand', 'NZ', '🇳🇿'),
    '65': ('Singapore', 'SG', '🇸🇬'),
    '66': ('Thailand', 'TH', '🇹🇭'),
    '81': ('Japan', 'JP', '🇯🇵'),
    '82': ('South Korea', 'KR', '🇰🇷'),
    '84': ('Vietnam', 'VN', '🇻🇳'),
    '86': ('China', 'CN', '🇨🇳'),
    '90': ('Turkey', 'TR', '🇹🇷'),
    '91': ('India', 'IN', '🇮🇳'),
    '92': ('Pakistan', 'PK', '🇵🇰'),
    '93': ('Afghanistan', 'AF', '🇦🇫'),
    '94': ('Sri Lanka', 'LK', '🇱🇰'),
    '95': ('Myanmar', 'MM', '🇲🇲'),
    '98': ('Iran', 'IR', '🇮🇷'),
    '212': ('Morocco', 'MA', '🇲🇦'),
    '213': ('Algeria', 'DZ', '🇩🇿'),
    '216': ('Tunisia', 'TN', '🇹🇳'),
    '218': ('Libya', 'LY', '🇱🇾'),
    '220': ('Gambia', 'GM', '🇬🇲'),
    '221': ('Senegal', 'SN', '🇸🇳'),
    '234': ('Nigeria', 'NG', '🇳🇬'),
    '249': ('Sudan', 'SD', '🇸🇩'),
    '254': ('Kenya', 'KE', '🇰🇪'),
    '255': ('Tanzania', 'TZ', '🇹🇿'),
    '256': ('Uganda', 'UG', '🇺🇬'),
    '260': ('Zambia', 'ZM', '🇿🇲'),
    '263': ('Zimbabwe', 'ZW', '🇿🇼'),
    '351': ('Portugal', 'PT', '🇵🇹'),
    '352': ('Luxembourg', 'LU', '🇱🇺'),
    '353': ('Ireland', 'IE', '🇮🇪'),
    '354': ('Iceland', 'IS', '🇮🇸'),
    '355': ('Albania', 'AL', '🇦🇱'),
    '358': ('Finland', 'FI', '🇫🇮'),
    '359': ('Bulgaria', 'BG', '🇧🇬'),
    '370': ('Lithuania', 'LT', '🇱🇹'),
    '371': ('Latvia', 'LV', '🇱🇻'),
    '372': ('Estonia', 'EE', '🇪🇪'),
    '380': ('Ukraine', 'UA', '🇺🇦'),
    '381': ('Serbia', 'RS', '🇷🇸'),
    '385': ('Croatia', 'HR', '🇭🇷'),
    '386': ('Slovenia', 'SI', '🇸🇮'),
    '420': ('Czech Republic', 'CZ', '🇨🇿'),
    '421': ('Slovakia', 'SK', '🇸🇰'),
    '880': ('Bangladesh', 'BD', '🇧🇩'),
    '886': ('Taiwan', 'TW', '🇹🇼'),
    '960': ('Maldives', 'MV', '🇲🇻'),
    '961': ('Lebanon', 'LB', '🇱🇧'),
    '962': ('Jordan', 'JO', '🇯🇴'),
    '963': ('Syria', 'SY', '🇸🇾'),
    '964': ('Iraq', 'IQ', '🇮🇶'),
    '965': ('Kuwait', 'KW', '🇰🇼'),
    '966': ('Saudi Arabia', 'SA', '🇸🇦'),
    '967': ('Yemen', 'YE', '🇾🇪'),
    '968': ('Oman', 'OM', '🇴🇲'),
    '970': ('Palestine', 'PS', '🇵🇸'),
    '971': ('UAE', 'AE', '🇦🇪'),
    '972': ('Israel', 'IL', '🇮🇱'),
    '973': ('Bahrain', 'BH', '🇧🇭'),
    '974': ('Qatar', 'QA', '🇶🇦'),
    '975': ('Bhutan', 'BT', '🇧🇹'),
    '976': ('Mongolia', 'MN', '🇲🇳'),
    '977': ('Nepal', 'NP', '🇳🇵'),
    '992': ('Tajikistan', 'TJ', '🇹🇯'),
    '993': ('Turkmenistan', 'TM', '🇹🇲'),
    '994': ('Azerbaijan', 'AZ', '🇦🇿'),
    '995': ('Georgia', 'GE', '🇬🇪'),
    '996': ('Kyrgyzstan', 'KG', '🇰🇬'),
    '998': ('Uzbekistan', 'UZ', '🇺🇿'),
}

#============================================
# Database Functions
#============================================

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_database():
    """إنشاء جداول قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            is_active INTEGER DEFAULT 1,
            api_key TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            created_by INTEGER,
            notes TEXT
        )
    ''')
    
    # جدول الدول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            flag TEXT DEFAULT '🌍',
            phone_code TEXT,
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    # جدول الأرقام
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            status TEXT DEFAULT 'available',
            used_by INTEGER,
            used_at TIMESTAMP,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (country_id) REFERENCES countries (id),
            UNIQUE(country_id, phone_number)
        )
    ''')
    
    # جدول سجل النشاطات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول رسائل OTP
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            phone_number TEXT NOT NULL,
            country_name TEXT,
            country_code TEXT,
            country_flag TEXT DEFAULT '🌍',
            service TEXT DEFAULT 'SMS',
            otp_code TEXT,
            raw_message TEXT,
            sender TEXT,
            received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read INTEGER DEFAULT 0,
            forwarded_telegram INTEGER DEFAULT 0
        )
    ''')
    
    # جدول إعدادات Telegram
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telegram_bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bot_token TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            forward_otp INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    # جدول الإعدادات العامة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إنشاء حساب المدير الافتراضي
    cursor.execute('SELECT * FROM users WHERE role = "admin"')
    if not cursor.fetchone():
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Tarek11Mohamed@@@010')
        password_hash = generate_password_hash(admin_password)
        api_key = f"tm_{secrets.token_hex(32)}"
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role, is_active, api_key, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', password_hash, 'admin@tmsms.local', 'admin', 1, api_key, 'حساب المدير الرئيسي'))
        
        print("=" * 60)
        print("🔐 تم إنشاء حساب المدير!")
        print(f"   👤 اسم المستخدم: admin")
        print(f"   🔑 كلمة المرور: {admin_password}")
        print(f"   🔗 API Key: {api_key}")
        print("   ⚠️  يرجى تغيير كلمة المرور فوراً!")
        print("=" * 60)
    
    conn.commit()
    conn.close()

def log_activity(user_id, action, details=None):
    """تسجيل النشاط"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        ip = request.remote_addr if request else 'system'
        cursor.execute('''
            INSERT INTO activity_logs (user_id, action, details, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (user_id, action, details, ip))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error logging activity: {e}")

#============================================
# Helper Functions
#============================================

def get_country_from_phone(phone_number):
    """استخراج معلومات الدولة من رقم الهاتف"""
    if not phone_number:
        return {'name': 'Unknown', 'code': 'XX', 'flag': '🌍'}
    
    # تنظيف الرقم
    clean = re.sub(r'[^\d]', '', str(phone_number))
    if clean.startswith('00'):
        clean = clean[2:]
    
    # البحث في قاعدة البيانات أولاً
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.name, c.code, c.flag 
            FROM phone_numbers p 
            JOIN countries c ON p.country_id = c.id 
            WHERE p.phone_number LIKE ?
        ''', (f'%{phone_number[-10:]}%',))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {'name': result['name'], 'code': result['code'], 'flag': result['flag']}
    except:
        pass
    
    # البحث في أكواد الدول
    for length in [4, 3, 2, 1]:
        code = clean[:length]
        if code in COUNTRY_CODES:
            name, iso, flag = COUNTRY_CODES[code]
            return {'name': name, 'code': iso, 'flag': flag}
    
    return {'name': 'Unknown', 'code': 'XX', 'flag': '🌍'}

def extract_otp(message):
    """استخراج كود OTP من الرسالة"""
    if not message:
        return 'N/A'
    
    patterns = [
        r'(?:code|código|kod|كود|رمز|otp|pin|verification|verify)[:\s]*(\d{4,8})',
        r'(\d{6})',
        r'(\d{4,8})',
        r'(\d{3}[-.\s]?\d{3})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, str(message), re.IGNORECASE)
        if match:
            code = match.group(1).replace(' ', '').replace('-', '').replace('.', '')
            return code
    
    return 'N/A'

def detect_service(message, sender=''):
    """تحديد الخدمة من الرسالة"""
    text = f"{message} {sender}".lower()
    
    services = {
        'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'signal': 'Signal',
        'facebook': 'Facebook', 'fb': 'Facebook', 'meta': 'Meta',
        'instagram': 'Instagram', 'insta': 'Instagram',
        'twitter': 'Twitter', 'x.com': 'Twitter',
        'google': 'Google', 'gmail': 'Google',
        'microsoft': 'Microsoft', 'outlook': 'Microsoft', 'hotmail': 'Microsoft',
        'apple': 'Apple', 'icloud': 'Apple',
        'amazon': 'Amazon', 'aws': 'Amazon',
        'paypal': 'PayPal', 'uber': 'Uber', 'lyft': 'Lyft',
        'tiktok': 'TikTok', 'snapchat': 'Snapchat', 'snap': 'Snapchat',
        'linkedin': 'LinkedIn', 'netflix': 'Netflix', 'spotify': 'Spotify',
        'discord': 'Discord', 'twitch': 'Twitch', 'reddit': 'Reddit',
        'binance': 'Binance', 'coinbase': 'Coinbase', 'crypto': 'Crypto',
        'bank': 'Bank', 'visa': 'Visa', 'mastercard': 'Mastercard',
    }
    
    for key, name in services.items():
        if key in text:
            return name
    
    return 'SMS Service'

def parse_phone_file(content):
    """تحليل ملف الأرقام"""
    numbers = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            phone = re.sub(r'[^\d+]', '', line)
            if len(phone) >= 8:
                numbers.append(phone)
    return list(set(numbers))

#============================================
# Telegram Integration
#============================================

def send_to_telegram(otp_data):
    """إرسال رسالة OTP لجميع بوتات تليجرام المفعلة"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM telegram_bots WHERE is_active = 1 AND forward_otp = 1')
        bots = cursor.fetchall()
        conn.close()
        
        if not bots:
            return False
        
        # تنسيق الرسالة
        message = f"""
🆕 *رسالة OTP جديدة*

━━━━━━━━━━━━━━━━━━
{otp_data.get('country_flag', '🌍')} *الدولة:* {otp_data.get('country_name', 'غير معروف')}
📞 *الرقم:* `{otp_data.get('phone_number', 'N/A')}`
🏷️ *الخدمة:* {otp_data.get('service', 'SMS')}
━━━━━━━━━━━━━━━━━━

🔐 *كود OTP:*
{otp_data.get('otp_code', 'N/A')}

📝 *الرسالة:*
_{otp_data.get('raw_message', '')[:300]}_

⏰ {otp_data.get('received_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
━━━━━━━━━━━━━━━━━━
📱 TM SMS PANEL
        """
        
        success = False
        for bot in bots:
            try:
                url = f"https://api.telegram.org/bot{bot['bot_token']}/sendMessage"
                response = requests.post(url, data={
                    'chat_id': bot['chat_id'],
                    'text': message,
                    'parse_mode': 'Markdown'
                }, timeout=10)
                
                if response.status_code == 200:
                    success = True
            except Exception as e:
                logger.error(f"Telegram send error: {e}")
        
        return success
        
    except Exception as e:
        logger.error(f"send_to_telegram error: {e}")
        return False

def save_otp_message(otp_data):
    """حفظ رسالة OTP في قاعدة البيانات وإرسالها لتليجرام"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        message_id = otp_data.get('id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT OR IGNORE INTO otp_messages 
            (message_id, phone_number, country_name, country_code, country_flag,
             service, otp_code, raw_message, sender, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            message_id,
            otp_data.get('phone_number', ''),
            otp_data.get('country_name', ''),
            otp_data.get('country_code', ''),
            otp_data.get('country_flag', '🌍'),
            otp_data.get('service', 'SMS'),
            otp_data.get('otp_code', 'N/A'),
            otp_data.get('raw_message', ''),
            otp_data.get('sender', ''),
            otp_data.get('received_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ))
        
        is_new = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        # إرسال لتليجرام إذا كانت رسالة جديدة
        if is_new:
            send_to_telegram(otp_data)
        
        return is_new
        
    except Exception as e:
        logger.error(f"save_otp_message error: {e}")
        return False

#============================================
# Authentication Decorators
#============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login'))
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT is_active FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not user[0]:
            session.clear()
            flash('تم إيقاف حسابك', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login'))
        
        if session.get('role') != 'admin':
            flash('ليس لديك صلاحية', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def api_key_required(f):
    """التحقق من API Key - للمدير فقط"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key required', 'code': 401}), 401
        
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE api_key = ? AND is_active = 1 AND role = 'admin'
        ''', (api_key,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'error': 'Invalid API key', 'code': 403}), 403
        
        g.api_user = dict(user)
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """الحصول على المستخدم الحالي"""
    if 'user_id' not in session:
        return None
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

#============================================
# Panel API Class - معدل لإصلاح مشكلة الرقم
#============================================

class PanelAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/') if base_url else ''
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
        self.logged_in = False
        self.session.headers.update({
            'User-Agent': 'TM-SMS-Panel/2.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    
    def login(self):
        try:
            if not self.base_url or not self.username:
                bot_stats['scraper_status'] = '⚠️ يحتاج إعداد'
                return False
            
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
                    bot_stats['scraper_status'] = '✅ متصل'
                    return True
            
            bot_stats['scraper_status'] = '❌ فشل الاتصال'
            return False
            
        except Exception as e:
            bot_stats['scraper_status'] = f'❌ خطأ'
            logger.error(f"Panel login error: {e}")
            return False
    
    def fetch_messages(self):
        if not self.logged_in and not self.login():
            return []
        
        try:
            response = self.session.get(f"{self.base_url}/api/sms?limit=100", timeout=15)
            
            if response.status_code == 401:
                self.logged_in = False
                if not self.login():
                    return []
                response = self.session.get(f"{self.base_url}/api/sms?limit=100", timeout=15)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            # Debug: طباعة أول رسالة لمعرفة الحقول
            if data:
                sample = data[0] if isinstance(data, list) else None
                if sample:
                    logger.info(f"Sample message keys: {list(sample.keys())}")
                    logger.info(f"Sample message: {sample}")
            
            messages = data if isinstance(data, list) else data.get('sms', data.get('messages', data.get('data', [])))
            
            formatted_messages = []
            for m in messages:
                formatted = self._format_message(m)
                if formatted:
                    formatted_messages.append(formatted)
            
            return formatted_messages
            
        except Exception as e:
            logger.error(f"Fetch messages error: {e}")
            return []
    
    def _format_message(self, msg):
        """تنسيق الرسالة - مع دعم جميع أسماء الحقول الممكنة"""
        try:
            # ===== استخراج الرقم - تجربة جميع الأسماء الممكنة =====
            phone = None
            phone_keys = ['Number', 'number', 'Phone', 'phone', 'From', 'from', 
                         'sender_number', 'mobile', 'Mobile', 'msisdn', 'MSISDN',
                         'phoneNumber', 'phone_number', 'recipient', 'to', 'To']
            
            for key in phone_keys:
                if msg.get(key):
                    phone = str(msg.get(key))
                    break
            
            if not phone:
                phone = 'Unknown'
            
            # ===== استخراج محتوى الرسالة =====
            content = None
            content_keys = ['content', 'Content', 'message', 'Message', 'text', 'Text',
                           'body', 'Body', 'sms', 'SMS', 'msg', 'Msg']
            
            for key in content_keys:
                if msg.get(key):
                    content = str(msg.get(key))
                    break
            
            if not content:
                content = ''
            
            # ===== استخراج المرسل =====
            sender = None
            sender_keys = ['sender', 'Sender', 'from_name', 'fromName', 'service', 'Service']
            
            for key in sender_keys:
                if msg.get(key):
                    sender = str(msg.get(key))
                    break
            
            if not sender:
                sender = ''
            
            # ===== استخراج الدولة =====
            country_raw = None
            country_keys = ['country', 'Country', 'country_name', 'countryName', 'region', 'Region']
            
            for key in country_keys:
                if msg.get(key):
                    country_raw = str(msg.get(key))
                    break
            
            # الحصول على معلومات الدولة من الرقم
            country_info = get_country_from_phone(phone)
            
            # إذا كانت الدولة موجودة في الرسالة، استخدمها
            if country_raw:
                country_info['name'] = country_raw
            
            # ===== استخراج التاريخ =====
            timestamp = None
            time_keys = ['created_at', 'CreatedAt', 'timestamp', 'Timestamp', 'date', 'Date',
                        'time', 'Time', 'createdAt', 'receivedAt', 'received_at']
            
            for key in time_keys:
                if msg.get(key):
                    timestamp = str(msg.get(key))
                    break
            
            if not timestamp:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # تنسيق التاريخ
            if timestamp and isinstance(timestamp, str):
                try:
                    if 'T' in timestamp:
                        dt = datetime.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')
                        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            # ===== استخراج ID =====
            msg_id = msg.get('id') or msg.get('Id') or msg.get('ID') or msg.get('_id') or str(hash(str(msg)))
            
            # ===== بناء البيانات النهائية =====
            otp_data = {
                'id': hashlib.sha256(str(msg_id).encode()).hexdigest()[:16],
                'phone_number': phone,
                'country_name': country_info['name'],
                'country_code': country_info['code'],
                'country_flag': country_info['flag'],
                'service': detect_service(content, sender),
                'otp_code': extract_otp(content),
                'raw_message': content[:500] if content else '',
                'sender': sender,
                'received_at': timestamp
            }
            
            # Debug log
            logger.info(f"Formatted OTP - Phone: {phone}, Country: {country_info['name']}, OTP: {otp_data['otp_code']}")
            
            return otp_data
            
        except Exception as e:
            logger.error(f"Format message error: {e}")
            logger.error(f"Raw message: {msg}")
            return None

def create_scraper():
    if not PANEL_URL or not PANEL_USERNAME or not PANEL_PASSWORD:
        bot_stats['scraper_status'] = '⚠️ يحتاج إعداد'
        return None
    
    api = PanelAPI(PANEL_URL, PANEL_USERNAME, PANEL_PASSWORD)
    api.login()
    return api

#============================================
# Background Monitor
#============================================

class OTPFilter:
    def __init__(self):
        self.cache = set()
    
    def is_new(self, msg_id):
        if msg_id in self.cache:
            return False
        self.cache.add(msg_id)
        if len(self.cache) > 1000:
            self.cache = set(list(self.cache)[-500:])
        return True
    
    def clear(self):
        self.cache.clear()

otp_filter = OTPFilter()

def check_and_update():
    global scraper, all_messages
    
    try:
        if not scraper:
            scraper = create_scraper()
            if not scraper:
                return
        
        messages = scraper.fetch_messages()
        bot_stats['last_check'] = datetime.now().strftime('%H:%M:%S')
        
        for msg in messages:
            if otp_filter.is_new(msg['id']):
                all_messages.insert(0, msg)
                bot_stats['total_otps'] += 1
                save_otp_message(msg)
        
        all_messages = all_messages[:MAX_MESSAGES]
        
    except Exception as e:
        logger.error(f"Check and update error: {e}")

def background_monitor():
    bot_stats['is_running'] = True
    check_and_update()
    
    while bot_stats['is_running']:
        try:
            time.sleep(10)
            check_and_update()
        except Exception as e:
            logger.error(f"Background monitor error: {e}")
            time.sleep(30)

#============================================
# Flask Routes - Authentication
#============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            if not user['is_active']:
                flash('تم إيقاف حسابك', 'danger')
                return render_template_string(LOGIN_TEMPLATE)
            
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # تحديث آخر دخول
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?',
                          (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id']))
            conn.commit()
            conn.close()
            
            log_activity(user['id'], 'login', 'تسجيل دخول ناجح')
            flash('مرحباً بك!', 'success')
            return redirect(url_for('dashboard'))
        else:
            log_activity(None, 'failed_login', f'محاولة فاشلة: {username}')
            flash('اسم المستخدم أو كلمة المرور خاطئة', 'danger')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], 'logout', 'تسجيل خروج')
    session.clear()
    return redirect(url_for('login'))

#============================================
# Flask Routes - Dashboard & Pages
#============================================

@app.route('/')
@login_required
def dashboard():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # جلب الدول مع الإحصائيات
    cursor.execute('''
        SELECT c.*, 
               COUNT(p.id) as total,
               SUM(CASE WHEN p.status = 'available' THEN 1 ELSE 0 END) as available
        FROM countries c
        LEFT JOIN phone_numbers p ON c.id = p.country_id
        WHERE c.is_active = 1
        GROUP BY c.id
        ORDER BY c.sort_order, c.name
    ''')
    countries = [dict(row) for row in cursor.fetchall()]
    
    # إحصائيات
    cursor.execute('SELECT COUNT(*) FROM countries WHERE is_active = 1')
    total_countries = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM phone_numbers')
    total_numbers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE status = 'available'")
    available_numbers = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM otp_messages')
    total_otp = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template_string(DASHBOARD_TEMPLATE,
                                  current_user=current_user,
                                  countries=countries,
                                  total_countries=total_countries,
                                  total_numbers=total_numbers,
                                  available_numbers=available_numbers,
                                  total_otp=total_otp,
                                  stats=bot_stats)

@app.route('/numbers')
@login_required
def numbers_page():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, 
               COUNT(p.id) as total,
               SUM(CASE WHEN p.status = 'available' THEN 1 ELSE 0 END) as available,
               SUM(CASE WHEN p.status = 'used' THEN 1 ELSE 0 END) as used
        FROM countries c
        LEFT JOIN phone_numbers p ON c.id = p.country_id
        WHERE c.is_active = 1
        GROUP BY c.id
        ORDER BY available DESC, c.name
    ''')
    countries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template_string(NUMBERS_PAGE_TEMPLATE,
                                  current_user=current_user,
                                  countries=countries)

@app.route('/numbers/<int:country_id>')
@login_required
def country_numbers(country_id):
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM countries WHERE id = ?', (country_id,))
    country = cursor.fetchone()
    
    if not country:
        flash('الدولة غير موجودة', 'danger')
        return redirect(url_for('numbers_page'))
    
    cursor.execute('''
        SELECT * FROM phone_numbers 
        WHERE country_id = ? 
        ORDER BY status ASC, created_at DESC
    ''', (country_id,))
    numbers = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE country_id = ? AND status = 'available'", (country_id,))
    available_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE country_id = ? AND status = 'used'", (country_id,))
    used_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template_string(COUNTRY_NUMBERS_TEMPLATE,
                                  current_user=current_user,
                                  country=dict(country),
                                  numbers=numbers,
                                  available_count=available_count,
                                  used_count=used_count)

@app.route('/otp')
@login_required
def otp_messages():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM otp_messages ORDER BY received_at DESC LIMIT 100')
    db_messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # دمج الرسائل من الذاكرة وقاعدة البيانات
    messages = db_messages if db_messages else all_messages
    
    return render_template_string(OTP_MESSAGES_TEMPLATE,
                                  current_user=current_user,
                                  messages=messages,
                                  stats=bot_stats)

@app.route('/otp/clear', methods=['POST'])
@admin_required
def clear_otp():
    global all_messages
    all_messages = []
    otp_filter.clear()
    bot_stats['total_otps'] = 0
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM otp_messages')
    conn.commit()
    conn.close()
    
    log_activity(session['user_id'], 'clear_otp', 'مسح جميع رسائل OTP')
    flash('تم مسح جميع الرسائل', 'success')
    return redirect(url_for('otp_messages'))

#============================================
# Flask Routes - Admin Panel
#============================================

@app.route('/admin')
@admin_required
def admin_panel():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # إحصائيات
    stats = {}
    cursor.execute('SELECT COUNT(*) FROM users')
    stats['users'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM countries')
    stats['countries'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM phone_numbers')
    stats['numbers'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE status = 'available'")
    stats['available'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM otp_messages')
    stats['messages'] = cursor.fetchone()[0]
    
    # آخر النشاطات
    cursor.execute('''
        SELECT a.*, u.username 
        FROM activity_logs a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.timestamp DESC LIMIT 50
    ''')
    activities = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template_string(ADMIN_TEMPLATE,
                                  current_user=current_user,
                                  stats=stats,
                                  activities=activities)

#============================================
# Flask Routes - Countries Management
#============================================

@app.route('/admin/countries')
@admin_required
def manage_countries():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, 
               COUNT(p.id) as total,
               SUM(CASE WHEN p.status = 'available' THEN 1 ELSE 0 END) as available
        FROM countries c
        LEFT JOIN phone_numbers p ON c.id = p.country_id
        GROUP BY c.id
        ORDER BY c.name
    ''')
    countries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template_string(MANAGE_COUNTRIES_TEMPLATE,
                                  current_user=current_user,
                                  countries=countries)

@app.route('/admin/countries/add', methods=['POST'])
@admin_required
def add_country():
    name = request.form.get('name', '').strip()
    code = request.form.get('code', '').strip().upper()
    flag = request.form.get('flag', '🌍').strip()
    phone_code = request.form.get('phone_code', '').strip()
    numbers_file = request.files.get('numbers_file')
    
    if not name or not code:
        flash('الاسم والكود مطلوبان', 'danger')
        return redirect(url_for('manage_countries'))
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO countries (name, code, flag, phone_code, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, code, flag, phone_code, session['user_id']))
        country_id = cursor.lastrowid
        
        # إضافة الأرقام من الملف
        added_count = 0
        if numbers_file and numbers_file.filename:
            content = numbers_file.read().decode('utf-8')
            numbers = parse_phone_file(content)
            for phone in numbers:
                try:
                    cursor.execute('INSERT INTO phone_numbers (country_id, phone_number) VALUES (?, ?)',
                                  (country_id, phone))
                    added_count += 1
                except:
                    pass
        
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'add_country', f'إضافة: {name} ({added_count} رقم)')
        flash(f'تم إضافة {name} مع {added_count} رقم', 'success')
        
    except sqlite3.IntegrityError:
        flash('كود الدولة موجود مسبقاً', 'danger')
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('manage_countries'))

@app.route('/admin/countries/edit', methods=['POST'])
@admin_required
def edit_country():
    country_id = request.form.get('country_id')
    name = request.form.get('name', '').strip()
    code = request.form.get('code', '').strip().upper()
    flag = request.form.get('flag', '🌍').strip()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE countries SET name = ?, code = ?, flag = ? WHERE id = ?',
                      (name, code, flag, country_id))
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'edit_country', f'تعديل: {name}')
        flash('تم التحديث', 'success')
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('manage_countries'))

@app.route('/admin/countries/toggle/<int:country_id>', methods=['POST'])
@admin_required
def toggle_country(country_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT is_active, name FROM countries WHERE id = ?', (country_id,))
    country = cursor.fetchone()
    
    if country:
        new_status = 0 if country[0] else 1
        cursor.execute('UPDATE countries SET is_active = ? WHERE id = ?', (new_status, country_id))
        conn.commit()
        log_activity(session['user_id'], 'toggle_country', f"{'تفعيل' if new_status else 'إيقاف'}: {country[1]}")
    
    conn.close()
    return redirect(url_for('manage_countries'))

@app.route('/admin/countries/delete/<int:country_id>', methods=['POST'])
@admin_required
def delete_country(country_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT name FROM countries WHERE id = ?', (country_id,))
    country = cursor.fetchone()
    
    if country:
        cursor.execute('DELETE FROM phone_numbers WHERE country_id = ?', (country_id,))
        cursor.execute('DELETE FROM countries WHERE id = ?', (country_id,))
        conn.commit()
        log_activity(session['user_id'], 'delete_country', f'حذف: {country[0]}')
        flash('تم الحذف', 'success')
    
    conn.close()
    return redirect(url_for('manage_countries'))

#============================================
# Flask Routes - Numbers Management
#============================================

@app.route('/admin/numbers/add/<int:country_id>', methods=['POST'])
@admin_required
def add_numbers(country_id):
    numbers_file = request.files.get('file')
    numbers_text = request.form.get('numbers_text', '')
    
    numbers = []
    
    if numbers_file and numbers_file.filename:
        content = numbers_file.read().decode('utf-8')
        numbers.extend(parse_phone_file(content))
    
    if numbers_text:
        numbers.extend(parse_phone_file(numbers_text))
    
    if not numbers:
        flash('لم يتم العثور على أرقام', 'warning')
        return redirect(url_for('country_numbers', country_id=country_id))
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        added = 0
        for phone in numbers:
            try:
                cursor.execute('INSERT INTO phone_numbers (country_id, phone_number) VALUES (?, ?)',
                              (country_id, phone))
                added += 1
            except:
                pass
        
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'add_numbers', f'إضافة {added} رقم')
        flash(f'تم إضافة {added} رقم', 'success')
        
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('country_numbers', country_id=country_id))

@app.route('/admin/numbers/status/<int:number_id>/<status>', methods=['POST'])
@admin_required
def change_number_status(number_id, status):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if status == 'used':
        cursor.execute('''
            UPDATE phone_numbers 
            SET status = 'used', used_by = ?, used_at = ? 
            WHERE id = ?
        ''', (session['user_id'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), number_id))
    else:
        cursor.execute('''
            UPDATE phone_numbers 
            SET status = 'available', used_by = NULL, used_at = NULL 
            WHERE id = ?
        ''', (number_id,))
    
    cursor.execute('SELECT country_id FROM phone_numbers WHERE id = ?', (number_id,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    
    if result:
        return redirect(url_for('country_numbers', country_id=result[0]))
    return redirect(url_for('numbers_page'))

@app.route('/admin/numbers/delete/<int:number_id>', methods=['POST'])
@admin_required
def delete_number(number_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT country_id FROM phone_numbers WHERE id = ?', (number_id,))
    result = cursor.fetchone()
    country_id = result[0] if result else None
    
    cursor.execute('DELETE FROM phone_numbers WHERE id = ?', (number_id,))
    conn.commit()
    conn.close()
    
    if country_id:
        return redirect(url_for('country_numbers', country_id=country_id))
    return redirect(url_for('numbers_page'))

#============================================
# Flask Routes - Users Management
#============================================

@app.route('/admin/users')
@admin_required
def manage_users():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template_string(MANAGE_USERS_TEMPLATE,
                                  current_user=current_user,
                                  users=users)

@app.route('/admin/users/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm = request.form.get('confirm_password', '')
    role = request.form.get('role', 'user')
    
    if not username or not password:
        flash('اسم المستخدم وكلمة المرور مطلوبان', 'danger')
        return redirect(url_for('manage_users'))
    
    if password != confirm:
        flash('كلمتا المرور غير متطابقتين', 'danger')
        return redirect(url_for('manage_users'))
    
    if len(password) < 6:
        flash('كلمة المرور قصيرة جداً (6 أحرف على الأقل)', 'danger')
        return redirect(url_for('manage_users'))
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('اسم المستخدم موجود', 'danger')
            conn.close()
            return redirect(url_for('manage_users'))
        
        password_hash = generate_password_hash(password)
        api_key = f"tm_{secrets.token_hex(32)}" if role == 'admin' else None
        
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role, api_key, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, email, role, api_key, session['user_id']))
        
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'add_user', f'إنشاء: {username}')
        flash(f'تم إنشاء {username}', 'success')
        
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('manage_users'))

@app.route('/admin/users/edit', methods=['POST'])
@admin_required
def edit_user():
    user_id = request.form.get('user_id')
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    role = request.form.get('role', 'user')
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        if password:
            password_hash = generate_password_hash(password)
            cursor.execute('''
                UPDATE users SET username = ?, email = ?, password_hash = ?, role = ?
                WHERE id = ?
            ''', (username, email, password_hash, role, user_id))
        else:
            cursor.execute('''
                UPDATE users SET username = ?, email = ?, role = ?
                WHERE id = ?
            ''', (username, email, role, user_id))
        
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'edit_user', f'تعديل: {username}')
        flash('تم التحديث', 'success')
        
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('manage_users'))

@app.route('/admin/users/toggle/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user(user_id):
    if user_id == session['user_id']:
        flash('لا يمكنك إيقاف حسابك', 'danger')
        return redirect(url_for('manage_users'))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT is_active, username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user:
        new_status = 0 if user[0] else 1
        cursor.execute('UPDATE users SET is_active = ? WHERE id = ?', (new_status, user_id))
        conn.commit()
        log_activity(session['user_id'], 'toggle_user', f"{'تفعيل' if new_status else 'إيقاف'}: {user[1]}")
    
    conn.close()
    return redirect(url_for('manage_users'))

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session['user_id']:
        flash('لا يمكنك حذف حسابك', 'danger')
        return redirect(url_for('manage_users'))
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        log_activity(session['user_id'], 'delete_user', f'حذف: {user[0]}')
        flash('تم الحذف', 'success')
    
    conn.close()
    return redirect(url_for('manage_users'))

#============================================
# Flask Routes - API Settings
#============================================

@app.route('/admin/api')
@admin_required
def api_settings():
    current_user = get_current_user()
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM telegram_bots ORDER BY created_at DESC')
    telegram_bots = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template_string(API_SETTINGS_TEMPLATE,
                                  current_user=current_user,
                                  telegram_bots=telegram_bots,
                                  base_url=request.host_url.rstrip('/'))

@app.route('/admin/api/regenerate', methods=['POST'])
@admin_required
def regenerate_api_key():
    new_key = f"tm_{secrets.token_hex(32)}"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET api_key = ? WHERE id = ?', (new_key, session['user_id']))
    conn.commit()
    conn.close()
    
    log_activity(session['user_id'], 'regenerate_api', 'إعادة توليد API Key')
    flash('تم إعادة توليد المفتاح', 'success')
    return redirect(url_for('api_settings'))

@app.route('/admin/telegram/add', methods=['POST'])
@admin_required
def add_telegram_bot():
    name = request.form.get('name', '').strip()
    bot_token = request.form.get('bot_token', '').strip()
    chat_id = request.form.get('chat_id', '').strip()
    
    if not name or not bot_token or not chat_id:
        flash('جميع الحقول مطلوبة', 'danger')
        return redirect(url_for('api_settings'))
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO telegram_bots (name, bot_token, chat_id, created_by)
            VALUES (?, ?, ?, ?)
        ''', (name, bot_token, chat_id, session['user_id']))
        conn.commit()
        conn.close()
        
        log_activity(session['user_id'], 'add_telegram', f'إضافة بوت: {name}')
        flash('تم إضافة البوت', 'success')
    except Exception as e:
        flash(f'خطأ: {str(e)}', 'danger')
    
    return redirect(url_for('api_settings'))

@app.route('/admin/telegram/toggle/<int:bot_id>', methods=['POST'])
@admin_required
def toggle_telegram_bot(bot_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT is_active FROM telegram_bots WHERE id = ?', (bot_id,))
    bot = cursor.fetchone()
    
    if bot:
        cursor.execute('UPDATE telegram_bots SET is_active = ? WHERE id = ?',
                      (0 if bot[0] else 1, bot_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('api_settings'))

@app.route('/admin/telegram/delete/<int:bot_id>', methods=['POST'])
@admin_required
def delete_telegram_bot(bot_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM telegram_bots WHERE id = ?', (bot_id,))
    conn.commit()
    conn.close()
    
    flash('تم حذف البوت', 'success')
    return redirect(url_for('api_settings'))

@app.route('/admin/telegram/test/<int:bot_id>')
@admin_required
def test_telegram_bot(bot_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM telegram_bots WHERE id = ?', (bot_id,))
    bot = cursor.fetchone()
    conn.close()
    
    if not bot:
        return jsonify({'success': False, 'error': 'Bot not found'})
    
    try:
        url = f"https://api.telegram.org/bot{bot['bot_token']}/sendMessage"
        message = f"""
🧪 *رسالة تجريبية*

✅ تم ربط البوت بنجاح!
📱 *TM SMS PANEL*
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        response = requests.post(url, data={
            'chat_id': bot['chat_id'],
            'text': message,
            'parse_mode': 'Markdown'
        }, timeout=10)
        
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'تم الإرسال بنجاح'})
        else:
            return jsonify({'success': False, 'error': response.text})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

#============================================
# API Endpoints (للمدير فقط)
#============================================

@app.route('/api/v1/otp/receive', methods=['POST'])
@api_key_required
def api_receive_otp():
    """استقبال رسالة OTP عبر API"""
    try:
        data = request.get_json() or {}
        
        # استخراج الرقم من مختلف الأسماء الممكنة
        phone = (data.get('phone_number') or data.get('phone') or 
                data.get('Number') or data.get('number') or 
                data.get('mobile') or data.get('from') or '')
        
        # استخراج الرسالة
        message = (data.get('message') or data.get('content') or 
                  data.get('text') or data.get('body') or '')
        
        if not phone:
            return jsonify({'success': False, 'error': 'phone_number is required'}), 400
        
        # الحصول على معلومات الدولة
        country_info = get_country_from_phone(phone)
        
        otp_data = {
            'id': data.get('id', str(uuid.uuid4())),
            'phone_number': phone,
            'country_name': data.get('country') or data.get('country_name') or country_info['name'],
            'country_code': data.get('country_code') or country_info['code'],
            'country_flag': data.get('country_flag') or data.get('flag') or country_info['flag'],
            'service': data.get('service') or detect_service(message, data.get('sender', '')),
            'otp_code': data.get('otp_code') or data.get('otp') or extract_otp(message),
            'raw_message': message,
            'sender': data.get('sender', ''),
            'received_at': data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
        
        # حفظ الرسالة
        is_new = save_otp_message(otp_data)
        
        if is_new:
            all_messages.insert(0, otp_data)
            if len(all_messages) > MAX_MESSAGES:
                all_messages.pop()
            bot_stats['total_otps'] += 1
        
        return jsonify({
            'success': True,
            'is_new': is_new,
            'data': {
                'id': otp_data['id'],
                'otp_code': otp_data['otp_code'],
                'phone_number': otp_data['phone_number'],
                'country': otp_data['country_name'],
                'service': otp_data['service']
            }
        })
        
    except Exception as e:
        logger.error(f"API receive error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/otp/messages', methods=['GET'])
@api_key_required
def api_get_messages():
    """جلب رسائل OTP"""
    try:
        limit = min(int(request.args.get('limit', 50)), 200)
        offset = int(request.args.get('offset', 0))
        
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM otp_messages 
            ORDER BY received_at DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        messages = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT COUNT(*) FROM otp_messages')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total': total,
            'count': len(messages),
            'messages': messages
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/otp/latest', methods=['GET'])
@api_key_required
def api_get_latest():
    """جلب آخر رسالة OTP"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM otp_messages ORDER BY received_at DESC LIMIT 1')
        message = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': dict(message) if message else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/stats', methods=['GET'])
@api_key_required
def api_stats():
    """إحصائيات النظام"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute('SELECT COUNT(*) FROM otp_messages')
        stats['total_otp'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM otp_messages WHERE DATE(received_at) = DATE("now")')
        stats['today_otp'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM countries WHERE is_active = 1')
        stats['countries'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM phone_numbers')
        stats['total_numbers'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM phone_numbers WHERE status = 'available'")
        stats['available_numbers'] = cursor.fetchone()[0]
        
        conn.close()
        
        stats['system_status'] = 'online' if bot_stats['is_running'] else 'offline'
        stats['last_check'] = bot_stats['last_check']
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/countries', methods=['GET'])
@api_key_required
def api_countries():
    """جلب قائمة الدول"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.name, c.code, c.flag,
                   COUNT(p.id) as total,
                   SUM(CASE WHEN p.status = 'available' THEN 1 ELSE 0 END) as available
            FROM countries c
            LEFT JOIN phone_numbers p ON c.id = p.country_id
            WHERE c.is_active = 1
            GROUP BY c.id
            ORDER BY c.name
        ''')
        countries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'countries': countries})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

#============================================
# Debug Route - لفحص الرسائل الخام
#============================================

@app.route('/debug/messages')
@admin_required
def debug_messages():
    """عرض الرسائل الخام للـ Debug"""
    return jsonify({
        'memory_messages_count': len(all_messages),
        'memory_messages': all_messages[:5],
        'stats': {
            'total_otps': bot_stats['total_otps'],
            'last_check': bot_stats['last_check'],
            'is_running': bot_stats['is_running'],
            'scraper_status': bot_stats['scraper_status']
        },
        'sample_keys': list(all_messages[0].keys()) if all_messages else []
    })

#============================================
# تحديث داخلي
#============================================

@app.route('/api/refresh')
@login_required
def api_refresh():
    check_and_update()
    return jsonify({'status': 'ok', 'count': len(all_messages), 'last_check': bot_stats['last_check']})

#============================================
# Main
#============================================

def main():
    global scraper
    
    print("=" * 60)
    print("  📱 TM SMS PANEL v2.0")
    print("  Professional SMS OTP Management System")
    print("=" * 60)
    
    # إنشاء قاعدة البيانات
    init_database()
    
    # تشغيل المراقب الخلفي
    if PANEL_URL and PANEL_USERNAME and PANEL_PASSWORD:
        scraper = create_scraper()
        threading.Thread(target=background_monitor, daemon=True).start()
        print("✅ Background monitor started")
    else:
        print("⚠️  Panel credentials not set - Configure in .env file")
        bot_stats['scraper_status'] = '⚠️ يحتاج إعداد'
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Server: http://localhost:{port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    main()


# ================= SECOND SYSTEM MERGED =================

import os
import logging
import requests
import re
import hashlib
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from dotenv import load_dotenv
import threading
import time
from functools import wraps

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'otp-king-secret-key-2026'

#============================================
# Database Setup
#============================================

def init_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  telegram TEXT,
                  country TEXT,
                  role TEXT DEFAULT 'user',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Panel settings table
    c.execute('''CREATE TABLE IF NOT EXISTS panel_settings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  panel_url TEXT,
                  panel_username TEXT,
                  panel_password TEXT,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Insert default admin if not exists
    c.execute("SELECT * FROM users WHERE username=?", ('mohaymen',))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, telegram, country, role) VALUES (?, ?, ?, ?, ?)",
                  ('mohaymen', 'mohaymen', '@mohaymen', 'Egypt', 'owner'))
    
    # Insert default panel settings
    c.execute("SELECT * FROM panel_settings")
    if not c.fetchone():
        c.execute("INSERT INTO panel_settings (panel_url, panel_username, panel_password) VALUES (?, ?, ?)",
                  ('http://198.135.52.238', 'gagaywb66', 'gagaywb66'))
    
    conn.commit()
    conn.close()

init_database()

#============================================
# Login Decorator
#============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'owner':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

#============================================
# Video Intro HTML
#============================================

VIDEO_INTRO = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - Intro</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Arial', sans-serif;
        }
        
        .video-container {
            width: 100%;
            max-width: 600px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: fadeIn 1s ease;
        }
        
        video {
            width: 100%;
            display: block;
        }
        
        .skip-btn {
            position: absolute;
            bottom: 30px;
            right: 30px;
            background: rgba(255,255,255,0.1);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 12px 30px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        
        .skip-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1.05);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .loading-text {
            color: white;
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <video id="introVideo" autoplay playsinline>
            <source src="https://drive.google.com/uc?export=download&id=1OGS3-mnoM7Q6P-MTl3GDrtU2_9BvL3Mr" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    
    <button class="skip-btn" onclick="skipIntro()">تخطي →</button>
    
    <script>
        const video = document.getElementById('introVideo');
        
        video.addEventListener('ended', function() {
            window.location.href = '/login';
        });
        
        function skipIntro() {
            window.location.href = '/login';
        }
        
        // Auto redirect after 4 seconds
        setTimeout(() => {
            window.location.href = '/login';
        }, 4000);
    </script>
</body>
</html>
'''

#============================================
# Login Page HTML
#============================================

LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - تسجيل الدخول</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 400px;
            padding: 20px;
        }
        
        .login-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .logo {
            font-size: 48px;
            font-weight: 900;
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 20px rgba(0,255,136,0.5);
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            color: #fff;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 500;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px 20px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #00ff88;
            background: rgba(0,255,136,0.1);
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 15px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: #000;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,255,136,0.4);
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.15);
        }
        
        .error-message {
            background: rgba(255,68,68,0.2);
            border: 1px solid #ff4444;
            color: #ff4444;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .register-link {
            text-align: center;
            color: #888;
            margin-top: 20px;
        }
        
        .register-link a {
            color: #00ff88;
            text-decoration: none;
            font-weight: 700;
        }
        
        .register-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-card">
            <div class="logo">OTP KING</div>
            
            {% if error %}
            <div class="error-message">{{ error }}</div>
            {% endif %}
            
            <form method="POST" action="/login">
                <div class="input-group">
                    <label>👤 اسم المستخدم</label>
                    <input type="text" name="username" required>
                </div>
                
                <div class="input-group">
                    <label>🔐 كلمة المرور</label>
                    <input type="password" name="password" required>
                </div>
                
                <button type="submit" class="btn btn-primary">تسجيل الدخول</button>
            </form>
            
            <button class="btn btn-secondary" onclick="window.location.href='/register'">
                ✨ Create my account
            </button>
            
            <div class="register-link">
                ليس لديك حساب؟ <a href="/register">أنشئ حساب جديد</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

#============================================
# Register Page HTML
#============================================

REGISTER_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - إنشاء حساب</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 450px;
            padding: 20px;
        }
        
        .register-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .logo {
            font-size: 36px;
            font-weight: 900;
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 20px rgba(0,255,136,0.5);
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            color: #fff;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 500;
        }
        
        .input-group input, .input-group select {
            width: 100%;
            padding: 15px 20px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .input-group select {
            cursor: pointer;
            option { background: #24243e; }
        }
        
        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: #00ff88;
            background: rgba(0,255,136,0.1);
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 15px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: #000;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,255,136,0.4);
        }
        
        .error-message {
            background: rgba(255,68,68,0.2);
            border: 1px solid #ff4444;
            color: #ff4444;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .success-message {
            background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .login-link {
            text-align: center;
            color: #888;
            margin-top: 20px;
        }
        
        .login-link a {
            color: #00ff88;
            text-decoration: none;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="register-card">
            <div class="logo">إنشاء حساب جديد</div>
            
            {% if error %}
            <div class="error-message">{{ error }}</div>
            {% endif %}
            
            {% if success %}
            <div class="success-message">{{ success }}</div>
            {% endif %}
            
            <form method="POST" action="/register">
                <div class="input-group">
                    <label>👤 اسم المستخدم</label>
                    <input type="text" name="username" required placeholder="أدخل اسم المستخدم">
                </div>
                
                <div class="input-group">
                    <label>🔐 كلمة المرور</label>
                    <input type="password" name="password" required placeholder="أدخل كلمة المرور">
                </div>
                
                <div class="input-group">
                    <label>📱 معرف تليجرام</label>
                    <input type="text" name="telegram" required placeholder="@username">
                </div>
                
                <div class="input-group">
                    <label>🌍 الدولة</label>
                    <select name="country" required>
                        <option value="">اختر دولتك</option>
                        <option value="Egypt">🇪🇬 مصر</option>
                        <option value="Saudi Arabia">🇸🇦 السعودية</option>
                        <option value="UAE">🇦🇪 الإمارات</option>
                        <option value="Kuwait">🇰🇼 الكويت</option>
                        <option value="Qatar">🇶🇦 قطر</option>
                        <option value="Bahrain">🇧🇭 البحرين</option>
                        <option value="Oman">🇴🇲 عمان</option>
                        <option value="Jordan">🇯🇴 الأردن</option>
                        <option value="Palestine">🇵🇸 فلسطين</option>
                        <option value="Lebanon">🇱🇧 لبنان</option>
                        <option value="Iraq">🇮🇶 العراق</option>
                        <option value="Yemen">🇾🇪 اليمن</option>
                        <option value="Syria">🇸🇾 سوريا</option>
                        <option value="Libya">🇱🇾 ليبيا</option>
                        <option value="Tunisia">🇹🇳 تونس</option>
                        <option value="Algeria">🇩🇿 الجزائر</option>
                        <option value="Morocco">🇲🇦 المغرب</option>
                        <option value="Sudan">🇸🇩 السودان</option>
                    </select>
                </div>
                
                <button type="submit" class="btn btn-primary">✨ Create</button>
            </form>
            
            <div class="login-link">
                لديك حساب بالفعل؟ <a href="/login">تسجيل الدخول</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

#============================================
# Account Logs Page HTML (Owner Only)
#============================================

ACCOUNT_LOGS_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - سجلات الحسابات</title>
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
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 900;
            color: #00ff88;
        }
        
        .nav-buttons {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
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
        
        .btn-warning {
            background: #ffbb33;
            color: #000;
        }
        
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: 900;
            color: #00ff88;
        }
        
        .stat-label {
            font-size: 16px;
            color: #aaa;
        }
        
        .users-table {
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .table-header {
            display: grid;
            grid-template-columns: 0.5fr 1fr 1fr 1fr 1fr 0.8fr 2fr;
            background: rgba(0,255,136,0.2);
            padding: 15px;
            font-weight: 700;
            color: #00ff88;
        }
        
        .table-row {
            display: grid;
            grid-template-columns: 0.5fr 1fr 1fr 1fr 1fr 0.8fr 2fr;
            padding: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            align-items: center;
        }
        
        .table-row:hover {
            background: rgba(255,255,255,0.05);
        }
        
        .role-badge {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            display: inline-block;
        }
        
        .role-owner { background: linear-gradient(135deg, #ffbb33, #ff8800); color: #000; }
        .role-admin { background: linear-gradient(135deg, #00ff88, #00cc6a); color: #000; }
        .role-user { background: rgba(255,255,255,0.2); color: #fff; }
        
        .action-btn {
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            margin: 2px;
        }
        
        .action-btn.edit { background: #00ff88; color: #000; }
        .action-btn.delete { background: #ff4444; color: #fff; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: linear-gradient(135deg, #0f0c29, #302b63);
            padding: 40px;
            border-radius: 20px;
            max-width: 400px;
            width: 90%;
        }
        
        .search-box {
            margin-bottom: 20px;
        }
        
        .search-box input {
            width: 100%;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
        }
        
        @media (max-width: 768px) {
            .table-header, .table-row {
                grid-template-columns: 1fr;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">👑 OTP KING - لوحة التحكم</div>
            <div class="nav-buttons">
                <a href="/dashboard" class="btn btn-secondary">⬅️ العودة للوحة</a>
                <a href="/add-admin" class="btn btn-primary">➕ إضافة أدمن</a>
                <a href="/logout" class="btn btn-danger">🚪 تسجيل الخروج</a>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{{ stats.total_users }}</div>
                <div class="stat-label">إجمالي المستخدمين</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.total_admins }}</div>
                <div class="stat-label">عدد الأدمن</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.new_today }}</div>
                <div class="stat-label">جديد اليوم</div>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 بحث عن مستخدم..." onkeyup="searchUsers()">
        </div>
        
        <div class="users-table">
            <div class="table-header">
                <div>#</div>
                <div>👤 المستخدم</div>
                <div>🔐 كلمة المرور</div>
                <div>📱 تليجرام</div>
                <div>🌍 الدولة</div>
                <div>⭐ الصلاحية</div>
                <div>⚡ الإجراءات</div>
            </div>
            
            <div id="usersList">
                {% for user in users %}
                <div class="table-row" data-username="{{ user.username }}" data-country="{{ user.country }}">
                    <div>{{ loop.index }}</div>
                    <div>{{ user.username }}</div>
                    <div>{{ user.password }}</div>
                    <div>{{ user.telegram }}</div>
                    <div>{{ user.country }}</div>
                    <div>
                        <span class="role-badge role-{{ user.role }}">
                            {% if user.role == 'owner' %}👑 مالك
                            {% elif user.role == 'admin' %}⚡ أدمن
                            {% else %}👤 مستخدم{% endif %}
                        </span>
                    </div>
                    <div>
                        {% if user.role != 'owner' %}
                        <button class="action-btn edit" onclick="editPassword('{{ user.username }}')">🔑 تغيير</button>
                        <button class="action-btn edit" onclick="makeAdmin('{{ user.username }}')">⭐ أدمن</button>
                        <button class="action-btn delete" onclick="deleteUser('{{ user.username }}')">🗑️ حذف</button>
                        {% else %}
                        <span style="color:#888;">لا يمكن التعديل</span>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <!-- Edit Password Modal -->
    <div id="editModal" class="modal">
        <div class="modal-content">
            <h2 style="color:#00ff88; margin-bottom:20px;">تغيير كلمة المرور</h2>
            <input type="hidden" id="editUsername">
            <div class="input-group">
                <label style="color:#fff;">كلمة المرور الجديدة</label>
                <input type="password" id="newPassword" style="width:100%; padding:10px; margin:10px 0; background:rgba(255,255,255,0.1); border:1px solid #00ff88; border-radius:5px; color:#fff;">
            </div>
            <button class="btn btn-primary" style="width:100%;" onclick="savePassword()">حفظ التغييرات</button>
            <button class="btn btn-secondary" style="width:100%; margin-top:10px;" onclick="closeModal()">إلغاء</button>
        </div>
    </div>
    
    <script>
        function searchUsers() {
            const searchText = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('.table-row');
            
            rows.forEach(row => {
                const username = row.dataset.username.toLowerCase();
                const country = row.dataset.country.toLowerCase();
                
                if (username.includes(searchText) || country.includes(searchText)) {
                    row.style.display = 'grid';
                } else {
                    row.style.display = 'none';
                }
            });
        }
        
        function editPassword(username) {
            document.getElementById('editUsername').value = username;
            document.getElementById('editModal').style.display = 'flex';
        }
        
        function closeModal() {
            document.getElementById('editModal').style.display = 'none';
        }
        
        function savePassword() {
            const username = document.getElementById('editUsername').value;
            const newPassword = document.getElementById('newPassword').value;
            
            if (!newPassword) {
                alert('الرجاء إدخال كلمة المرور الجديدة');
                return;
            }
            
            fetch('/api/change-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: newPassword })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('تم تغيير كلمة المرور بنجاح');
                    location.reload();
                } else {
                    alert('حدث خطأ: ' + data.error);
                }
            });
        }
        
        function makeAdmin(username) {
            if (confirm('هل أنت متأكد من ترقية هذا المستخدم إلى أدمن؟')) {
                fetch('/api/make-admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: username })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('تم ترقية المستخدم إلى أدمن');
                        location.reload();
                    } else {
                        alert('حدث خطأ: ' + data.error);
                    }
                });
            }
        }
        
        function deleteUser(username) {
            if (confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
                fetch('/api/delete-user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: username })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('تم حذف المستخدم بنجاح');
                        location.reload();
                    } else {
                        alert('حدث خطأ: ' + data.error);
                    }
                });
            }
        }
    </script>
</body>
</html>
'''

#============================================
# Add Admin Page HTML (Owner Only)
#============================================

ADD_ADMIN_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP KING - إضافة أدمن</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 450px;
            padding: 20px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        
        h1 {
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
            font-size: 32px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            color: #fff;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            color: #fff;
            font-size: 16px;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #00ff88;
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: #000;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,255,136,0.4);
        }
        
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
        
        .message {
            background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .error {
            background: rgba(255,68,68,0.2);
            border: 1px solid #ff4444;
            color: #ff4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>➕ إضافة أدمن جديد</h1>
            
            {% if message %}
            <div class="message">{{ message }}</div>
            {% endif %}
            
            {% if error %}
            <div class="message error">{{ error }}</div>
            {% endif %}
            
            <form method="POST" action="/add-admin">
                <div class="input-group">
                    <label>👤 اسم المستخدم</label>
                    <input type="text" name="username" required>
                </div>
                
                <div class="input-group">
                    <label>🔐 كلمة المرور</label>
                    <input type="password" name="password" required>
                </div>
                
                <div class="input-group">
                    <label>📱 تليجرام</label>
                    <input type="text" name="telegram" required placeholder="@username">
                </div>
                
                <div class="input-group">
                    <label>🌍 الدولة</label>
                    <input type="text" name="country" required placeholder="مصر">
                </div>
                
                <button type="submit" class="btn btn-primary">✅ إضافة أدمن</button>
                <button type="button" class="btn btn-secondary" onclick="window.location.href='/account-logs'">⬅️ رجوع</button>
            </form>
        </div>
    </div>
</body>
</html>
'''

#============================================
# Main Dashboard HTML (Modified Original)
#============================================

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 SMS OTP Dashboard</title>
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
        
        .logo { 
            font-size: 24px; 
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stats-bar { display: flex; gap: 20px; flex-wrap: wrap; }
        
        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
        }
        
        .stat-value { font-size: 20px; font-weight: 700; color: #00ff88; }
        .stat-label { font-size: 12px; color: #aaa; }
        
        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .status-online { background: rgba(0,255,136,0.2); color: #00ff88; }
        .status-offline { background: rgba(255,68,68,0.2); color: #ff4444; }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        .btn {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary { background: linear-gradient(135deg, #00ff88, #00cc6a); color: #000; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: #fff; }
        .btn-danger { background: #ff4444; color: #fff; }
        .btn-warning { background: #ffbb33; color: #000; }
        
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
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .country-info { display: flex; align-items: center; gap: 10px; }
        .country-flag { font-size: 32px; }
        .country-name { font-weight: 600; }
        
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
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            color: #00ff88;
            cursor: pointer;
            margin-top: 10px;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .info-label { color: #888; font-size: 13px; }
        .info-value { color: #fff; font-size: 13px; }
        
        .message-content {
            background: rgba(0,0,0,0.2);
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 13px;
            color: #aaa;
            max-height: 100px;
            overflow-y: auto;
        }
        
        .timestamp { text-align: right; font-size: 11px; color: #666; margin-top: 10px; }
        
        .empty-state { text-align: center; padding: 60px; color: #888; grid-column: 1/-1; }
        .empty-icon { font-size: 64px; margin-bottom: 20px; }
        
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
        
        .debug-log { padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        
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
        
        .tabs { display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
        .tab {
            padding: 10px 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .tab.active { background: #00ff88; color: #000; }
        
        .user-info {
            background: rgba(255,255,255,0.05);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .header-content { flex-direction: column; }
            .messages-grid { grid-template-columns: 1fr; }
            .tabs { justify-content: center; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">
                📱 SMS OTP Dashboard
                <span class="user-info">{{ session.username }} ({{ session.role }})</span>
            </div>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-value">{{ stats.total_otps }}</div>
                    <div class="stat-label">Total OTPs</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ stats.last_check }}</div>
                    <div class="stat-label">Last Check</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ messages|length }}</div>
                    <div class="stat-label">Messages</div>
                </div>
            </div>
            
            <div class="status-badge {{ 'status-online' if stats.is_running else 'status-offline' }}">
                {{ '🟢 Online' if stats.is_running else '🔴 Offline' }}
            </div>
        </div>
    </header>
    
    <div class="container">
        <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; margin-bottom: 20px;">
            <div>
                <button class="btn btn-primary" onclick="location.reload()">🔄 Refresh</button>
                <button class="btn btn-secondary" onclick="manualCheck()">⚡ Force Check</button>
                <button class="btn btn-danger" onclick="clearAll()">🗑️ Clear All</button>
                <button class="btn btn-secondary" onclick="toggleDebug()">🔧 Debug</button>
            </div>
            <div>
                {% if session.role == 'owner' %}
                <a href="/account-logs" class="btn btn-warning">📋 Account Logs</a>
                <a href="/add-admin" class="btn btn-primary">➕ Add Admin</a>
                {% endif %}
                <a href="/logout" class="btn btn-danger">🚪 Logout</a>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('messages')">📨 Messages</div>
            <div class="tab" onclick="showTab('debug')">🔧 Debug Logs</div>
        </div>
        
        <!-- Debug Panel -->
        <div id="debugPanel" class="debug-panel" style="display:none;">
            <h3>🔧 Debug Logs</h3>
            <p><strong>Status:</strong> {{ stats.scraper_status }}</p>
            <p><strong>Last Error:</strong> {{ stats.last_error or 'None' }}</p>
            <p><strong>Panel URL:</strong> {{ panel_url }}</p>
            <hr style="margin: 10px 0; border-color: rgba(255,255,255,0.1);">
            <h4>API Response:</h4>
            <pre style="white-space: pre-wrap;">{{ stats.api_response or 'No response yet' }}</pre>
            <hr style="margin: 10px 0; border-color: rgba(255,255,255,0.1);">
            <h4>Logs:</h4>
            {% for log in debug_logs %}
            <div class="debug-log">{{ log }}</div>
            {% endfor %}
        </div>
        
        <!-- Messages Grid -->
        <div id="messagesPanel" class="messages-grid">
            {% if messages %}
                {% for msg in messages %}
                <div class="message-card">
                    <div class="card-header">
                        <div class="country-info">
                            <span class="country-flag">{{ msg.country_flag }}</span>
                            <span class="country-name">{{ msg.country or 'Unknown' }}</span>
                        </div>
                        <span class="service-badge">{{ msg.service }}</span>
                    </div>
                    
                    <div class="otp-section">
                        <div style="font-size:12px; color:#888;">OTP CODE</div>
                        <div class="otp-code">{{ msg.otp }}</div>
                        <button class="copy-btn" onclick="copyOTP(this, '{{ msg.otp }}')">📋 Copy</button>
                    </div>
                    
                    <div class="info-row">
                        <span class="info-label">📱 Phone</span>
                        <span class="info-value">{{ msg.phone_masked }}</span>
                    </div>
                    
                    <div class="info-row">
                        <span class="info-label">🆔 ID</span>
                        <span class="info-value">{{ msg.id }}</span>
                    </div>
                    
                    <div class="message-content">{{ msg.raw_message }}</div>
                    <div class="timestamp">⏰ {{ msg.timestamp }}</div>
                </div>
                {% endfor %}
            {% else %}
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <h3>No messages yet</h3>
                    <p>Waiting for OTP messages...</p>
                    <p style="margin-top:10px; color:#666;">Check Debug panel for details</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="refresh-indicator">
        <span class="pulse"></span>
        Auto-refresh: <span id="countdown">10</span>s
    </div>

    <script>
        function copyOTP(btn, otp) {
            navigator.clipboard.writeText(otp.replace(/-/g, ''));
            btn.textContent = '✅ Copied!';
            setTimeout(() => btn.textContent = '📋 Copy', 2000);
        }
        
        function manualCheck() {
            fetch('/api/refresh').then(() => location.reload());
        }
        
        function clearAll() {
            if(confirm('Clear all messages?')) {
                fetch('/api/clear').then(() => location.reload());
            }
        }
        
        function toggleDebug() {
            const panel = document.getElementById('debugPanel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }
        
        function showTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            
            if(tab === 'debug') {
                document.getElementById('debugPanel').style.display = 'block';
                document.getElementById('messagesPanel').style.display = 'none';
            } else {
                document.getElementById('debugPanel').style.display = 'none';
                document.getElementById('messagesPanel').style.display = 'grid';
            }
        }
        
        // Auto-refresh
        let countdown = 10;
        setInterval(() => {
            countdown--;
            document.getElementById('countdown').textContent = countdown;
            if (countdown <= 0) {
                location.reload();
            }
        }, 1000);
    </script>
</body>
</html>
'''

#============================================
# Original OTP System Code (Modified)
#============================================

PANEL_URL = "http://198.135.52.238"
PANEL_USERNAME = "gagaywb66"
PANEL_PASSWORD = "gagaywb66"

all_messages = []
MAX_MESSAGES = 100
debug_logs = []

bot_stats = {
    'start_time': datetime.now(),
    'total_otps': 0,
    'last_check': 'Never',
    'is_running': False,
    'scraper_status': 'Not initialized',
    'last_error': None,
    'api_response': None
}

scraper = None

#============================================
# أعلام الدول
#============================================

COUNTRY_FLAGS = {
    'venezuela': '🇻🇪', 've': '🇻🇪',
    'brazil': '🇧🇷', 'br': '🇧🇷',
    'argentina': '🇦🇷', 'ar': '🇦🇷',
    'colombia': '🇨🇴', 'co': '🇨🇴',
    'usa': '🇺🇸', 'us': '🇺🇸', 'united states': '🇺🇸',
    'canada': '🇨🇦', 'ca': '🇨🇦',
    'mexico': '🇲🇽', 'mx': '🇲🇽',
    'uk': '🇬🇧', 'gb': '🇬🇧', 'united kingdom': '🇬🇧',
    'germany': '🇩🇪', 'de': '🇩🇪',
    'france': '🇫🇷', 'fr': '🇫🇷',
    'italy': '🇮🇹', 'it': '🇮🇹',
    'spain': '🇪🇸', 'es': '🇪🇸',
    'russia': '🇷🇺', 'ru': '🇷🇺',
    'india': '🇮🇳', 'in': '🇮🇳',
    'china': '🇨🇳', 'cn': '🇨🇳',
    'japan': '🇯🇵', 'jp': '🇯🇵',
    'korea': '🇰🇷', 'kr': '🇰🇷',
    'indonesia': '🇮🇩', 'id': '🇮🇩',
    'malaysia': '🇲🇾', 'my': '🇲🇾',
    'philippines': '🇵🇭', 'ph': '🇵🇭',
    'vietnam': '🇻🇳', 'vn': '🇻🇳',
    'thailand': '🇹🇭', 'th': '🇹🇭',
    'singapore': '🇸🇬', 'sg': '🇸🇬',
    'pakistan': '🇵🇰', 'pk': '🇵🇰',
    'bangladesh': '🇧🇩', 'bd': '🇧🇩',
    'tajikistan': '🇹🇯', 'tj': '🇹🇯',
    'uzbekistan': '🇺🇿', 'uz': '🇺🇿',
    'kazakhstan': '🇰🇿', 'kz': '🇰🇿',
    'ukraine': '🇺🇦', 'ua': '🇺🇦',
    'poland': '🇵🇱', 'pl': '🇵🇱',
    'turkey': '🇹🇷', 'tr': '🇹🇷',
    'saudi': '🇸🇦', 'sa': '🇸🇦',
    'uae': '🇦🇪', 'ae': '🇦🇪',
    'egypt': '🇪🇬', 'eg': '🇪🇬',
    'morocco': '🇲🇦', 'ma': '🇲🇦',
    'nigeria': '🇳🇬', 'ng': '🇳🇬',
    'australia': '🇦🇺', 'au': '🇦🇺',
    'sudan': '🇸🇩', 'sd': '🇸🇩',
}

#============================================
# Database Functions
#============================================

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_panel_settings():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM panel_settings ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    if result:
        return {
            'panel_url': result['panel_url'],
            'panel_username': result['panel_username'],
            'panel_password': result['panel_password']
        }
    return {
        'panel_url': PANEL_URL,
        'panel_username': PANEL_USERNAME,
        'panel_password': PANEL_PASSWORD
    }

#============================================
# Debug Log
#============================================

def add_debug(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log = f"[{timestamp}] {message}"
    debug_logs.insert(0, log)
    if len(debug_logs) > 50:
        debug_logs.pop()
    logger.info(message)

#============================================
# إخفاء جزء من الرقم
#============================================

def mask_phone_number(phone):
    if not phone or phone == 'Unknown':
        return 'Unknown'
    phone = str(phone).strip()
    if len(phone) <= 6:
        return phone[:2] + '•••' + phone[-1:]
    if phone.startswith('+'):
        return f"{phone[:5]}•••{phone[-4:]}"
    return f"{phone[:4]}•••{phone[-4:]}"

#============================================
# API Scraper
#============================================

class PanelAPI:
    def __init__(self):
        settings = get_panel_settings()
        self.base_url = settings['panel_url'].rstrip('/')
        self.username = settings['panel_username']
        self.password = settings['panel_password']
        self.token = None
        self.session = requests.Session()
        self.logged_in = False
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 Chrome/120.0.0.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    
    def login(self):
        try:
            add_debug(f"🔐 Attempting login to {self.base_url}")
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"username": self.username, "password": self.password},
                timeout=15
            )
            
            add_debug(f"📥 Login response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                add_debug(f"📥 Login response: {str(data)[:200]}")
                
                if 'token' in data:
                    self.token = data['token']
                    self.logged_in = True
                    self.session.headers['Authorization'] = f'Bearer {self.token}'
                    bot_stats['scraper_status'] = '✅ Connected'
                    add_debug("✅ Login successful!")
                    return True
                else:
                    add_debug(f"❌ No token in response: {data}")
            else:
                add_debug(f"❌ Login failed: {response.text[:200]}")
            
            bot_stats['scraper_status'] = '❌ Login failed'
            return False
            
        except Exception as e:
            add_debug(f"❌ Login error: {str(e)}")
            bot_stats['scraper_status'] = f'❌ Error: {str(e)[:50]}'
            bot_stats['last_error'] = str(e)
            return False
    
    def fetch_messages(self):
        if not self.logged_in:
            add_debug("⚠️ Not logged in, attempting login...")
            if not self.login():
                return []
        
        try:
            url = f"{self.base_url}/api/sms?limit=100"
            add_debug(f"📥 Fetching from: {url}")
            
            response = self.session.get(url, timeout=15)
            add_debug(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 401:
                add_debug("⚠️ Token expired, re-logging in...")
                self.logged_in = False
                if not self.login():
                    return []
                response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                add_debug(f"❌ Failed to fetch: {response.status_code}")
                add_debug(f"Response: {response.text[:300]}")
                return []
            
            # حفظ الـ response للـ debug
            raw_data = response.text
            bot_stats['api_response'] = raw_data[:1000]
            add_debug(f"📥 Raw response: {raw_data[:300]}")
            
            try:
                data = response.json()
            except:
                add_debug(f"❌ Invalid JSON response")
                return []
            
            add_debug(f"📥 Response type: {type(data)}")
            
            if isinstance(data, list):
                messages = data
                add_debug(f"📥 Response is a list with {len(messages)} items")
            elif isinstance(data, dict):
                add_debug(f"📥 Response keys: {list(data.keys())}")
                messages = data.get('messages', data.get('sms', data.get('data', [])))
                add_debug(f"📥 Extracted {len(messages)} messages")
            else:
                add_debug(f"❌ Unknown response type: {type(data)}")
                messages = []
            
            if messages and len(messages) > 0:
                add_debug(f"📨 First message sample: {json.dumps(messages[0], ensure_ascii=False)[:300]}")
            
            formatted = []
            for i, m in enumerate(messages):
                f = self._format_message(m)
                if f:
                    formatted.append(f)
                    if i == 0:
                        add_debug(f"✅ Formatted first message: {f.get('otp')} - {f.get('service')}")
            
            add_debug(f"📨 Total formatted: {len(formatted)}")
            return formatted
            
        except Exception as e:
            add_debug(f"❌ Fetch error: {str(e)}")
            bot_stats['last_error'] = str(e)
            return []
    
    def _format_message(self, msg):
        try:
            content = msg.get('message', msg.get('content', msg.get('text', '')))
            otp = self._extract_otp(content)
            
            phone = msg.get('phone_number', msg.get('Number', msg.get('number', msg.get('phone', 'Unknown'))))
            country_name = msg.get('country', msg.get('Country', ''))
            country_flag = self._get_country_flag(country_name)
            
            service = (
                msg.get('sender', msg.get('service', msg.get('Service', ''))) or 
                self._detect_service(content)
            )
            
            timestamp = msg.get('received_at', msg.get('created_at', msg.get('timestamp', '')))
            if timestamp:
                try:
                    dt = datetime.strptime(str(timestamp)[:19], '%Y-%m-%dT%H:%M:%S')
                    timestamp = dt.strftime('%Y-%m-%d %I:%M %p')
                except:
                    timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
            
            return {
                'otp': otp,
                'phone': phone,
                'phone_masked': mask_phone_number(phone),
                'service': service or 'SMS Service',
                'country': country_name or 'Unknown',
                'country_flag': country_flag,
                'timestamp': timestamp,
                'raw_message': content[:200] if content else '',
                'id': msg.get('id', msg.get('_id', str(hash(str(msg)))))
            }
        except Exception as e:
            add_debug(f"❌ Format error: {str(e)}")
            return None
    
    def _extract_otp(self, content):
        if not content:
            return 'N/A'
        
        patterns = [
            r'(\d{3}[-\s]?\d{3})',
            r'(\d{4}[-\s]?\d{4})',
            r'(?:code|kode|otp|كود)[:\s]*(\d{4,8})',
            r'(\d{6})',
            r'(\d{4,8})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.I)
            if match:
                return match.group(1).replace(' ', '-').replace('-', '')
        return 'N/A'
    
    def _detect_service(self, content):
        if not content:
            return 'Unknown'
        
        services = {
            'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
            'facebook': 'Facebook', 'instagram': 'Instagram',
            'twitter': 'Twitter', 'google': 'Google',
            'tiktok': 'TikTok', 'snapchat': 'Snapchat',
            'adobe': 'Adobe', 'microsoft': 'Microsoft',
            'apple': 'Apple', 'amazon': 'Amazon',
        }
        
        content_lower = content.lower()
        for key, name in services.items():
            if key in content_lower:
                return name
        return 'SMS Service'
    
    def _get_country_flag(self, country):
        if not country:
            return '🌍'
        country_lower = country.lower().strip()
        if country_lower in COUNTRY_FLAGS:
            return COUNTRY_FLAGS[country_lower]
        for key, flag in COUNTRY_FLAGS.items():
            if key in country_lower:
                return flag
        return '🌍'


def create_scraper():
    try:
        add_debug("🔧 Creating scraper...")
        api = PanelAPI()
        if api.login():
            add_debug("✅ Scraper ready")
        return api
    except Exception as e:
        add_debug(f"❌ Scraper error: {str(e)}")
        return None

#============================================
# OTP Filter
#============================================

class OTPFilter:
    def __init__(self):
        self.cache = set()
    
    def is_new(self, msg_id):
        if msg_id in self.cache:
            return False
        self.cache.add(msg_id)
        if len(self.cache) > 1000:
            self.cache = set(list(self.cache)[-500:])
        return True
    
    def clear(self):
        self.cache.clear()

otp_filter = OTPFilter()

#============================================
# Background Monitor
#============================================

def check_and_update():
    global scraper, all_messages
    
    try:
        add_debug("🔄 Starting check...")
        
        if not scraper:
            add_debug("⚠️ No scraper, creating...")
            scraper = create_scraper()
            if not scraper:
                add_debug("❌ Failed to create scraper")
                return
        
        if not scraper.logged_in:
            add_debug("⚠️ Not logged in, logging in...")
            if not scraper.login():
                add_debug("❌ Login failed")
                return
        
        messages = scraper.fetch_messages()
        bot_stats['last_check'] = datetime.now().strftime('%H:%M:%S')
        
        add_debug(f"📨 Fetched {len(messages)} messages")
        
        new_count = 0
        for msg in messages:
            if otp_filter.is_new(msg['id']):
                all_messages.insert(0, msg)
                bot_stats['total_otps'] += 1
                new_count += 1
        
        add_debug(f"🆕 New messages: {new_count}")
        
        all_messages = all_messages[:MAX_MESSAGES]
                
    except Exception as e:
        add_debug(f"❌ Check error: {str(e)}")
        bot_stats['last_error'] = str(e)

def background_monitor():
    bot_stats['is_running'] = True
    add_debug("🚀 Background monitor started")
    
    # First check immediately
    check_and_update()
    
    while bot_stats['is_running']:
        try:
            time.sleep(10)
            check_and_update()
        except Exception as e:
            add_debug(f"❌ Monitor error: {str(e)}")
            time.sleep(30)

#============================================
# Flask Routes - Authentication
#============================================

@app.route('/')
def index():
    return render_template_string(VIDEO_INTRO)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
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
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_PAGE, error="اسم المستخدم أو كلمة المرور غير صحيحة")
    
    return render_template_string(LOGIN_PAGE)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telegram = request.form.get('telegram')
        country = request.form.get('country')
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users (username, password, telegram, country, role) VALUES (?, ?, ?, ?, 'user')",
                     (username, password, telegram, country))
            conn.commit()
            success = "تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن"
            return render_template_string(REGISTER_PAGE, success=success)
        except sqlite3.IntegrityError:
            error = "اسم المستخدم موجود بالفعل"
            return render_template_string(REGISTER_PAGE, error=error)
        finally:
            conn.close()
    
    return render_template_string(REGISTER_PAGE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

#============================================
# Flask Routes - Dashboard
#============================================

@app.route('/dashboard')
@login_required
def dashboard():
    settings = get_panel_settings()
    return render_template_string(DASHBOARD_TEMPLATE, 
                                  messages=all_messages, 
                                  stats=bot_stats,
                                  debug_logs=debug_logs,
                                  session=session,
                                  panel_url=settings['panel_url'])

@app.route('/account-logs')
@owner_required
def account_logs():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    conn.close()
    
    stats = {
        'total_users': len(users),
        'total_admins': len([u for u in users if u['role'] in ['admin', 'owner']]),
        'new_today': len([u for u in users if u['created_at'].startswith(datetime.now().strftime('%Y-%m-%d'))])
    }
    
    return render_template_string(ACCOUNT_LOGS_PAGE, users=users, stats=stats)

@app.route('/add-admin', methods=['GET', 'POST'])
@owner_required
def add_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telegram = request.form.get('telegram')
        country = request.form.get('country')
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users (username, password, telegram, country, role) VALUES (?, ?, ?, ?, 'admin')",
                     (username, password, telegram, country))
            conn.commit()
            return render_template_string(ADD_ADMIN_PAGE, message="✅ تم إضافة الأدمن بنجاح")
        except sqlite3.IntegrityError:
            return render_template_string(ADD_ADMIN_PAGE, error="❌ اسم المستخدم موجود بالفعل")
        finally:
            conn.close()
    
    return render_template_string(ADD_ADMIN_PAGE)

#============================================
# API Routes
#============================================

@app.route('/api/messages')
@login_required
def api_messages():
    return jsonify({
        'messages': all_messages,
        'stats': bot_stats,
        'debug': debug_logs[:10]
    })

@app.route('/api/refresh')
@login_required
def api_refresh():
    add_debug("⚡ Manual refresh triggered")
    check_and_update()
    return jsonify({'status': 'ok', 'count': len(all_messages)})

@app.route('/api/clear')
@login_required
def api_clear():
    global all_messages
    all_messages = []
    otp_filter.clear()
    bot_stats['total_otps'] = 0
    add_debug("🗑️ Cache cleared")
    return jsonify({'status': 'ok'})

@app.route('/api/debug')
@login_required
def api_debug():
    return jsonify({
        'stats': bot_stats,
        'logs': debug_logs,
        'messages_count': len(all_messages)
    })

@app.route('/api/change-password', methods=['POST'])
@owner_required
def change_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('password')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/make-admin', methods=['POST'])
@owner_required
def make_admin():
    data = request.json
    username = data.get('username')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET role='admin' WHERE username=?", (username,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/delete-user', methods=['POST'])
@owner_required
def delete_user():
    data = request.json
    username = data.get('username')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=? AND role!='owner'", (username,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

#============================================
# Main
#============================================

def main():
    global scraper
    
    add_debug("🚀 Starting SMS OTP Dashboard...")
    
    scraper = create_scraper()
    
    threading.Thread(target=background_monitor, daemon=True).start()
    
    port = int(os.environ.get('PORT', 5000))
    add_debug(f"🌐 Dashboard at http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    main()




# ============================================
# EXTRA FEATURES MERGED (Chat + Force + Sites)
# ============================================

import sqlite3
from datetime import datetime
from flask import jsonify, session, request, redirect

CHAT_DB = "extra_features.db"

def init_extra_db():
    conn = sqlite3.connect(CHAT_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chat(id INTEGER PRIMARY KEY, username TEXT, message TEXT, time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS sites(id INTEGER PRIMARY KEY, owner TEXT, name TEXT, created TEXT)")
    conn.commit()
    conn.close()

init_extra_db()

def extra_db():
    conn = sqlite3.connect(CHAT_DB)
    conn.row_factory = sqlite3.Row
    return conn

# ================= CHAT =================

@app.route("/chat")
def chat_room():
    if "username" not in session:
        return redirect("/login")
    return '''
    <h2>💬 Chat Room</h2>
    <div id="box"></div>
    <input id="msg"><button onclick="send()">Send</button>
    <script>
    function load(){
        fetch("/api/chat").then(r=>r.json()).then(data=>{
            let h="";
            data.forEach(m=>{h+=`<p><b>${m.username}</b>: ${m.message}</p>`})
            document.getElementById("box").innerHTML=h;
        })
    }
    function send(){
        fetch("/api/send",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({message:document.getElementById("msg").value})
        }).then(()=>{document.getElementById("msg").value="";load();})
    }
    setInterval(load,2000);load();
    </script>
    '''

@app.route("/api/chat")
def api_chat():
    conn=extra_db()
    msgs=conn.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(m) for m in msgs])

@app.route("/api/send", methods=["POST"])
def api_send():
    if "username" not in session:
        return jsonify({"error":"login required"})
    data=request.json
    conn=extra_db()
    conn.execute("INSERT INTO chat(username,message,time) VALUES(?,?,?)",
                 (session["username"], data["message"], datetime.now().strftime("%H:%M:%S")))
    conn.commit()
    conn.close()
    return jsonify({"ok":True})

# ================= FORCE CHECK =================

@app.route("/force-check")
def force_check():
    if "username" not in session:
        return jsonify({"msg":"Login Required"})
    return jsonify({"msg":"⚡ Force Check Activated"})

# ================= CREATE WEBSITE =================

@app.route("/create-site", methods=["GET","POST"])
def create_site():
    if "username" not in session:
        return redirect("/login")
    if request.method=="POST":
        name=request.form["name"]
        conn=extra_db()
        conn.execute("INSERT INTO sites(owner,name,created) VALUES(?,?,?)",
                     (session["username"], name, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        link=request.host_url+"site/"+name
        return f"Created:<br><a href='{link}'>{link}</a>"
    return '''
    <h2>🌐 Create Website</h2>
    <form method="post">
    <input name="name" placeholder="Enter site name">
    <button>Create</button>
    </form>
    '''

@app.route("/site/<name>")
def view_site(name):
    return f"<h1>Welcome to {name}</h1><p>Powered by OTP KING</p>"


