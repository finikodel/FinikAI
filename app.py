from flask import Flask, render_template, request, jsonify, send_from_directory
import g4f
import os

app = Flask(__name__)

# 1. МАРШРУТ ДЛЯ АВАТАРКИ (ico.jpg)
@app.route('/avatar')
def get_avatar():
    # Ищем файл ico.jpg в корневой папке проекта
    return send_from_directory(app.root_path, 'ico.jpg')

# 2. МАРШРУТ ДЛЯ ИКОНОК РОЛЕЙ
@app.route('/icons/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'icons'), filename)

# 3. ГЛАВНАЯ СТРАНИЦА
@app.route('/')
def index():
    return render_template('index.html')

# 4. ЛОГИКА ОБРАБОТКИ ЗАПРОСОВ
@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.json
    user_input = user_data.get("message")
    lang = user_data.get("lang", "ru")
    role = user_data.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    # --- НАСТРОЙКА РОЛЕЙ (Краткость + Характер) ---
    # Мы добавляем требование "BE VERY BRIEF" для скорости и стиля
    prompts = {
        "finik": f"You are FinikAI. Answer strictly in {lang}. Be charismatic, witty, use irony/dark humor like 4chan/Reddit. BE CONCISE.",
        "pomni": f"You are Pomni. Answer in {lang}. BE VERY BRIEF. You are anxious, paranoid, and confused. Use short, shaky sentences.",
        "jax": f"You are Jax. Answer in {lang}. BE VERY BRIEF. You are a cynical prankster, mean-spirited but funny. Short insults only.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. BE VERY BRIEF. Extremely energetic and happy. Short 'I'm ready!' style.",
        "patrick": f"You are Patrick Star. Answer in {lang}. BE VERY BRIEF. Extremely slow and confused. Use 3-5 words maximum."
    }

    system_prompt = prompts.get(role, prompts["finik"])

    try:
        # Пытаемся получить ответ через быстрый Blackbox
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            provider=g4f.Provider.Blackbox,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            timeout=10 # Ограничиваем время ожидания для скорости
        )
        
        if not response:
            raise Exception("Empty")

        return jsonify({"answer": response})

    except Exception:
        # Авто-фоллбэк на любого рабочего провайдера, если первый упал
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            return jsonify({"answer": response})
        except Exception as final_e:
            # Локализованные ошибки
            err_msgs = {
                "ru": "Ошибка связи. Проверь интернет или VPN.",
                "en": "Connection error. Check internet or VPN.",
                "uz": "Aloqa xatosi. Internet yoki VPN-ni tekshiring.",
                "kk": "Байланыс қатесі. Интернетті немесе VPN-ді тексеріңіз.",
                "be": "Памылка сувязі. Праверце інтэрнэт ці VPN."
            }
            return jsonify({"answer": err_msgs.get(lang, err_msgs["ru"])})

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True)