// Add authentication code at the VERY BEGINNING of popup.js (before const elements)

// ============================================
// AUTHENTICATION SYSTEM
// ============================================

(async function initAuth() {
    const authOverlay = document.getElementById('auth-overlay');
    const authPassword = document.getElementById('auth-password');
    const authSubmit = document.getElementById('auth-submit');
    const authError = document.getElementById('auth-error');
    const authNews = document.getElementById('auth-news');
    const mainContainer = document.getElementById('main-container');

    // Always fetch fresh config first to check expiration
    let config;
    try {
        config = await window.IvasmsAuth.fetchPasswordConfig();
        authNews.textContent = config.text || 'Welcome!';
        console.log('[Auth] Fresh config:', config);

        // Check if expired from FRESH API data
        if (window.IvasmsAuth.isExpired(config.expires)) {
            // Clear any cached auth since it's now expired
            await window.IvasmsAuth.clearAuth();
            authNews.textContent = '⚠️ Extension Expired - Contact Developer for Renewal';
            authNews.style.background = '#f56565';
            authPassword.disabled = true;
            authSubmit.disabled = true;
            mainContainer.classList.add('locked');
            return;
        }
    } catch (error) {
        console.error('[Auth] Config fetch failed:', error);
        authNews.textContent = '⚠️ Could not connect to server';
        authNews.style.background = '#f56565';
    }

    // Now check if already authenticated (stored auth)
    const isAuth = await window.IvasmsAuth.isAuthenticated();

    if (isAuth) {
        // Hide auth overlay and show main content
        authOverlay.classList.add('hidden');
        mainContainer.classList.remove('locked');
        return;
    }

    // Lock main container - need password
    mainContainer.classList.add('locked');

    // Handle password submission
    async function handleSubmit() {
        const password = authPassword.value.trim();

        if (!password) {
            showError('Please enter a password');
            return;
        }

        authSubmit.disabled = true;
        authSubmit.textContent = '🔄 Verifying...';
        authError.style.display = 'none';

        try {
            const result = await window.IvasmsAuth.verifyPassword(password);

            // Store authentication
            await window.IvasmsAuth.storeAuth(result.expires, result.text);

            // Hide overlay with animation
            authOverlay.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                authOverlay.classList.add('hidden');
                mainContainer.classList.remove('locked');
            }, 300);

        } catch (error) {
            if (error.message === 'EXPIRED') {
                showError('⚠️ Extension has expired. Contact developer for renewal.');
                authPassword.disabled = true;
                authSubmit.disabled = true;
            } else {
                showError('❌ Invalid password. Join channel for access.');
            }
            authSubmit.disabled = false;
            authSubmit.textContent = '🔓 Unlock Extension';
        }
    }

    function showError(message) {
        authError.textContent = message;
        authError.style.display = 'block';
    }

    authSubmit.addEventListener('click', handleSubmit);
    authPassword.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    });
})();

// Add fadeOut animation
const authStyle = document.createElement('style');
authStyle.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(authStyle);

// ============================================
// MAIN EXTENSION CODE STARTS HERE
// ============================================

