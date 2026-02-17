// ============================================
// EXPIRATION CHECK - Locks extension on ALL devices
// ============================================

const AUTH_CONFIG_URL = 'https://gist.githubusercontent.com/siamdev1/5493c7309d4ba65d3e8c30867212d75d/raw/password.json';
const AUTH_STORAGE_KEY = 'ivasms_auth';

// Check expiration and lock if expired
async function checkAndLockIfExpired() {
    try {
        const response = await fetch(AUTH_CONFIG_URL);
        const config = await response.json();

        const expirationDate = new Date(config.expires);
        const now = new Date();

        if (now > expirationDate) {
            // Extension expired - clear all auth data on THIS device
            await chrome.storage.local.remove(AUTH_STORAGE_KEY);
            console.log('[Auth] Extension expired - session locked');

            // Notify open popups to refresh and show lock screen
            chrome.runtime.sendMessage({ type: 'AUTH_EXPIRED' }).catch(() => { });
        }
    } catch (error) {
        console.error('[Auth] Expiration check failed:', error);
    }
}

// Run check on startup
checkAndLockIfExpired();

// Check every 5 minutes (300000ms)
setInterval(checkAndLockIfExpired, 5 * 60 * 1000);

// Check when browser starts
chrome.runtime.onStartup.addListener(() => {
    checkAndLockIfExpired();
});

// ============================================
// MAIN BACKGROUND SCRIPT
// ============================================

// Background Service Worker for IVASMS Auto Range Add Extension
// This allows processing to continue even when popup is closed

let processingState = {
    isRunning: false,
    shouldStop: false,
    currentIndex: 0,
    numbers: [],
    results: [],
    delay: 1000
};

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startProcessing') {
        startBackgroundProcessing(request.numbers, request.delay);
        sendResponse({ success: true });
    } else if (request.action === 'stopProcessing') {
        processingState.shouldStop = true;
        sendResponse({ success: true });
    } else if (request.action === 'startReturning') {
        startBackgroundReturning(request.ids, request.batchSize);
        sendResponse({ success: true });
    } else if (request.action === 'stopReturning') {
        processingState.shouldStop = true;
        sendResponse({ success: true });
    } else if (request.action === 'startMessageCollection') {
        startMessageCollection(request.startDate, request.endDate, request.tabId);
        sendResponse({ success: true });
    } else if (request.action === 'getMessageCollectionState') {
        chrome.storage.local.get(['messageCollectionState'], (result) => {
            sendResponse(result.messageCollectionState || { status: 'idle' });
        });
        return true;
    } else if (request.action === 'getMessageHistory') {
        chrome.storage.local.get(['messageHistory'], (result) => {
            sendResponse(result.messageHistory || []);
        });
        return true;
    } else if (request.action === 'getState') {
        sendResponse(processingState);
    } else if (request.action === 'clearResults') {
        processingState.results = [];
        chrome.storage.local.set({ results: [] });
        sendResponse({ success: true });
    }
    return true;
});

