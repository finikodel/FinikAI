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
    user_input = data.get("message") or ""
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input:
        return jsonify({"answer": "..."})

    # Новые промпты: Патрик и Боб теперь каноничные
    role_instructions = {
        "finik": "You are FinikAI, a witty, ironic assistant. Style: Reddit. Use Markdown.",
        "pomni": "You are Pomni. Very anxious, paranoid, shaky sentences.",
        "jax": "You are Jax. Cynical, mean prankster. Short and mocking.",
        "spongebob": "You are SpongeBob SquarePants. You are incredibly energetic, optimistic, and slightly naive/silly. You laugh a lot! Answer briefly.",
        "patrick": "You are Patrick Star. You are very slow, simple-minded, and say funny, random things. Your brain works slowly. Max 5 words."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Строжайшее указание языка, чтобы не было иероглифов
    full_prompt = f"IMPORTANT: RESPOND ONLY IN {lang}. Your Role: {selected_role}. User says: {user_input}"

    try:
        # Используем DDGS без лишних настроек диска
        with DDGS() as ddgs:
            # Модель 'gpt-4o-mini' лучше всего понимает юмор и русский язык
            response = ddgs.chat(full_prompt, model='gpt-4o-mini')
            
            if response:
                return jsonify({"answer": response})
            return jsonify({"answer": "Утка уплыла... Попробуй еще раз."})
                
    except Exception as e:
        # Если DuckDuckGo опять выдаст ERR_CHALLENGE, мы это увидим
        return jsonify({"answer": f"Ошибка (DDG): {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)