const elements = {
    // Tab elements
    tabBtns: document.querySelectorAll('.tab-btn'),

    // Add Numbers elements
    numbersInput: document.getElementById('numbers-input'),
    startBtn: document.getElementById('start-btn'),
    stopBtn: document.getElementById('stop-btn'),
    delayCheckbox: document.getElementById('delay-checkbox'),
    delayValue: document.getElementById('delay-value'),
    progressSection: document.querySelector('.progress-section'),
    progressBar: document.getElementById('progress-bar'),
    progressText: document.getElementById('progress-text'),
    btnText: document.querySelector('.btn-text'),
    spinner: document.querySelector('.spinner'),

    // SMS Extractor elements
    smsRefreshBtn: document.getElementById('sms-refresh-btn'),
    smsCopyAllBtn: document.getElementById('sms-copy-all'),
    smsLoading: document.getElementById('sms-loading'),
    smsContent: document.getElementById('sms-content'),
    smsEmpty: document.getElementById('sms-empty'),
    smsCount: document.getElementById('sms-count'),
    smsUnique: document.getElementById('sms-unique'),
    smsNumberList: document.getElementById('sms-number-list'),

    // Return automation elements
    returnStartBtn: document.getElementById('return-start-btn'),
    returnStopBtn: document.getElementById('return-stop-btn'),
    returnIterations: document.getElementById('return-iterations'),
    returnStatus: document.getElementById('return-status'),

    // Message Collector elements
    msgCollectBtn: document.getElementById('msg-collect-btn'),
    msgStartDate: document.getElementById('msg-start-date'),
    msgEndDate: document.getElementById('msg-end-date'),
    msgStats: document.getElementById('msg-stats'),
    msgTotal: document.getElementById('msg-total'),
    msgRanges: document.getElementById('msg-ranges'),
    msgLoading: document.getElementById('msg-loading'),
    msgContent: document.getElementById('msg-content'),
    msgList: document.getElementById('msg-list'),
    msgEmpty: document.getElementById('msg-empty'),
    msgCopyAll: document.getElementById('msg-copy-all'),
    msgExportJson: document.getElementById('msg-export-json'),
    msgClearHistory: document.getElementById('msg-clear-history'),

    // Shared elements
    logOutput: document.getElementById('log-output'),
    clearLog: document.getElementById('clear-log')
};

let extractedNumbers = [];

// Tab switching
elements.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Update buttons
        elements.tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Auto-extract SMS when switching to SMS tab
        if (tabName === 'sms-extractor') {
            extractSMSNumbers();
        }

        // Auto-load message history when switching to Messages tab
        if (tabName === 'messages') {
            loadMessageHistory();
        }
    });
});

// Load previous results when popup opens
loadPreviousResults();

// Event listeners - Add Numbers
elements.startBtn.addEventListener('click', startProcessing);
elements.stopBtn.addEventListener('click', stopProcessing);
elements.clearLog.addEventListener('click', clearLog);

// Export All Numbers button
document.getElementById('export-all-numbers').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url.includes('ivasms.com')) {
        chrome.tabs.update(tab.id, { url: 'https://www.ivasms.com/portal/numbers/export' });
    } else {
        chrome.tabs.create({ url: 'https://www.ivasms.com/portal/numbers/export' });
    }
});

// Event listeners - SMS Extractor
elements.smsRefreshBtn.addEventListener('click', extractSMSNumbers);
elements.smsCopyAllBtn.addEventListener('click', copySMSNumbers);

// Event listeners - Return Automation
elements.returnStartBtn.addEventListener('click', startReturnAutomation);
elements.returnStopBtn.addEventListener('click', stopReturnAutomation);

// Listen for updates from background worker
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'logUpdate') {
        addLog(request.result.message, request.result.type);
        // Update summary in real-time
        chrome.storage.local.get(['results'], (data) => {
            if (data.results) {
                updateSummary(data.results);
            }
        });
    }
});

// Poll for state updates while popup is open
setInterval(async () => {
    const response = await chrome.runtime.sendMessage({ action: 'getState' });
    if (response && response.isRunning) {
        updateUIForRunning(response);
        updateProgress(response.currentIndex + 1, response.numbers.length);
    } else {
        updateUIForStopped();
    }
}, 500);

// Load previous results from storage
async function loadPreviousResults() {
    const data = await chrome.storage.local.get(['results']);
    if (data.results && data.results.length > 0) {
        data.results.forEach(result => {
            addLog(result.message, result.type);
        });
        updateSummary(data.results);
    }
}

