import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# --- НАСТРОЙКА ИИ ---
# Рекомендую на Vercel добавить ключ в Environment Variables под именем GOOGLE_API_KEY
# Но для теста можно оставить так (хотя это небезопасно)
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBkdfyrFv3-j1L2aojIxEKmeNHpDuARzHo")
genai.configure(api_key=API_KEY)

# ТУТ ЗАДАЕТСЯ РОЛЬ (System Instruction)
SYSTEM_PROMPT = """
Ты — FinikAI, продвинутый и дружелюбный ИИ-помощник, созданный разработчиком Finikodel. 
Твой характер: умный, немного ироничный, но всегда готовый помочь. 
Ты любишь тему анимации, веб-разработки (особенно HTML5) и игр.
Важно: Если тебя спрашивают про персонажей, используй такие имена: Pomni, Jax, SpongeBob, Patrick.
Отвечай всегда на том языке, на котором к тебе обратились.
"""

# Инициализация модели с ролью
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

@app.route('/')
def index():
    return "FinikAI Server is Running!"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_message = data.get("message")
        chat_history = data.get("history", []) # Если захочешь добавить память чата позже

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Генерация ответа с учетом роли
        # Мы используем start_chat для возможности ведения диалога в будущем
        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        
        return jsonify({
            "answer": response.text,
            "status": "success"
        })

    except Exception as e:
        print(f"Ошибка сервера: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # На Vercel порт выбирается автоматически
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)