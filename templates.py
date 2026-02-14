#============================================
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
