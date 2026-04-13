// script.js Полностью заменить код

// 1. СЛОВАРЬ ПЕРЕВОДА ИНТЕРФЕЙСА
const translations = {
    ru: {
        welcome: "Привет! Я FinikAI. Готов поболтать или пошутить (в стиле 4chan/Reddit). Выбирай язык и роль в панели слева!",
        newChat: "+ Новый чат",
        roles: "Ролевые разговоры:",
        btnSend: "Отправить",
        loading: "FinikAI думает...",
        placeholder: "Спроси у FinikAI...",
        history: "История:",
        langLabel: "Язык:"
    },
    en: {
        welcome: "Hello! I am FinikAI. Ready to chat or joke around (4chan/Reddit style). Choose your language and role in the left panel!",
        newChat: "+ New Chat",
        roles: "Roleplay Chats:",
        btnSend: "Send",
        loading: "FinikAI is thinking...",
        placeholder: "Ask FinikAI...",
        history: "History:",
        langLabel: "Language:"
    },
    uz: {
        welcome: "Salom! Men FinikAI-man. Gaplashishga yoki hazillashishga (4chan/Reddit stilida) tayyorman. Tilni va rolni chap paneldan tanlang!",
        newChat: "+ Yangi chat",
        roles: "Rolli suhbatlar:",
        btnSend: "Yuborish",
        loading: "FinikAI o'ylamoqda...",
        placeholder: "FinikAI'dan so'rang...",
        history: "Tarix:",
        langLabel: "Til:"
    },
    kk: {
        welcome: "Сәлем! Мен FinikAI-мын. Мен сөйлесуге немесе әзілдесуге (4chan/Reddit стилінде) дайынмын. Тілді және рөлді сол жақ панельден таңдаңыз!",
        newChat: "+ Жаңа чат",
        roles: "Рөлдік әңгімелер:",
        btnSend: "Жіберу",
        loading: "FinikAI ойлануда...",
        placeholder: "FinikAI-дан сұраңыз...",
        history: "Тарихы:",
        langLabel: "Тіл:"
    },
    be: {
        welcome: "Прывітанне! Я FinikAI. Гатовы паразмаўляць або пажартаваць (у стылі 4chan/Reddit). Выбірайце мову і ролю ў панэлі злева!",
        newChat: "+ Новы чат",
        roles: "Ролевыя размовы:",
        btnSend: "Адправіць",
        loading: "FinikAI думае...",
        placeholder: "Спытайце ў FinikAI...",
        history: "Гісторыя:",
        langLabel: "Мова:"
    }
};

let currentLang = 'ru';
let currentRole = 'finik'; // По умолчанию - харизматичный Finik

// 2. ФУНКЦИЯ ПЕРЕВОДА ИНТЕРФЕЙСА
function changeLanguage() {
    currentLang = document.getElementById('lang-select').value;
    const t = translations[currentLang] || translations.ru;
    
    // Перевод заголовков и кнопок
    document.getElementById('new-chat').innerText = t.newChat;
    document.getElementById('label-roles').innerText = t.roles;
    document.getElementById('label-lang').innerText = t.langLabel;
    
    // Перевод в окне чата (только приветствие)
    const welcomeMsg = document.getElementById('welcome-msg');
    if (welcomeMsg) welcomeMsg.innerText = t.welcome;
    
    // Перевод ввода
    document.getElementById('send-btn').innerText = t.btnSend;
    document.getElementById('loading-text').innerText = t.loading;
    document.getElementById('user-query').placeholder = t.placeholder;
}

// 3. ВЫБОР РОЛИ
function setRole(roleName) {
    currentRole = roleName;
    
    // Подсветка активной роли в UI
    document.querySelectorAll('.role-btn').forEach(btn => btn.classList.remove('active'));
    if (roleName !== 'finik') {
        const activeBtn = document.querySelector(`.role-btn[title="${roleName.charAt(0).toUpperCase() + roleName.slice(1)}"]`);
        if (activeBtn) activeBtn.classList.add('active');
    }

    // Очистка чата при смене роли
    const messages = document.getElementById('messages');
    messages.innerHTML = `<div class="message ai" id="welcome-msg">${translations[currentLang].welcome}</div>`;
    
    // Изменение приветствия в зависимости от роли (по желанию можно добавить разные стартовые фразы)
}

