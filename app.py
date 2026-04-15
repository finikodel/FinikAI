import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Используем 1.0-pro, она не выдает 404
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.0-pro')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input: return jsonify({"answer": "..."})

    # Персонажи по твоей просьбе
    role_instructions = {
        "finik": "You are FinikAI, a witty assistant. Style: Reddit.",
        "pomni": "You are Pomni. Extremely anxious and paranoid.",
        "jax": "You are Jax. Cynical, mean prankster.",
        "spongebob": "Ты — Губка Боб. Ты очень энергичный, добрый, но немножко глупенький и наивный. Ты постоянно смеешься! Отвечай весело и просто.",
        "patrick": "Ты — Патрик Стар. Ты ОЧЕНЬ тупой и смешной. Твои мысли путаются. Максимум 5 слов в ответе. Говори глупости."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    full_prompt = f"Answer ONLY in {lang}. Role: {selected_role}. User: {user_input}"

    try:
        response = model.generate_content(full_prompt)
        return jsonify({"answer": response.text if response.text else "..."})
    except Exception as e:
        return jsonify({"answer": f"Ошибка: {str(e)}"})

@app.route('/')
def index(): return render_template('index.html')

@app.route('/avatar')
def get_avatar(): return send_from_directory(app.root_path, 'ico.PNG')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))