// Update summary statistics
function updateSummary(results) {
    // Only count actual processing results, not summary messages
    const successful = results.filter(r =>
        r.type === 'success' && (r.message.includes('Added:') || r.message.includes('returned'))
    ).length;

    const failed = results.filter(r =>
        r.type === 'error' && (r.message.includes('Failed:') || r.message.includes('Error:'))
    ).length;

    const total = successful + failed;

    document.getElementById('success-count').textContent = successful;
    document.getElementById('failed-count').textContent = failed;
    document.getElementById('total-count').textContent = total;
}

// Log functions
function addLog(message, type = 'info') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;

    const icons = {
        success: '✓',
        error: '✗',
        info: 'ℹ',
        warning: '⚠'
    };

    entry.innerHTML = `
        <span class="log-icon">${icons[type]}</span>
        <span class="log-message">${message}</span>
    `;

    elements.logOutput.appendChild(entry);
    elements.logOutput.scrollTop = elements.logOutput.scrollHeight;
}

async function clearLog() {
    elements.logOutput.innerHTML = '';
    await chrome.runtime.sendMessage({ action: 'clearResults' });
    // Reset summary
    document.getElementById('success-count').textContent = '0';
    document.getElementById('failed-count').textContent = '0';
    document.getElementById('total-count').textContent = '0';
}

function updateProgress(current, total) {
    const percentage = total > 0 ? (current / total) * 100 : 0;
    elements.progressBar.style.width = `${percentage}%`;
    elements.progressText.textContent = `${current} / ${total} processed`;
}

function updateUIForRunning(state) {
    elements.startBtn.disabled = true;
    elements.btnText.style.display = 'none';
    elements.spinner.style.display = 'block';
    elements.stopBtn.style.display = 'block';
    elements.progressSection.style.display = 'block';
    elements.numbersInput.disabled = true;
}

function updateUIForStopped() {
    elements.startBtn.disabled = false;
    elements.btnText.style.display = 'block';
    elements.spinner.style.display = 'none';
    elements.stopBtn.style.display = 'none';
    elements.numbersInput.disabled = false;
}

// ============ ADD NUMBERS FUNCTIONALITY ============
async function startProcessing() {
    const numbers = elements.numbersInput.value
        .split('\n')
        .map(n => n.trim())
        .filter(n => n.length > 0);

    if (numbers.length === 0) {
        addLog('Please enter at least one test number', 'warning');
        return;
    }

    // Validate we're on IVASMS
    const tabs = await chrome.tabs.query({ url: 'https://www.ivasms.com/*' });
    if (tabs.length === 0) {
        addLog('Please open IVASMS website first!', 'error');
        return;
    }

    // Clear previous results
    await clearLog();

    // UI updates
    updateUIForRunning({ isRunning: true });
    elements.progressSection.style.display = 'block';

    addLog(`Starting to process ${numbers.length} number(s)...`, 'info');
    addLog(`💡 You can close this popup - processing will continue in background!`, 'info');

    const delay = elements.delayCheckbox.checked ? parseInt(elements.delayValue.value) : 0;

    // Send to background worker
    await chrome.runtime.sendMessage({
        action: 'startProcessing',
        numbers: numbers,
        delay: delay
    });
}

async function stopProcessing() {
    await chrome.runtime.sendMessage({ action: 'stopProcessing' });
    addLog('Stopping after current number...', 'warning');
}

// ============ SMS EXTRACTOR FUNCTIONALITY ============
async function extractSMSNumbers() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    elements.smsLoading.style.display = 'block';
    elements.smsContent.style.display = 'none';
    elements.smsEmpty.style.display = 'none';

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: scrapeNumbers
    }, (results) => {
        if (results && results[0] && results[0].result) {
            extractedNumbers = results[0].result;
            displaySMSNumbers(extractedNumbers);
        } else {
            showSMSEmpty();
        }
    });
}

function scrapeNumbers() {
    const numbers = [];
    const rows = document.querySelectorAll('#clientsmshistory-table tbody tr');
    rows.forEach(row => {
        const numberCell = row.querySelectorAll('td')[1];
        if (numberCell) {
            const numberText = numberCell.textContent.trim();
            if (numberText && numberText.match(/^\d+$/)) {
                numbers.push(numberText);
            }
        }
    });
    return numbers;
}

