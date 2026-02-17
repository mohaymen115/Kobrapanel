// URL Obfuscation Utilities
// Simple obfuscation to deter casual copying (not true security)

// Decode obfuscated URL
function d(encoded) {
    try {
        // Reverse the string and decode from base64
        return atob(encoded.split('').reverse().join(''));
    } catch (e) {
        console.error('[URL] Decode failed:', e);
        return '';
    }
}

// Encode URL (for development - won't be included in final build)
function e(url) {
    return btoa(url).split('').reverse().join('');
}

// Obfuscated IVASMS API URLs
const IVASMS_URLS = {
    // Base URLs
    base: d('bW9jLnNtc2F2aS53d3cvLzpzcHR0aA=='),

    // Portal endpoints
    portal: {
        sms: {
            received: d('ZGV2aWVjZXIvc21zL2xhdHJvcC9tb2Muc21zYXZpLnd3dy8vOnNwdHRo'),
            getSMS: d('c21zc3RlZy9kZXZpZWNlci9zbXMvbGF0cm9wL21vYy5zbXNhdmkud3d3Ly86c3B0dGg='),
            getDetails: d('cmVibXVuL3NtczpzdGVnL2RldmllY2VyL3Ntcy9sYXRyb3AvbW9jLnNtc2F2aS53d3cvLzpzcHR0aA=='),
            getDetailsNumber: d('c21zL3JlYm11bi9zbXM6c3RlZy9kZXZpZWNlci9zbXMvbGF0cm9wL21vYy5zbXNhdmkud3d3Ly86c3B0dGg='),
            test: d('c21zL3RzZXQvc21zL2xhdHJvcC9tb2Muc21zYXZpLnd3dy8vOnNwdHRo')
        }
    }
};

// Build full URL
function buildUrl(path) {
    if (path.startsWith('http')) {
        return path; // Already full URL
    }
    return `${IVASMS_URLS.base}${path}`;
}

// Export
if (typeof window !== 'undefined') {
    window.IvasmsUrls = {
        d,
        urls: IVASMS_URLS,
        buildUrl
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { d, IVASMS_URLS, buildUrl };
}
