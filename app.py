import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Настройка модели 2.5 Pro (актуальная стабильная в 2026)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Отключаем фильтры безопасности, чтобы точки не заменяли ответ
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Вместо gemini-2.5-pro ставим 3.0-flash
model = genai.GenerativeModel(
    model_name='gemini-3.0-flash', 
    safety_settings=safety_settings
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input:
        return jsonify({"answer": "А говорить кто будет?"})

    # Персонажи: Губка Боб и Патрик теперь официально в ударе
    role_instructions = {
        "finik": "Ты — ФиникAI, ироничный ассистент. Стиль: Reddit.",
        "pomni": "Ты — Помни. У тебя паника, ты в Цифровом Цирке. Трясущиеся короткие фразы.",
        "jax": "Ты — Джекс. Циничный кролик-тролль. Короткие издевки.",
        "spongebob": "Ты — Губка Боб! Ты ГИПЕР-энергичный, безумно добрый, но очень глупенький и наивный. Смейся 'А-ха-ха-ха!' в конце каждой фразы.",
        "patrick": "Ты — Патрик Стар. Ты ОЧЕНЬ ТУПОЙ. Твои мысли текут как улитка. Максимум 5 слов. Пиши полную чепуху невпопад."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    full_prompt = f"STRICT: Answer ONLY in {lang}. Role context: {selected_role}. User: {user_input}"

    try:
        response = model.generate_content(full_prompt)
        
        # Если текст есть — возвращаем, если нет — пишем причину, а не точки
        if response.text:
            return jsonify({"answer": response.text})
        else:
            return jsonify({"answer": "Google заблокировал ответ. Попробуй перефразировать!"})
            
    except Exception as e:
        return jsonify({"answer": f"Ошибка (Gemini 2.5): {str(e)}"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/avatar')
def get_avatar():
    return send_from_directory(app.root_path, 'ico.jpg')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)