function displaySMSNumbers(numbers) {
    if (numbers.length === 0) {
        showSMSEmpty();
        return;
    }

    elements.smsLoading.style.display = 'none';
    elements.smsContent.style.display = 'block';
    elements.smsEmpty.style.display = 'none';

    const uniqueNumbers = [...new Set(numbers)];
    elements.smsCount.textContent = numbers.length;
    elements.smsUnique.textContent = uniqueNumbers.length;

    elements.smsNumberList.innerHTML = '';
    uniqueNumbers.forEach(number => {
        const item = document.createElement('div');
        item.className = 'number-item';
        item.innerHTML = `<span class="number">${number}</span><button class="copy-btn">Copy</button>`;
        item.querySelector('.copy-btn').addEventListener('click', () => copyNumber(number, item.querySelector('.copy-btn')));
        elements.smsNumberList.appendChild(item);
    });
}

function showSMSEmpty() {
    elements.smsLoading.style.display = 'none';
    elements.smsContent.style.display = 'none';
    elements.smsEmpty.style.display = 'block';
}

function copyNumber(number, btn) {
    navigator.clipboard.writeText(number).then(() => {
        const orig = btn.textContent;
        btn.textContent = '✓';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = orig;
            btn.classList.remove('copied');
        }, 1500);
    });
}

function copySMSNumbers() {
    const uniqueNumbers = [...new Set(extractedNumbers)];
    const allNumbers = uniqueNumbers.join('\n');
    navigator.clipboard.writeText(allNumbers).then(() => {
        const orig = elements.smsCopyAllBtn.textContent;
        elements.smsCopyAllBtn.textContent = '✓ Copied!';
        setTimeout(() => { elements.smsCopyAllBtn.textContent = orig; }, 1500);
    });
}

// ============ RETURN AUTOMATION FUNCTIONALITY ============
async function startReturnAutomation() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const total = Number(elements.returnIterations.value) || 7;
    elements.returnStatus.innerHTML = '<div class="info">Starting automation...</div>';
    await chrome.tabs.sendMessage(tab.id, { type: 'START_AUTOMATION', total }).catch(() => null);
    window.close();
}

async function stopReturnAutomation() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    elements.returnStatus.innerHTML = '<div class="info">Stopping automation...</div>';
    await chrome.tabs.sendMessage(tab.id, { type: 'STOP_AUTOMATION' }).catch(() => null);
    window.close();
}

// Extract SMS on load if on SMS tab
extractSMSNumbers();

// ============ MESSAGE COLLECTOR FUNCTIONALITY (FIXED) ============
let collectedMessages = [];
let exportFormat = 'number-otp'; // Default format

// Set default dates to today
const today = new Date().toISOString().split('T')[0];
if (elements.msgStartDate) elements.msgStartDate.value = today;
if (elements.msgEndDate) elements.msgEndDate.value = today;

// Event listeners
if (elements.msgCollectBtn) {
    elements.msgCollectBtn.addEventListener('click', collectMessages);

    // Clear history button
    if (elements.msgClearHistory) {
        elements.msgClearHistory.addEventListener('click', async () => {
            if (confirm('Are you sure you want to clear all message collection history?')) {
                await chrome.storage.local.set({ messageHistory: [] });
                elements.msgHistorySelector = document.getElementById('msg-history-selector');
                if (elements.msgHistorySelector) {
                    elements.msgHistorySelector.style.display = 'none';
                }
                showMessagesEmpty();
                alert('History cleared successfully!');
            }
        });
    }

}
if (elements.msgCopyAll) {
    elements.msgCopyAll.addEventListener('click', copyAllMessages);
}
if (elements.msgExportJson) {
    elements.msgExportJson.addEventListener('click', exportMessagesJSON);
}

