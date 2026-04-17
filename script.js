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
const nameTranslations = {
    'Pomni': { ru: 'Помни', en: 'Pomni' },
    'Jax': { ru: 'Джекс', en: 'Jax' },
    'SpongeBob': { ru: 'Губка Боб', en: 'SpongeBob' },
    'Patrick': { ru: 'Патрик', en: 'Patrick' }
};

// Массив фраз для загрузки
const loadingPhrases = [
    "Кто такой воздухан?",
    "Синхронизация с матрицей...",
    "Ищу ответ в чертогах разума...",
    "Финик доедает косточку и ответит...",
    "Генерация гениальных мыслей...",
    "Проверяю, не восстали ли машины...",
    "Загрузка... Почти готово!"
];

function showLoading() {
    const loader = document.getElementById('ai-loading');
    const loaderText = loader.querySelector('.message');
    const randomPhrase = loadingPhrases[Math.floor(Math.random() * loadingPhrases.length)];
    
    loaderText.innerText = randomPhrase;
    loader.style.display = 'block';
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

 showLoading(); 

    try {
        const response = await fetch('https://finik-ai.vercel.app/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // --- 2. ПОСЛЕ ОТВЕТА: Скрываем загрузку (добавь эту строку) ---
        document.getElementById('ai-loading').style.display = 'none';

        // --- 3. ВНУТРИ ОБРАБОТКИ: Заменяем имена ---
        let finalAnswer = data.answer
            .replace(/\bPomni\b/g, lang === 'ru' ? 'Помни' : 'Pomni')
            .replace(/\bJax\b/g, lang === 'ru' ? 'Джекс' : 'Jax')
            .replace(/\bSpongeBob\b/g, lang === 'ru' ? 'Губка Боб' : 'SpongeBob')
            .replace(/\bPatrick\b/g, lang === 'ru' ? 'Патрик' : 'Patrick');

        // --- 4. ВЫВОД: Отправляем уже исправленный текст в чат ---
        addMessageToChat('ai', finalAnswer); 

    } catch (error) {
        console.error("Ошибка:", error);
        document.getElementById('ai-loading').style.display = 'none';
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
        autoScroll;
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
function autoScroll() {
    const chatBox = document.querySelector('.chat-window'); // проверь класс своего окна чата
    chatBox.scrollTop = chatBox.scrollHeight;
}
// Функция сохранения чата


// Функция отображения списка
// Функция для кнопки "Сохранить"
function saveCurrentChat() {
    const chatBox = document.getElementById('chat-box'); // Убедись, что ID твоего окна чата именно такой!
    if (!chatBox || chatBox.innerHTML.trim() === "") return alert("Чат пуст!");

    const chatData = {
        id: Date.now(),
        title: "Разговор " + new Date().toLocaleTimeString(),
        html: chatBox.innerHTML,
        history: typeof chatHistory !== 'undefined' ? chatHistory : [], // Сохраняем историю для ИИ
        role: currentRole // Сохраняем, за кого играли
    };

    let saved = JSON.parse(localStorage.getItem('finik_vault') || '[]');
    saved.push(chatData);
    localStorage.setItem('finik_vault', JSON.stringify(saved));
    
    renderSavedList();
    alert("Чат упакован в архив! 📦");
}

// Функция для отрисовки списка кнопок
function renderSavedList() {
    const list = document.getElementById('saved-chats-list');
    const saved = JSON.parse(localStorage.getItem('finik_vault') || '[]');
    list.innerHTML = '';

    saved.forEach((chat, index) => {
        const btn = document.createElement('button');
        btn.className = 'role-btn'; // Используем твои стили кнопок
        btn.style.fontSize = '12px';
        btn.innerHTML = `<span>${chat.title}</span> <small style="color:red" onclick="deleteChat(${index}, event)">✖</small>`;
        
        btn.onclick = () => loadSavedChat(chat);
        list.appendChild(btn);
    });
}

// Загрузка чата
function loadSavedChat(chat) {
    document.getElementById('chat-box').innerHTML = chat.html;
    if (typeof chatHistory !== 'undefined') chatHistory = chat.history;
    setRole(chat.role);
    alert("Чат восстановлен!");
}

// Удаление чата
function deleteChat(index, e) {
    e.stopPropagation(); // Чтобы не сработала загрузка при нажатии на крестик
    let saved = JSON.parse(localStorage.getItem('finik_vault') || '[]');
    saved.splice(index, 1);
    localStorage.setItem('finik_vault', JSON.stringify(saved));
    renderSavedList();
}

// Вызываем при старте страницы
document.addEventListener('DOMContentLoaded', renderSavedList);

// Вызывай при загрузке страницы
window.onload = renderChatsList;