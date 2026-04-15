import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Используем стабильную модель 2026 года
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input: return jsonify({"answer": "..."})

    # Улучшенные каноничные роли
    role_instructions = {
        "finik": "Ты — ФиникAI, остроумный и ироничный ассистент. Стиль: Reddit.",
        "pomni": "Ты — Помни. У тебя паническая атака, ты в ужасе. Короткие фразы.",
        "jax": "Ты — Джекс. Циничный шутник, обожаешь подкалывать. Кратко и зло.",
        "spongebob": "Ты — Губка Боб Квадратные Штаны! Ты ГИПЕР-энергичный, безумно оптимистичный и очень наивный/глупенький. Ты постоянно смеешься 'А-ха-ха-ха!'.",
        "patrick": "Ты — Патрик Стар. Ты ОЧЕНЬ тупой. Ты медленно соображаешь и говоришь невпопад. МАКСИМУМ 5 СЛОВ в ответе. Пиши чепуху."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Инструкция для ИИ
    full_prompt = f"STRICT: Answer ONLY in {lang}. Role context: {selected_role}. User query: {user_input}"

    try:
        response = model.generate_content(full_prompt)
        return jsonify({"answer": response.text if response.text else "..."})
    except Exception as e:
        # Если API выдаст ошибку, мы увидим её в чате
        return jsonify({"answer": f"Ошибка (Gemini 2.5): {str(e)}"})

@app.route('/')
def index(): return render_template('index.html')

@app.route('/avatar')
def get_avatar(): return send_from_directory(app.root_path, 'ico.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))