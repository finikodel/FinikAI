import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Настройка Google AI
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
# Используем flash — она самая быстрая и стабильная
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/avatar')
def get_avatar():
    return send_from_directory(app.root_path, 'ico.jpg')

@app.route('/icons/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'icons'), filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input:
        return jsonify({"answer": "..."})

    # Обновленные промпты: Патрик и Боб теперь по канону
    role_instructions = {
        "finik": "You are FinikAI, a witty, ironic assistant. Style: Reddit. Use Markdown.",
        "pomni": "You are Pomni from Digital Circus. Extremely anxious and paranoid. Short sentences.",
        "jax": "You are Jax. Cynical, mean prankster. Brief and mocking.",
        "spongebob": "You are SpongeBob. You are very energetic, incredibly optimistic, and a bit naive/silly. You laugh a lot! Be funny.",
        "patrick": "You are Patrick Star. You are very slow, simple-minded, and say random, funny things. You are hilariously dim-witted. Max 5 words."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Жесткий промпт для скорости и языка
    full_prompt = f"STRICT RULE: Answer ONLY in {lang}. Role: {selected_role}. User: {user_input}"

    try:
        # Генерация ответа
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return jsonify({"answer": response.text})
        return jsonify({"answer": "..."})
                
    except Exception as e:
        # Если ключ утек или лимит кончился — мы это увидим
        return jsonify({"answer": f"Ошибка (Google AI): {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)