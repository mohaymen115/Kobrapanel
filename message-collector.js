/**
 * iVASMS Message Collector - Hybrid DOM + API Approach
 * Uses DOM clicking for speed, API fallback for errors
 * Developed for IVASMS Auto Range Add Extension
 */

// Only run if not already loaded
if (!window.IVASMS_COLLECTOR_LOADED) {
    window.IVASMS_COLLECTOR_LOADED = true;

    // Utility: Wait for condition with timeout
    const waitFor = async (conditionFn, timeout = 5000, interval = 100) => {
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
            if (conditionFn()) return true;
            await new Promise(r => setTimeout(r, interval));
        }
        return false;
    };

    // Update status in loading div
    const updateStatus = (message) => {
        const loadingDiv = document.querySelector('#msg-loading');
        if (loadingDiv && loadingDiv.style.display !== 'none') {
            loadingDiv.innerHTML = `⏳ ${message}`;
        }
    };

    // Convert yyyy-mm-dd to dd-mm-yyyy
    const formatDate = (dateStr) => {
        const [y, m, d] = dateStr.split('-');
        return `${d}-${m}-${y}`;
    };

    // Extract OTP from message text (any type)
    const extractOTP = (text) => {
        // Match any 3-10 digit consecutive number (covers all OTP types)
        const otpRegex = /\b(\d{3,10})\b/g;
        const otpMatches = text.match(otpRegex);
        if (otpMatches) {
            // Prioritize common OTP lengths: 6-digit, 5-digit, 4-digit, then any others
            return otpMatches.find(m => m.length === 6) ||
                otpMatches.find(m => m.length === 5) ||
                otpMatches.find(m => m.length === 4) ||
                otpMatches[0];  // Return first match if no common length found
        }
        return "N/A";
    };

    // API Fallback: Get messages for a specific number using API
    async function getMessagesViaAPI(number, range, startDate, endDate, token) {
        try {
            const smsFormData = new FormData();
            smsFormData.append('_token', token);
            smsFormData.append('start', startDate);
            smsFormData.append('end', endDate);
            smsFormData.append('Number', number);
            smsFormData.append('Range', range);

            const response = await fetch('https://www.ivasms.com/portal/sms/received/getsms/number/sms', {
                method: 'POST',
                body: smsFormData
            });

            const html = await response.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const cards = doc.querySelectorAll('.card.card-body');

            const messages = [];
            cards.forEach(card => {
                const sender = card.querySelector('.col-sm-4')?.textContent.trim() || 'Unknown';
                const content = card.querySelector('.col-9.col-sm-6 p')?.textContent.trim() || '';

                if (content) {
                    messages.push({
                        sender: sender,
                        message: content,
                        number: number,
                        range: range,
                        otp: extractOTP(content),
                        timestamp: new Date().toISOString()
                    });
                }
            });

            return messages;
        } catch (error) {
            console.error(`[API Fallback] Error for ${number}:`, error);
            return [];
        }
    }

    // Process a single number with DOM clicking + API fallback
    async function processNumberHybrid(numClickEl, rangeName, startDate, endDate, token) {
        const phoneNumber = numClickEl.innerText.trim();
        const numberCard = numClickEl.closest('.card.card-body');

        try {
            // Try DOM clicking first
            const existingSms = numberCard ? numberCard.querySelector('.ContentSMS') : null;
            if (!existingSms || existingSms.children.length === 0 || existingSms.style.display === 'none') {
                if (numClickEl.offsetParent !== null) {
                    numClickEl.click();
                }
            }

            // Wait for SMS content
            const contentFound = await waitFor(() => {
                const smsDiv = numberCard ? numberCard.querySelector('.ContentSMS') : null;
                if (!smsDiv || smsDiv.style.display === 'none') return false;

                // Check for error message
                const errorText = smsDiv.innerText;
                if (errorText.includes('Somthing Error')) {
                    return 'error'; // Special marker for error state
                }

                const pText = smsDiv.querySelector('p.mb-0');
                const colText = smsDiv.querySelector('.col-9, .col-sm-6');

                return (pText && pText.innerText.trim().length > 0) ||
                    (colText && colText.innerText.trim().length > 0);
            }, 5000);

            // If we got "Somthing Error", use API fallback
            if (contentFound === 'error') {
                console.log(`[Hybrid] DOM error for ${phoneNumber}, using API fallback`);
                updateStatus(`⚠️ Retrying ${phoneNumber} via API...`);
                return await getMessagesViaAPI(phoneNumber, rangeName, startDate, endDate, token);
            }

            if (!contentFound) {
                console.log(`[Hybrid] No content for ${phoneNumber}, using API fallback`);
                return await getMessagesViaAPI(phoneNumber, rangeName, startDate, endDate, token);
            }

            // Extract from DOM
            const contentSMS = numberCard.querySelector('.ContentSMS');
            const msgParagraph = contentSMS.querySelector('p.mb-0');
            let fullText = "";

            if (msgParagraph) {
                fullText = msgParagraph.innerText.trim();
            } else {
                const col9 = contentSMS.querySelector('.col-9, .col-sm-6');
                if (col9) fullText = col9.innerText.trim();
            }

            if (fullText && fullText.length > 0) {
                const senderEl = contentSMS.querySelector('.col-sm-4');
                const sender = senderEl ? senderEl.innerText.trim() : 'Unknown';

                const extractedOTP = extractOTP(fullText);
                console.log(`[Hybrid] ${phoneNumber}: Found message, OTP: ${extractedOTP}`);

                return [{
                    sender: sender,
                    message: fullText,
                    number: phoneNumber,
                    range: rangeName,
                    otp: extractedOTP,
                    timestamp: new Date().toISOString()
                }];
            } else {
                console.log(`[Hybrid] ${phoneNumber}: Skipped - empty message text`);
            }

            return [];

        } catch (error) {
            console.error(`[Hybrid] Error processing ${phoneNumber}:`, error);
            // Final fallback to API
            return await getMessagesViaAPI(phoneNumber, rangeName, startDate, endDate, token);
        }
    }

    // Main extraction function
    async function collectMessagesHybrid(startDate, endDate) {
        const messages = [];
        let stopRequested = false;

        try {
            console.log(`[Collector] Starting collection for ${startDate} to ${endDate}`);
            updateStatus('Preparing date fields...');

            // The page's datepicker expects yyyy-mm-dd format, not dd-mm-yyyy
            // So we'll keep the dates as-is from the popup
            const formattedStart = startDate;  // Already in yyyy-mm-dd
            const formattedEnd = endDate;  // Already in yyyy-mm-dd

            console.log(`[Collector] Using dates: ${formattedStart} to ${formattedEnd}`);

            // Get CSRF token
            const token = document.querySelector('meta[name="csrf-token"]')?.content ||
                document.querySelector('input[name="_token"]')?.value;

            if (!token) {
                throw new Error('CSRF token not found');
            }

            console.log('[Collector] CSRF token found');

            // Step 1: Fill in dates
            const startDateInput = document.getElementById('start_date');
            const endDateInput = document.getElementById('end_date');

            if (!startDateInput || !endDateInput) {
                throw new Error('Date inputs not found on page');
            }

            console.log('[Collector] Setting dates in input fields');
            startDateInput.value = formattedStart;
            endDateInput.value = formattedEnd;

            updateStatus('Clicking Get SMS button...');

            // Step 2: Click "Get SMS" button
            const getSmsButton = document.querySelector('button[onclick*="GetSMS()"]');
            if (!getSmsButton) {
                throw new Error('Get SMS button not found');
            }

            console.log('[Collector] Clicking Get SMS button');
            getSmsButton.click();

            // Wait for ranges to load
            updateStatus('Waiting for ranges to load...');
            const rangesLoaded = await waitFor(() => {
                const resultDiv = document.getElementById('ResultCDR');
                return resultDiv && !resultDiv.querySelector('p#messageFlash');
            }, 10000);

            if (!rangesLoaded) {
                throw new Error('Ranges failed to load');
            }

            console.log('[Collector] Ranges loaded successfully');

            // Get the total count from CountSMS element
            const countSMSElement = document.getElementById('CountSMS');
            const expectedTotal = countSMSElement ? parseInt(countSMSElement.textContent.trim()) : 0;
            console.log(`[Collector] Expected total messages (from CountSMS): ${expectedTotal}`);

            await new Promise(r => setTimeout(r, 1000));

            // Step 3: Get all ranges
            const ranges = document.querySelectorAll('#ResultCDR .item');
            updateStatus(`Found ${ranges.length} ranges. Expanding...`);

            console.log(`[Collector] Found ${ranges.length} ranges`);

            // Step 4: Expand all ranges
            for (let i = 0; i < ranges.length; i++) {
                if (stopRequested) break;

                const rangeItem = ranges[i];
                const rangeButton = rangeItem.querySelector('.card.card-body.pointer');
                if (!rangeButton) continue;

                const rangeName = rangeButton.innerText.split('\n')[0].trim();
                updateStatus(`Expanding range ${i + 1}/${ranges.length}: ${rangeName}`);

                const contentNumbers = rangeItem.querySelector('.ContentNumbers');
                if (!contentNumbers || contentNumbers.style.display === 'none' || contentNumbers.children.length === 0) {
                    rangeButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    rangeButton.click();
                    await waitFor(() => contentNumbers && contentNumbers.children.length > 0, 5000);
                }

                await new Promise(r => setTimeout(r, 200));
            }

            updateStatus('All ranges expanded. Processing messages...');
            await new Promise(r => setTimeout(r, 1000));

            // Step 5: Extract data using hybrid approach
            for (let i = 0; i < ranges.length; i++) {
                if (stopRequested) break;

                const rangeItem = ranges[i];
                const rangeButton = rangeItem.querySelector('.card.card-body.pointer');
                if (!rangeButton) continue;

                const rangeName = rangeButton.innerText.split('\n')[0].trim();
                const contentNumbers = rangeItem.querySelector('.ContentNumbers');
                if (!contentNumbers) continue;

                const numberClickTargets = Array.from(contentNumbers.querySelectorAll('div[onclick*="getDetialsNumber"]'));

                updateStatus(`Range ${i + 1}/${ranges.length} (${rangeName}): ${numberClickTargets.length} numbers`);

                // Process each number with hybrid approach
                for (let j = 0; j < numberClickTargets.length; j++) {
                    if (stopRequested) break;

                    const numClickEl = numberClickTargets[j];
                    const phoneNumber = numClickEl.innerText.trim();

                    updateStatus(`Range ${i + 1}/${ranges.length}: ${phoneNumber} (${j + 1}/${numberClickTargets.length})`);

                    const numberMessages = await processNumberHybrid(
                        numClickEl,
                        rangeName,
                        formattedStart,
                        formattedEnd,
                        token
                    );

                    messages.push(...numberMessages);

                    console.log(`[Collector] ${phoneNumber}: ${numberMessages.length} messages`);

                    // Small delay between numbers
                    await new Promise(r => setTimeout(r, 100));
                }
            }

            updateStatus(`✅ Collection complete! Found ${messages.length} messages.`);
            console.log(`[Collector] Total messages collected: ${messages.length}`);
            if (expectedTotal > 0 && messages.length !== expectedTotal) {
                console.warn(`[Collector] ⚠️ Count mismatch! Expected: ${expectedTotal}, Collected: ${messages.length}, Missing: ${expectedTotal - messages.length}`);
                console.warn(`[Collector] Possible reasons: empty messages, parsing errors, or DOM timing issues`);
            }
            await new Promise(r => setTimeout(r, 500));

        } catch (error) {
            console.error('[Collector] Error:', error);
            updateStatus(`❌ Error: ${error.message}`);
        }

        return messages;
    }

    // Make function available globally
    window.collectMessagesHybrid = collectMessagesHybrid;
    console.log('[Collector] Script loaded successfully');
}