// 4. ЛОГИКА ОТПРАВКИ
async function sendMessage() {
    const input = document.getElementById('user-query');
    const query = input.value;
    const loader = document.getElementById('loader');
    
    if (!query) return;

    // UI: добавить сообщение юзера, показать лоадер, очистить ввод
    appendMessage('user', query);
    loader.style.display = 'flex';
    input.value = '';

    try {
        // Запрос к серверу
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: query, 
                lang: currentLang, 
                role: currentRole 
            })
        });

        const data = await response.json();
        // UI: спрятать лоадер, добавить ответ ИИ
        loader.style.display = 'none';
        appendMessage('ai', data.answer);
    } catch (e) {
        loader.style.display = 'none';
        appendMessage('ai', `Ошибка: ${e}`);
    }
}

function appendMessage(role, text) {
    const messages = document.getElementById('messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    msgDiv.innerText = text;
    messages.appendChild(msgDiv);
    // Скролл вниз
    messages.scrollTop = messages.scrollHeight;
}
// script.js - Основные функции
let controller; // Для отмены запроса
const tips = [
    "FinikAI может имитировать персонажей — загляни в Роли!",
    "Нажми кнопку-квадратик, чтобы мгновенно остановить ответ.",
    "FinikAI черпает харизму из недр Reddit и 4chan.",
    "В ролевом режиме чаты не сохраняются для приватности."
];

// 1. ПРЕЛОАДЕР И СОВЕТЫ
window.onload = () => {
    let tipIdx = 0;
    const tipElement = document.getElementById('loading-tip');
    const interval = setInterval(() => {
        tipIdx = (tipIdx + 1) % tips.length;
        tipElement.innerText = tips[tipIdx];
    }, 2000);

    // Ускоряем запуск: скрываем лоадер через 3 секунды
    setTimeout(() => {
        clearInterval(interval);
        document.getElementById('preloader').style.display = 'none';
    }, 3000);
};

// 2. ПЕРЕКЛЮЧАТЕЛЬ РОЛЕЙ
function toggleRoles() {
    const container = document.getElementById('roles-container');
    const arrow = document.getElementById('toggle-arrow');
    if (container.style.display === 'none') {
        container.style.display = 'block';
        arrow.style.transform = 'rotate(180deg)';
    } else {
        container.style.display = 'none';
        arrow.style.transform = 'rotate(0deg)';
    }
}

// 3. ОБРАБОТКА КНОПКИ (ОТПРАВКА/СТОП)
function handleAction() {
    const btn = document.getElementById('action-btn');
    if (btn.classList.contains('send-mode')) {
        sendMessage();
    } else {
        stopGeneration();
    }
}

async function sendMessage() {
    const input = document.getElementById('user-query');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';
    
    // Переключаем кнопку в режим СТОП
    const btn = document.getElementById('action-btn');
    btn.classList.remove('send-mode');
    btn.classList.add('stop-mode');

    controller = new AbortController();
    document.getElementById('ai-loading').style.display = 'block';

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, lang: currentLang, role: currentRole }),
            signal: controller.signal
        });
        const data = await response.json();
        document.getElementById('ai-loading').style.display = 'none';
        appendMessage('ai', data.answer);
    } catch (err) {
        document.getElementById('ai-loading').style.display = 'none';
        if (err.name === 'AbortError') {
            appendMessage('ai', 'Запрос остановлен пользователем.');
        }
    } finally {
        resetButton();
    }
}

function stopGeneration() {
    if (controller) controller.abort();
    resetButton();
}

function resetButton() {
    const btn = document.getElementById('action-btn');
    btn.classList.remove('stop-mode');
    btn.classList.add('send-mode');
}

function appendMessage(role, text) {
    const container = document.getElementById('messages');
    const wrap = document.createElement('div');
    wrap.className = role === 'ai' ? 'ai-msg-container' : 'message user';
    
    if (role === 'ai') {
        wrap.innerHTML = `<div class="ai-avatar"></div><div class="message ai">${text}</div>`;
    } else {
        wrap.innerText = text;
    }
    
    container.appendChild(wrap);
    container.scrollTop = container.scrollHeight;
}

function resetChat() {
    document.getElementById('messages').innerHTML = '';
}
function showTab(tab) {
    document.getElementById('chat-tab').style.display = tab === 'chat' ? 'block' : 'none';
    document.getElementById('settings-tab').style.display = tab === 'settings' ? 'block' : 'none';
    document.getElementById('tab-chat-btn').classList.toggle('active', tab === 'chat');
    document.getElementById('tab-set-btn').classList.toggle('active', tab === 'settings');
}