// Range Finder button
const rangeFinderBtn = document.getElementById('open-range-finder');
if (rangeFinderBtn) {
    rangeFinderBtn.addEventListener('click', () => {
        chrome.tabs.create({ url: 'range-finder.html' });
    });
}

// Add format selector listener
const formatSelector = document.getElementById('msg-format');
if (formatSelector) {
    formatSelector.addEventListener('change', (e) => {
        exportFormat = e.target.value;
    });
}

// Convert yyyy-mm-dd to dd-mm-yyyy
function convertDateFormat(dateStr) {
    const [y, m, d] = dateStr.split('-');
    return `${d}-${m}-${y}`;
}

async function collectMessages() {
    const startDate = elements.msgStartDate.value;
    const endDate = elements.msgEndDate.value;

    if (!startDate || !endDate) {
        alert('Please select start and end dates');
        return;
    }

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Get initial count from the page
        const countResults = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                const countEl = document.getElementById('CountSMS');
                return countEl ? countEl.textContent.trim() : '0';
            }
        });

        const totalCount = countResults && countResults[0] ? countResults[0].result : '0';

        // Show loading with initial count
        elements.msgLoading.style.display = 'block';
        elements.msgLoading.innerHTML = `
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #667eea; margin-bottom: 8px;">
                    ${totalCount} SMS Messages Found
                </div>
                <div style="font-size: 14px; color: #718096;" id="collection-status">
                    ⏳ Starting collection process...
                </div>
                <div style="margin-top: 12px; font-size: 12px; color: #a0aec0;">
                    Please wait, collecting messages...
                </div>
            </div>
        `;
        elements.msgContent.style.display = 'none';
        elements.msgEmpty.style.display = 'none';
        elements.msgStats.style.display = 'none';

        collectedMessages = [];

        // Inject the collector script
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['message-collector.js']
        });

        // Start polling for status updates
        const statusInterval = setInterval(async () => {
            const statusResult = await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: () => {
                    const loadingDiv = document.querySelector('#msg-loading');
                    return loadingDiv ? loadingDiv.innerHTML : null;
                }
            }).catch(() => null);

            if (statusResult && statusResult[0] && statusResult[0].result) {
                elements.msgLoading.innerHTML = statusResult[0].result;
            }
        }, 500);

        // Execute collection
        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: (start, end) => window.collectMessagesHybrid(start, end),
            args: [startDate, endDate]
        });

        clearInterval(statusInterval);

        if (results && results[0] && results[0].result) {
            collectedMessages = results[0].result;

            // Save to history
            const historyEntry = {
                id: Date.now(),
                startDate: startDate,
                endDate: endDate,
                collectedAt: new Date().toISOString(),
                messageCount: collectedMessages.length,
                messages: collectedMessages
            };

            chrome.storage.local.get(['messageHistory'], (storage) => {
                const history = storage.messageHistory || [];
                history.unshift(historyEntry);
                if (history.length > 10) history.splice(10);
                chrome.storage.local.set({ messageHistory: history });
            });

            displayMessages(collectedMessages);
        } else {
            showMessagesEmpty();
        }
    } catch (error) {
        console.error('Error collecting messages:', error);
        alert('Error collecting messages. Make sure you are on IVASMS /portal/sms/received page.');
        showMessagesEmpty();
    }
}

// Load message history
async function loadMessageHistory() {
    const history = await chrome.runtime.sendMessage({ action: 'getMessageHistory' });

    if (!history || history.length === 0) {
        showMessagesEmpty();
        return;
    }

    // Load the most recent collection
    const latestCollection = history[0];
    collectedMessages = latestCollection.messages;
    displayMessages(collectedMessages);

    // Show history selector if there are multiple collections
    if (history.length > 1) {
        showHistorySelector(history);
    }
}

