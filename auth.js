// Authentication Module for IVASMS Extension
// Handles password verification from remote API

const AUTH_CONFIG_URL = 'https://gist.githubusercontent.com/siamdev1/5493c7309d4ba65d3e8c30867212d75d/raw/password.json';
const AUTH_STORAGE_KEY = 'ivasms_auth';

// Fetch password configuration from GitHub Gist
async function fetchPasswordConfig() {
    try {
        const response = await fetch(AUTH_CONFIG_URL);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('[Auth] Failed to fetch config:', error);
        throw new Error('Failed to connect to authentication server');
    }
}

// Check if extension has expired
function isExpired(expiresISO) {
    const expirationDate = new Date(expiresISO);
    const now = new Date();
    console.log('[Auth] Expiration check:', {
        expires: expiresISO,
        expirationDate: expirationDate.toISOString(),
        now: now.toISOString(),
        isExpired: now > expirationDate
    });
    return now > expirationDate;
}

// Verify password against remote config
async function verifyPassword(inputPassword) {
    const config = await fetchPasswordConfig();

    // Check expiration first
    if (isExpired(config.expires)) {
        throw new Error('EXPIRED');
    }

    // Check password
    if (inputPassword === config.password) {
        return {
            success: true,
            text: config.text,
            expires: config.expires
        };
    } else {
        throw new Error('Invalid password');
    }
}

// Check if user is authenticated (from local storage)
async function isAuthenticated() {
    try {
        const result = await chrome.storage.local.get([AUTH_STORAGE_KEY]);
        if (!result[AUTH_STORAGE_KEY]) {
            return false;
        }

        const authData = result[AUTH_STORAGE_KEY];

        // Check if stored auth has expired
        if (isExpired(authData.expires)) {
            await clearAuth();
            return false;
        }

        return true;
    } catch (error) {
        console.error('[Auth] Error checking authentication:', error);
        return false;
    }
}

// Store authentication
async function storeAuth(expiresISO, text) {
    await chrome.storage.local.set({
        [AUTH_STORAGE_KEY]: {
            authenticated: true,
            expires: expiresISO,
            text: text,
            timestamp: new Date().toISOString()
        }
    });
}

// Clear authentication
async function clearAuth() {
    await chrome.storage.local.remove(AUTH_STORAGE_KEY);
}

// Get stored auth data
async function getAuthData() {
    const result = await chrome.storage.local.get([AUTH_STORAGE_KEY]);
    return result[AUTH_STORAGE_KEY] || null;
}

// Export functions (will be used by popup.js and background.js)
if (typeof window !== 'undefined') {
    window.IvasmsAuth = {
        fetchPasswordConfig,
        verifyPassword,
        isAuthenticated,
        storeAuth,
        clearAuth,
        getAuthData,
        isExpired
    };
}