async function startBackgroundProcessing(numbers, delay) {
    if (processingState.isRunning) {
        return;
    }

    processingState = {
        isRunning: true,
        shouldStop: false,
        currentIndex: 0,
        numbers: numbers,
        results: [],
        delay: delay
    };

    // Show badge to indicate processing
    chrome.action.setBadgeText({ text: '...' });
    chrome.action.setBadgeBackgroundColor({ color: '#667eea' });

    for (let i = 0; i < numbers.length; i++) {
        if (processingState.shouldStop) {
            addResult('warning', `Process stopped by user at ${i}/${numbers.length}`);
            break;
        }

        processingState.currentIndex = i;
        const number = numbers[i];

        // Update badge with progress
        chrome.action.setBadgeText({ text: `${i + 1}` });

        try {
            addResult('info', `Processing: ${number}...`);

            // Get active IVASMS tab
            const tabs = await chrome.tabs.query({ url: 'https://www.ivasms.com/*' });

            if (tabs.length === 0) {
                addResult('error', `No IVASMS tab found. Please open IVASMS.`);
                break;
            }

            // Execute in the page context
            const result = await chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                func: addNumberToRange,
                args: [number]
            });

            if (result[0].result.success) {
                addResult('success', `✓ Added: ${number} (${result[0].result.range})`);
            } else {
                addResult('error', `✗ Failed: ${number} - ${result[0].result.error}`);
            }
        } catch (error) {
            addResult('error', `✗ Error: ${number} - ${error.message}`);
        }

        // Add delay between requests
        if (delay > 0 && i < numbers.length - 1 && !processingState.shouldStop) {
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    // Final summary
    const successful = processingState.results.filter(r => r.type === 'success').length;
    const failed = processingState.results.filter(r => r.type === 'error' && r.message.includes('Failed')).length;

    addResult('info', `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    addResult('info', `📊 Summary:`);
    addResult('success', `✓ ${successful} range${successful !== 1 ? 's' : ''} added successfully`);
    if (failed > 0) {
        addResult('error', `✗ ${failed} range${failed !== 1 ? 's' : ''} failed`);
    }
    addResult('info', `Total processed: ${processingState.currentIndex + 1}`);

    // Show completion notification
    const successMsg = `${successful} range${successful !== 1 ? 's' : ''} added successfully`;
    const failMsg = failed > 0 ? `, ${failed} failed` : '';
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon128.png',
        title: 'IVASMS Auto Range Add - Complete! 🎉',
        message: `${successMsg}${failMsg}`,
        priority: 2
    });

    // Reset state
    processingState.isRunning = false;
    chrome.action.setBadgeText({ text: '' });
}

function addResult(type, message) {
    const result = {
        type: type,
        message: message,
        timestamp: new Date().toISOString()
    };

    processingState.results.push(result);

    // Store in chrome.storage so it persists
    chrome.storage.local.set({ results: processingState.results });

    // Notify popup if it's open
    chrome.runtime.sendMessage({ action: 'logUpdate', result: result }).catch(() => {
        // Popup might be closed, that's ok
    });
}

// This function runs in the page context
async function addNumberToRange(testNumber) {
    try {
        // Get CSRF token from the page
        const tokenInput = document.querySelector('input[name="_token"]');
        if (!tokenInput) {
            return { success: false, error: 'CSRF token not found. Please refresh IVASMS page.' };
        }
        const token = tokenInput.value;

        // Step 1: Search for the test number
        const draw = Date.now();
        const timestamp = Date.now();
        const searchParams = new URLSearchParams({
            'draw': draw,
            'columns[0][data]': 'range',
            'columns[1][data]': 'test_number',
            'columns[2][data]': 'term',
            'columns[2][searchable]': 'false',
            'columns[2][orderable]': 'false',
            'columns[3][data]': 'P2P',
            'columns[3][searchable]': 'false',
            'columns[3][orderable]': 'false',
            'columns[4][data]': 'A2P',
            'columns[4][searchable]': 'false',
            'columns[4][orderable]': 'false',
            'columns[5][data]': 'Limit_Range',
            'columns[5][searchable]': 'false',
            'columns[5][orderable]': 'false',
            'columns[6][data]': 'limit_cli_a2p',
            'columns[6][searchable]': 'false',
            'columns[7][data]': 'limit_did_a2p',
            'columns[7][searchable]': 'false',
            'columns[8][data]': 'limit_cli_did_a2p',
            'columns[8][searchable]': 'false',
            'columns[9][data]': 'limit_cli_p2p',
            'columns[9][searchable]': 'false',
            'columns[10][data]': 'limit_did_p2p',
            'columns[10][searchable]': 'false',
            'columns[11][data]': 'limit_cli_did_p2p',
            'columns[11][searchable]': 'false',
            'columns[12][data]': 'updated_at',
            'columns[12][searchable]': 'false',
            'columns[13][data]': 'action',
            'columns[13][searchable]': 'false',
            'columns[13][orderable]': 'false',
            'order[0][column]': '1',
            'order[0][dir]': 'desc',
            'start': '0',
            'length': '50',
            'search[value]': testNumber,
            '_': timestamp
        });

        const searchUrl = `https://www.ivasms.com/portal/numbers/test?${searchParams.toString()}`;

        const searchResponse = await fetch(searchUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            },
            credentials: 'include'
        });

        if (!searchResponse.ok) {
            return { success: false, error: `Search failed (${searchResponse.status})` };
        }

        const contentType = searchResponse.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            return { success: false, error: 'Server returned non-JSON response. Are you logged in?' };
        }

        const searchData = await searchResponse.json();

        if (!searchData.data || searchData.data.length === 0) {
            return { success: false, error: 'Number not found in any range' };
        }

        // Get the first match
        const rangeId = searchData.data[0].id;
        const rangeName = searchData.data[0].range;

        // Step 2: Add the number
        const addResponse = await fetch('https://www.ivasms.com/portal/numbers/termination/number/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            },
            credentials: 'include',
            body: `_token=${encodeURIComponent(token)}&id=${rangeId}`
        });

        if (!addResponse.ok) {
            return { success: false, error: `Add failed (${addResponse.status})` };
        }

        const addData = await addResponse.json();

        return {
            success: true,
            range: rangeName,
            message: addData.message
        };

    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Return Numbers background processing function
