import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 1. Берем ключ именно по твоему названию из Vercel
API_KEY = os.environ.get("GOOGLE_API_KEY")
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
    # Получаем данные (поддержка и JSON, и Form для твоего старого скрипта)
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or request.form.get("message")
    lang = data.get("lang") or request.form.get("lang", "ru")
    role = data.get("role") or request.form.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    # Описания ролей (твои любимые персонажи)
    prompts = {
        "finik": f"You are FinikAI. Answer in {lang}. Be witty, ironic, Reddit style. Use Markdown.",
        "pomni": f"You are Pomni. Answer in {lang}. Anxious, paranoid. SHORT sentences.",
        "jax": f"You are Jax. Answer in {lang}. Mean, cynical prankster. VERY BRIEF.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. Energetic, naive. SHORT.",
        "patrick": f"You are Patrick. Answer in {lang}. Confused, slow. Max 5 words."
    }
    
    system_prompt = prompts.get(role, prompts["finik"])

    try:
        # 2. Используем актуальную модель Gemini 3 Flash
        model = genai.GenerativeModel(
            model_name='gemini-3-flash',
            system_instruction=system_prompt
        )

        response = model.generate_content(user_input)
        return jsonify({"answer": response.text})
        
    except Exception as e:
        # Если модель не найдена или ключ не подхватился, выводим понятную ошибку
        return jsonify({"answer": f"Ошибка системы: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)