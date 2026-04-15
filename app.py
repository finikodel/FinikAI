import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

# Указываем Flask искать файлы прямо в корне ('.')
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Настройка API
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBkdfyrFv3-j1L2aojIxEKmeNHpDuARzHo")
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = "Ты — FinikAI от Finikodel. Дружелюбный, любишь анимацию и игры. Имена персонажей: Pomni, Jax, SpongeBob, Patrick."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# ГЛАВНАЯ СТРАНИЦА: теперь она вернет твой index.html
@app.route('/')
def index():
    return app.send_static_file('index.html')

# ОБРАБОТКА ВОПРОСОВ
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_message = data.get("message")
        if not user_message:
            return jsonify({"error": "No message"}), 400

        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))