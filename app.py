import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Используем твой ключ CLIENT_KEY из настроек Vercel
API_KEY = os.environ.get("CLIENT_KEY", "AIzaSyBkdfyrFv3-j1L2aojIxEKmeNHpDuARzHo")
genai.configure(api_key=API_KEY)

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
    lang = data.get("lang") or request.form.get("lang", "ru")
    role = data.get("role") or request.form.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    # Твои любимые роли
    prompts = {
        "finik": f"You are FinikAI. Answer in {lang}. Be witty, ironic, Reddit style. Use Markdown.",
        "pomni": f"You are Pomni. Answer in {lang}. Anxious, paranoid. SHORT.",
        "jax": f"You are Jax. Answer in {lang}. Mean, cynical prankster. BRIEF.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. Energetic. SHORT.",
        "patrick": f"You are Patrick. Answer in {lang}. Confused. Max 5 words."
    }
    
    system_prompt = prompts.get(role, prompts["finik"])

    # Список моделей на пробу (самая новая -> стабильная)
    model_names = ['gemini-3-flash', 'gemini-3-pro', 'gemini-2.5-flash']

    for name in model_names:
        try:
            model = genai.GenerativeModel(
                model_name=name,
                system_instruction=system_prompt
            )
            response = model.generate_content(user_input)
            return jsonify({"answer": response.text})
        except Exception as e:
            # Если это последняя модель в списке и она упала — пишем ошибку
            if name == model_names[-1]:
                return jsonify({"answer": f"Ошибка системы: {str(e)}"})
            continue # Пробуем следующую модель из списка

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)