// Show history selector
function showHistorySelector(history) {
    const historyEl = document.getElementById('msg-history-selector');
    if (!historyEl) return;

    historyEl.style.display = 'block';
    const selectEl = historyEl.querySelector('select');
    selectEl.innerHTML = '';

    history.forEach((entry, index) => {
        const option = document.createElement('option');
        option.value = index;
        const date = new Date(entry.collectedAt).toLocaleString();
        option.textContent = `${date} (${entry.messageCount} messages)`;
        selectEl.appendChild(option);
    });

    selectEl.addEventListener('change', (e) => {
        const selectedEntry = history[e.target.value];
        collectedMessages = selectedEntry.messages;
        displayMessages(collectedMessages);
    });
}

async function collectMessagesFromAPIWithProgress(startDate, endDate) {
    const messages = [];

    // Helper to update status in the loading div
    const updateStatus = (message) => {
        const loadingDiv = document.querySelector('#msg-loading');
        if (loadingDiv && loadingDiv.style.display !== 'none') {
            loadingDiv.innerHTML = `⏳ ${message}`;
        }
    };

    try {
        // Get CSRF token
        const token = document.querySelector('meta[name="csrf-token"]')?.content ||
            document.querySelector('input[name="_token"]')?.value;

        if (!token) {
            throw new Error('CSRF token not found');
        }

        updateStatus('Fetching ranges...');

        // Step 1: Get all ranges
        const formData = new FormData();
        formData.append('from', startDate);
        formData.append('to', endDate);
        formData.append('_token', token);

        const rangesResponse = await fetch('https://www.ivasms.com/portal/sms/received/getsms', {
            method: 'POST',
            body: formData
        });

        const rangesHTML = await rangesResponse.text();
        const rangesDoc = new DOMParser().parseFromString(rangesHTML, 'text/html');
        const rangeElements = rangesDoc.querySelectorAll('[onclick^="getDetials"]');

        // Extract range names
        const ranges = Array.from(rangeElements).map(el => {
            const onclickValue = el.getAttribute('onclick');
            const match = onclickValue.match(/getDetials\('([^']+)'\)/);
            return match ? match[1] : null;
        }).filter(Boolean);

        console.log(`Found ${ranges.length} ranges`);
        updateStatus(`Found ${ranges.length} ranges. Collecting numbers...`);

        // Step 2: For each range, get numbers
        let rangeIndex = 0;
        for (const range of ranges) {
            rangeIndex++;
            updateStatus(`Processing range ${rangeIndex}/${ranges.length}: ${range}`);

            const numbersFormData = new FormData();
            numbersFormData.append('_token', token);
            numbersFormData.append('start', startDate);
            numbersFormData.append('end', endDate);
            numbersFormData.append('range', range);

            const numbersResponse = await fetch('https://www.ivasms.com/portal/sms/received/getsms/number', {
                method: 'POST',
                body: numbersFormData
            });

            const numbersHTML = await numbersResponse.text();
            const numbersDoc = new DOMParser().parseFromString(numbersHTML, 'text/html');
            const numberElements = numbersDoc.querySelectorAll('[onclick*="getDetialsNumber"]');

            // Extract numbers
            const numbers = Array.from(numberElements).map(el => {
                const onclickValue = el.getAttribute('onclick');
                const match = onclickValue.match(/getDetialsNumber[^']*\('([^']+)'/);
                return match ? match[1] : null;
            }).filter(Boolean);

            console.log(`Range ${range}: Found ${numbers.length} numbers`);

            // Step 3: For each number, get SMS messages
            let numberIndex = 0;
            for (const number of numbers) {
                numberIndex++;
                updateStatus(`Range ${rangeIndex}/${ranges.length} (${range}): Number ${numberIndex}/${numbers.length}`);

                const smsFormData = new FormData();
                smsFormData.append('_token', token);
                smsFormData.append('start', startDate);
                smsFormData.append('end', endDate);
                smsFormData.append('Number', number);
                smsFormData.append('Range', range);

                const smsResponse = await fetch('https://www.ivasms.com/portal/sms/received/getsms/number/sms', {
                    method: 'POST',
                    body: smsFormData
                });

                const smsHTML = await smsResponse.text();
                const smsDoc = new DOMParser().parseFromString(smsHTML, 'text/html');
                const smsCards = smsDoc.querySelectorAll('.card.card-body');

                smsCards.forEach(card => {
                    const sender = card.querySelector('.col-sm-4')?.textContent.trim() || 'Unknown';
                    const content = card.querySelector('.col-9.col-sm-6 p')?.textContent.trim() || '';

                    if (content) {
                        // Extract OTP (prioritize 6-digit, then 4 or 8 digit codes)
                        const otpRegex = /\b(\d{8}|\d{6}|\d{4})\b/g;
                        const matches = content.match(otpRegex);
                        let otp = "N/A";
                        if (matches) {
                            otp = matches.find(m => m.length === 6) || matches[0];
                        }

                        messages.push({
                            sender: sender,
                            message: content,
                            number: number,
                            range: range,
                            otp: otp
                        });
                    }
                });

                // Small delay to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }

        updateStatus(`✅ Collection complete! Found ${messages.length} messages.`);
        await new Promise(resolve => setTimeout(resolve, 500));

    } catch (error) {
        console.error('Error in collectMessagesFromAPIWithProgress:', error);
        updateStatus('❌ Error during collection. Check console.');
    }

    return messages;
}


function displayMessages(messages) {
    if (messages.length === 0) {
        showMessagesEmpty();
        return;
    }

    elements.msgLoading.style.display = 'none';
    elements.msgContent.style.display = 'block';
    elements.msgEmpty.style.display = 'none';
    elements.msgStats.style.display = 'flex';

    // Update stats
    const uniqueNumbers = [...new Set(messages.map(m => m.number))];
    const uniqueRanges = [...new Set(messages.map(m => m.range))];
    const withOTP = messages.filter(m => m.otp !== 'N/A').length;

    elements.msgTotal.textContent = messages.length;
    elements.msgRanges.textContent = uniqueRanges.length + ' ranges';

    // Show range filter
    const rangeFilterEl = document.getElementById('msg-range-filter');
    if (rangeFilterEl) {
        rangeFilterEl.style.display = 'block';
        const rangeList = document.getElementById('msg-range-list');
        rangeList.innerHTML = '';

        uniqueRanges.forEach(range => {
            const count = messages.filter(m => m.range === range).length;
            const item = document.createElement('label');
            item.className = 'range-filter-item';
            item.innerHTML = `
                <input type="checkbox" value="${escapeHtml(range)}" checked>
                <span>${escapeHtml(range)} (${count} msgs)</span>
            `;
            rangeList.appendChild(item);
        });
    }

    // Display messages
    elements.msgList.innerHTML = '';
    messages.forEach((msg, index) => {
        const item = document.createElement('div');
        item.className = 'message-item';
        item.dataset.range = msg.range;

        const otpBadge = msg.otp !== 'N/A'
            ? `<span class="otp-badge">OTP: ${escapeHtml(msg.otp)}</span>`
            : '';

        item.innerHTML = `
            <div class="message-header">
                <span class="message-number">📱 ${escapeHtml(msg.number)}</span>
                ${otpBadge}
            </div>
            <div class="message-range-badge">${escapeHtml(msg.range)}</div>
            <div class="message-content">${escapeHtml(msg.message)}</div>
            <div class="message-footer">
                <button class="message-copy-btn" data-index="${index}">Copy</button>
            </div>
        `;

        item.querySelector('.message-copy-btn').addEventListener('click', (e) => {
            copyMessage(index, e.target);
        });

        elements.msgList.appendChild(item);
    });
}

function showMessagesEmpty() {
    elements.msgLoading.style.display = 'none';
    elements.msgContent.style.display = 'none';
    elements.msgEmpty.style.display = 'block';
    elements.msgStats.style.display = 'none';
}

function copyMessage(index, btn) {
    const msg = collectedMessages[index];
    const text = `Number: ${msg.number}\nOTP: ${msg.otp}\nMessage: ${msg.message}`;

    navigator.clipboard.writeText(text).then(() => {
        const orig = btn.textContent;
        btn.textContent = '✓';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = orig;
            btn.classList.remove('copied');
        }, 1500);
    });
}

function copyAllMessages() {
    const allText = collectedMessages.map(msg =>
        `Number: ${msg.number}\nOTP: ${msg.otp}\nMessage: ${msg.message}\n---`
    ).join('\n\n');

    navigator.clipboard.writeText(allText).then(() => {
        const orig = elements.msgCopyAll.textContent;
        elements.msgCopyAll.textContent = '✓ Copied!';
        setTimeout(() => { elements.msgCopyAll.textContent = orig; }, 1500);
    });
}

function exportMessagesJSON() {
    const dataStr = JSON.stringify(collectedMessages, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ivasms-messages-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

//  Export TXT
function exportMessagesTXT() {
    const selectedRanges = getSelectedRanges();
    const filteredMessages = collectedMessages.filter(m => selectedRanges.includes(m.range));

    let content = '';
    const format = exportFormat;

    filteredMessages.forEach(msg => {
        if (format === 'number-otp') {
            content += `${msg.number}-${msg.otp}\n`;
        } else if (format === 'number-otp-message') {
            content += `${msg.number}-${msg.otp}-${msg.message}\n`;
        }
    });

    const dataBlob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ivasms-export-${new Date().toISOString().split('T')[0]}.txt`;
    link.click();
    URL.revokeObjectURL(url);
}

// Export CSV
function exportMessagesCSV() {
    const selectedRanges = getSelectedRanges();
    const filteredMessages = collectedMessages.filter(m => selectedRanges.includes(m.range));

    const format = exportFormat;
    let content = '';

    if (format === 'number-otp') {
        content = 'Number,OTP\n';
        filteredMessages.forEach(msg => {
            content += `${msg.number},${msg.otp}\n`;
        });
    } else if (format === 'number-otp-message') {
        content = 'Number,OTP,Message\n';
        filteredMessages.forEach(msg => {
            content += `${msg.number},${msg.otp},"${msg.message.replace(/"/g, '""')}"\n`;
        });
    }

    const dataBlob = new Blob([content], { type: 'text/csv' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ivasms-export-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
}

// Get selected ranges from filter
function getSelectedRanges() {
    const rangeList = document.getElementById('msg-range-list');
    if (!rangeList) return collectedMessages.map(m => m.range);

    const checkboxes = rangeList.querySelectorAll('input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

// Copy all - also respect range filter
function copyAllMessages() {
    const selectedRanges = getSelectedRanges();
    const filteredMessages = collectedMessages.filter(m => selectedRanges.includes(m.range));

    const allText = filteredMessages.map(msg =>
        `Number: ${msg.number}\nOTP: ${msg.otp}\nMessage: ${msg.message}\n---`
    ).join('\n\n');

    navigator.clipboard.writeText(allText).then(() => {
        const orig = elements.msgCopyAll.textContent;
        elements.msgCopyAll.textContent = '✓ Copied!';
        setTimeout(() => { elements.msgCopyAll.textContent = orig; }, 1500);
    });
}

// Export JSON - also respect range filter  
function exportMessagesJSON() {
    const selectedRanges = getSelectedRanges();
    const filteredMessages = collectedMessages.filter(m => selectedRanges.includes(m.range));

    const dataStr = JSON.stringify(filteredMessages, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ivasms-messages-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}


// Add missing utility functions and event listeners

// Add event listeners for new export buttons
const msgExportTxt = document.getElementById('msg-export-txt');
const msgExportCsv = document.getElementById('msg-export-csv');

if (msgExportTxt) {
    msgExportTxt.addEventListener('click', exportMessagesTXT);
}
if (msgExportCsv) {
    msgExportCsv.addEventListener('click', exportMessagesCSV);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

