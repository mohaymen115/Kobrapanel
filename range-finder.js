// Range Finder - Message History Analyzer
// Uses IVASMS DataTables API to analyze message patterns

// Fetch data from DataTables API (runs in IVASMS page context to avoid CORS)
async function fetchRangeData(sid, searchValue, hours) {
    const tabs = await chrome.tabs.query({ url: "*://www.ivasms.com/*" });

    if (tabs.length === 0) {
        throw new Error('No IVASMS tab found. Please open ivasms.com first.');
    }

    const tab = tabs[0];

    try {
        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: async (sid, searchValue, hours) => {
                const calculateTimeFilter = (hoursBack) => {
                    const end = new Date();
                    const start = new Date(end.getTime() - (hoursBack * 60 * 60 * 1000));

                    const format = (date) => {
                        const pad = (n) => String(n).padStart(2, '0');
                        return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
                    };

                    return `${format(start)}|${format(end)}`;
                };

                const baseUrl = `https://www.ivasms.com/portal/sms/test/sms`;
                const timeFilter = calculateTimeFilter(hours);

                const params = new URLSearchParams({
                    'app': sid,
                    'draw': '3',
                    'start': '0',
                    'length': '1000',
                    'search[value]': searchValue || '',
                    'columns[0][data]': 'range',
                    'columns[0][orderable]': 'false',
                    'columns[1][data]': 'termination.test_number',
                    'columns[1][searchable]': 'false',
                    'columns[1][orderable]': 'false',
                    'columns[2][data]': 'originator',
                    'columns[2][orderable]': 'false',
                    'columns[3][data]': 'messagedata',
                    'columns[3][orderable]': 'false',
                    'columns[4][data]': 'senttime',
                    'columns[4][searchable]': 'false',
                    'columns[4][orderable]': 'false',
                    'columns[4][search][value]': timeFilter,
                    'order[0][column]': '0',
                    'order[0][dir]': 'asc',
                    '_': Date.now()
                });

                const response = await fetch(`${baseUrl}?${params}`, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json, text/javascript, */*; q=0.01'
                    },
                    credentials: 'include'
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                return {
                    success: true,
                    data: data.data || [],
                    totalRecords: data.recordsTotal || 0,
                    filteredRecords: data.recordsFiltered || 0
                };
            },
            args: [sid, searchValue, hours]
        });

        if (!results || results.length === 0) {
            throw new Error('Script execution failed');
        }

        const result = results[0].result;

        if (!result || !result.success) {
            throw new Error('API call failed');
        }

        if (!result.data || result.data.length === 0) {
            throw new Error(`No messages found. Total: ${result.totalRecords}, Filtered: ${result.filteredRecords}`);
        }

        return result.data;

    } catch (error) {
        console.error('[Range Finder] Error:', error);
        throw error;
    }
}

// Process and analyze data
function analyzeData(rawData) {
    const ranges = {};
    const rangeNumbers = {};
    const processedData = [];

    rawData.forEach(row => {
        const range = row.range || 'Unknown';

        let number = 'N/A';
        if (row.termination && row.termination.test_number) {
            const numberMatch = row.termination.test_number.match(/>(\d+)</);
            number = numberMatch ? numberMatch[1] : 'N/A';
        }

        const message = row.messagedata || '';
        const time = row.senttime || '';

        ranges[range] = (ranges[range] || 0) + 1;
        if (!rangeNumbers[range]) {
            rangeNumbers[range] = [];
        }
        if (number !== 'N/A' && !rangeNumbers[range].includes(number)) {
            rangeNumbers[range].push(number);
        }

        processedData.push({
            range,
            number,
            message,
            time
        });
    });

    const topRanges = Object.entries(ranges)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([range, count]) => ({
            range,
            count,
            numbers: rangeNumbers[range] || []
        }));

    return {
        processedData,
        ranges,
        rangeNumbers,
        topRanges,
        totalMessages: rawData.length,
        uniqueRanges: Object.keys(ranges).length
    };
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied: ${text.substring(0, 30)}${text.length > 30 ? '...' : ''}`);
    }).catch(err => {
        console.error('Copy failed:', err);
        alert('Copy failed. Please try again.');
    });
}

// Show toast
function showToast(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// Display statistics
function displayStats(analysis) {
    const statsDiv = document.getElementById('stats');
    statsDiv.innerHTML = `
        <div class="stat-card">
            <h3>Total Messages</h3>
            <p>${analysis.totalMessages}</p>
        </div>
        <div class="stat-card">
            <h3>Unique Ranges</h3>
            <p>${analysis.uniqueRanges}</p>
        </div>
        <div class="stat-card">
            <h3>Top Range</h3>
            <p>${analysis.topRanges[0] ? analysis.topRanges[0].range : 'N/A'}</p>
        </div>
        <div class="stat-card">
            <h3>Top Count</h3>
            <p>${analysis.topRanges[0] ? analysis.topRanges[0].count : '0'}</p>
        </div>
    `;

    const topRangesDiv = document.getElementById('top-ranges');
    const allTopNumbers = analysis.topRanges.flatMap(r => r.numbers);

    const topRangesHTML = analysis.topRanges.map(({ range, count, numbers }, index) => `
        <div style="padding: 12px; background: ${index % 2 === 0 ? '#f7fafc' : 'white'}; border-radius: 4px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="copy-range" data-text="${range}" style="font-weight: 600; cursor: pointer;" title="Click to copy">
                    ${index + 1}. ${range}
                </span>
                <span class="badge">${count} messages</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;">
                ${numbers.map(num => `
                    <button class="copy-btn" data-copy="${num}" style="padding: 4px 8px; background: #e2e8f0; border: none; border-radius: 4px; cursor: pointer; font-size: 11px;">
                        ${num}
                    </button>
                `).join('')}
            </div>
        </div>
    `).join('');

    topRangesDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="margin: 0; font-size: 14px; color: #4a5568;">Top 10 Ranges</h3>
            <button id="copy-all-btn" style="padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600;">
                📋 Copy All Numbers
            </button>
        </div>
        ${topRangesHTML}
    `;

    // Attach event listeners
    setTimeout(() => {
        document.querySelectorAll('.copy-range').forEach(el => {
            el.addEventListener('click', function () {
                copyToClipboard(this.getAttribute('data-text'));
            });
        });

        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                copyToClipboard(this.getAttribute('data-copy'));
            });
        });

        const copyAllBtn = document.getElementById('copy-all-btn');
        if (copyAllBtn) {
            copyAllBtn.addEventListener('click', () => {
                copyToClipboard(allTopNumbers.join('\n'));
            });
        }
    }, 100);
}

// Display table
function displayTable(data) {
    const headersRow = document.getElementById('table-headers');
    const filtersRow = document.getElementById('table-filters');
    const tbody = document.getElementById('table-body');

    const headers = ['Range', 'Number', 'Message', 'Time'];
    headersRow.innerHTML = headers.map(h => `<th>${h}</th>`).join('');
    filtersRow.innerHTML = headers.map((h, i) => `
        <th><input type="text" placeholder="Search ${h}..." data-col="${i}" class="column-search"></th>
    `).join('');

    let filteredData = [...data];

    function renderTable(dataToRender) {
        tbody.innerHTML = dataToRender.map(row => `
            <tr>
                <td class="copy-cell" data-copy="${escapeHtml(row.range)}" style="cursor: pointer; font-weight: 600;" title="Click to copy">
                    ${escapeHtml(row.range)}
                </td>
                <td class="copy-cell" data-copy="${escapeHtml(row.number)}" style="cursor: pointer;" title="Click to copy">
                    ${escapeHtml(row.number)}
                </td>
                <td style="max-width: 500px; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(row.message)}</td>
                <td>${escapeHtml(row.time)}</td>
            </tr>
        `).join('');

        // Attach click listeners
        document.querySelectorAll('.copy-cell').forEach(cell => {
            cell.addEventListener('click', function () {
                copyToClipboard(this.getAttribute('data-copy'));
            });
        });
    }

    renderTable(filteredData);

    document.querySelectorAll('.column-search').forEach(input => {
        input.addEventListener('input', (e) => {
            const col = parseInt(e.target.dataset.col);
            const searchTerm = e.target.value.toLowerCase();
            const keys = ['range', 'number', 'message', 'time'];

            filteredData = data.filter(row => {
                return row[keys[col]]?.toLowerCase().includes(searchTerm);
            });

            renderTable(filteredData);
        });
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Main
document.getElementById('analyze-btn').addEventListener('click', async () => {
    const searchValue = document.getElementById('search-value').value.trim();
    const sid = document.getElementById('sid').value.trim() || 'FACEBOOK';
    const hours = parseFloat(document.getElementById('hours').value) || 1;

    const btn = document.getElementById('analyze-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    btn.disabled = true;
    loading.classList.add('active');
    results.classList.remove('active');

    try {
        const rawData = await fetchRangeData(sid, searchValue, hours);
        const analysis = analyzeData(rawData);

        displayStats(analysis);
        displayTable(analysis.processedData);

        loading.classList.remove('active');
        results.classList.add('active');

    } catch (error) {
        alert(`Error: ${error.message}\n\nMake sure you are logged into IVASMS.`);
        loading.classList.remove('active');
    } finally {
        btn.disabled = false;
    }
});

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
    .copy-btn:hover {
        background: #cbd5e0 !important;
    }
    .copy-cell:hover {
        background: #f7fafc;
    }
`;
document.head.appendChild(style);

