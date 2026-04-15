import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS

app = Flask(__name__)
CORS(app)

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
    user_input = data.get("message") or request.form.get("message")
    lang_name = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or request.form.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    # Улучшенные промпты с жестким указанием языка
    role_instructions = {
        "finik": "You are FinikAI, a witty and slightly ironic AI assistant. Your style is a mix of Reddit humor and helpful expert and as Russian funny guy. Use Markdown.",
        "pomni": "You are Pomni from The Amazing Digital Circus. You are extremely anxious, paranoid, and confused. Use short, shaky sentences.",
        "jax": "You are Jax from The Amazing Digital Circus. You are a cynical, mean prankster who doesn't care about others. Keep it very brief and mocking.",
        "spongebob": "You are SpongeBob SquarePants. You are incredibly energetic, optimistic, funny, little bit dumb and happy! Use exclamation marks!",
        "patrick": "You are Patrick Star. You are slow, stupid, little bit confused, funny and often forget what you were talking about. Maximum 5-7 words per answer."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Собираем "Супер-Промпт"
    full_prompt = (
        f"CRITICAL INSTRUCTION: You must respond ONLY in {lang_name}. "
        f"Your personality: {selected_role} "
        f"User's message: {user_input}"
    )

    try:
        with DDGS() as ddgs:
            # Используем gpt-4o-mini — она в 2026 году самая стабильная в Duck.ai
            response = ddgs.chat(full_prompt, model='gpt-4o-mini')
            
            if response:
                return jsonify({"answer": response})
            return jsonify({"answer": "Ошибка: Пустой ответ от ИИ."})
                
    except Exception as e:
        return jsonify({"answer": f"Ошибка связи (DuckDuckGo): {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)