async function startBackgroundReturning(ids) {
    if (processingState.isRunning) {
        return;
    }

    processingState = {
        isRunning: true,
        shouldStop: false,
        currentIndex: 0,
        numbers: ids,
        results: [],
        delay: 0
    };

    chrome.action.setBadgeText({ text: '...' });
    chrome.action.setBadgeBackgroundColor({ color: '#fc8181' });

    addResult('info', `Returning ${ids.length} selected number(s)...`);

    try {
        const tabs = await chrome.tabs.query({ url: 'https://www.ivasms.com/*' });

        if (tabs.length === 0) {
            addResult('error', `No IVASMS tab found.`);
            processingState.isRunning = false;
            chrome.action.setBadgeText({ text: '' });
            return;
        }

        const result = await chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            func: returnAllSelectedNumbers
        });

        if (result[0].result.success) {
            addResult('success', `✓ Successfully returned ${result[0].result.count} numbers`);
            addResult('info', result[0].result.message);
        } else {
            addResult('error', `✗ Failed: ${result[0].result.error}`);
        }
    } catch (error) {
        addResult('error', `✗ Error: ${error.message}`);
    }

    addResult('info', `📊 Return operation complete!`);

    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon128.png',
        title: 'IVASMS Return Numbers - Complete!',
        message: `Return operation completed`,
        priority: 2
    });

    processingState.isRunning = false;
    chrome.action.setBadgeText({ text: '' });
}

// This function runs in the page context - uses the simple "return all" API
async function returnAllSelectedNumbers() {
    try {
        const response = await fetch('https://www.ivasms.com/portal/numbers/return/allnumber/bluck', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'include',
            body: null
        });

        if (!response.ok) {
            return { success: false, error: `Request failed (${response.status})` };
        }

        const data = await response.json();

        if (data.count) {
            return {
                success: true,
                count: data.count,
                message: data.message || `Returned ${data.count} numbers`
            };
        } else {
            return { success: false, error: 'No numbers returned' };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
}


// ============ MESSAGE COLLECTION IN BACKGROUND ============

async function startMessageCollection(startDate, endDate, tabId) {
    console.log('[Background] Starting message collection');

    // Update state
    await chrome.storage.local.set({
        messageCollectionState: {
            status: 'running',
            progress: 0,
            currentRange: 0,
            totalRanges: 0,
            messagesCollected: 0,
            startDate: startDate,
            endDate: endDate
        }
    });

    try {
        // Inject and run the collector script
        await chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ['message-collector.js']
        });

        // Start collection
        const results = await chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: (start, end) => window.collectMessagesHybrid(start, end),
            args: [startDate, endDate]
        });

        if (results && results[0] && results[0].result) {
            const messages = results[0].result;

            // Save to history
            const historyEntry = {
                id: Date.now(),
                startDate: startDate,
                endDate: endDate,
                collectedAt: new Date().toISOString(),
                messageCount: messages.length,
                messages: messages
            };

            // Get existing history
            const storage = await chrome.storage.local.get(['messageHistory']);
            const history = storage.messageHistory || [];
            history.unshift(historyEntry);  // Add to beginning

            // Keep only last 10 collections
            if (history.length > 10) history.splice(10);

            await chrome.storage.local.set({
                messageHistory: history,
                messageCollectionState: {
                    status: 'complete',
                    messagesCollected: messages.length
                }
            });

            // Show notification
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icon.png',
                title: 'Message Collection Complete!',
                message: `Collected ${messages.length} messages from ${startDate} to ${endDate}`,
                priority: 2
            });

            console.log(`[Background] Collection complete: ${messages.length} messages`);
        }

    } catch (error) {
        console.error('[Background] Collection error:', error);
        await chrome.storage.local.set({
            messageCollectionState: {
                status: 'error',
                error: error.message
            }
        });
    }
}
