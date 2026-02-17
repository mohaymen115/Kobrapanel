// ============ BULK RETURN AUTO-CLICKER ============
// Adapted from GIFT extension - Developed by Siam (@SiamDeveloper1)

const sleep = (ms) => new Promise(res => setTimeout(res, ms));

function getCount() { return Number(sessionStorage.getItem('brac_count') || '0'); }
function setCount(n) { sessionStorage.setItem('brac_count', String(n)); }
function setActive(flag) { sessionStorage.setItem('brac_active', flag ? '1' : '0'); }
function isActive() { return sessionStorage.getItem('brac_active') === '1'; }
function setTotal(n) { sessionStorage.setItem('brac_total', String(n)); }
function getTotal() { return Number(sessionStorage.getItem('brac_total') || '7'); }

function anyDialogContainer() {
    return (
        document.querySelector('.swal2-container, .modal.show, .modal.in, .swal2-popup, .swal2-actions') ||
        document.querySelector('[role="dialog"], [aria-modal="true"]')
    );
}

async function waitFor(target, { timeout = 15000, interval = 120 } = {}) {
    const isFn = typeof target === 'function';
    const start = Date.now();
    while (Date.now() - start < timeout) {
        try {
            let found = isFn ? target() : document.querySelector(target);
            if (found) return found;
        } catch { }
        await sleep(interval);
    }
    return null;
}

async function triggerBulkReturn() {
    const header = document.querySelector('.card-header.text-right');
    if (!header) throw new Error('Container not found.');
    const nodes = [...header.querySelectorAll('#BluckButton')];
    const visibleEnabled = nodes.filter(el => {
        const cs = getComputedStyle(el);
        const notHidden = cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
        const inLayout = el.offsetParent !== null || cs.position === 'fixed';
        const notDisabled = !el.hasAttribute('disabled') && !el.classList.contains('disabled');
        return notHidden && inLayout && notDisabled;
    });
    if (visibleEnabled.length < 2) {
        if (nodes.length >= 2 && nodes[1]) {
            nodes[1].scrollIntoView({ block: 'center', inline: 'center' });
            nodes[1].click();
            try { if (typeof window.BluckReturnAllNumbers === 'function') window.BluckReturnAllNumbers(); } catch { }
            return true;
        }
        throw new Error('Button not found.');
    }
    const byText = visibleEnabled.find(el => /bulk\s*return\s*all\s*numbers/i.test(el.textContent || ''));
    const btn = byText || visibleEnabled[1];
    if (!btn) throw new Error('Button not found.');
    btn.scrollIntoView({ block: 'center', inline: 'center' });
    btn.click();
    try { if (typeof window.BluckReturnAllNumbers === 'function') window.BluckReturnAllNumbers(); } catch { }
    return true;
}

async function confirmYesReturn() {
    const normalize = s => (s || '').replace(/\s+/g, ' ').trim();
    const waitForDialog = async (timeout = 15000) => {
        const start = Date.now();
        while (Date.now() - start < timeout) {
            if (anyDialogContainer()) return true;
            await sleep(120);
        }
        return false;
    };
    await waitForDialog();
    for (let i = 0; i < 8; i++) {
        const all = [...document.querySelectorAll('button, [role="button"], .btn')];
        let btn = all.find(el => /^\s*yes[, ]*\s*return\s*$/i.test(normalize(el.textContent)));
        if (!btn) btn = document.querySelector('.swal2-confirm, .swal2-styled.swal2-confirm, .swal2-actions .swal2-confirm');
        if (!btn) btn = document.querySelector('[data-confirm], [data-yes], [aria-label="Yes, Return"], [aria-label="Yes"]');
        if (btn) {
            btn.scrollIntoView({ block: 'center', inline: 'center' });
            btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
            await sleep(120);
            return;
        }
        await sleep(250);
    }
    throw new Error('Confirm button not found.');
}

async function runOnce() {
    await triggerBulkReturn();
    await sleep(500);
    await confirmYesReturn();
    await sleep(1000);
}

async function runController() {
    let count = getCount();
    const total = getTotal();
    if (!isActive()) return;
    try {
        await runOnce();
        count += 1;
        setCount(count);
        if (count < total) {
            location.reload();
        } else {
            setActive(false);
            alert(`Automation finished: ${total} iterations completed | Dev: Siam (@SiamDeveloper1)`);
        }
    } catch (err) {
        setActive(false);
        console.warn('Error:', err);
        alert('Automation stopped: ' + err.message);
    }
}

(async function resumeIfNeeded() {
    if (isActive()) {
        await sleep(700);
        runController();
    }
})();

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    if (msg?.type === 'START_AUTOMATION') {
        setTotal(Number(msg.total) || 7);
        setCount(0);
        setActive(true);
        runController();
        sendResponse({ ok: true });
    } else if (msg?.type === 'STOP_AUTOMATION') {
        setActive(false);
        sendResponse({ ok: true });
    }
});
