import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Подхватываем ключ CLIENT_KEY из настроек Vercel (как на твоем скрине)
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
    # ИСПРАВЛЕНИЕ: Пытаемся взять сообщение и из JSON, и из обычной формы
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or request.form.get("message")
    
    lang = data.get("lang") or request.form.get("lang", "ru")
    role = data.get("role") or request.form.get("role", "finik")
    file = request.files.get("file")

    # Если сообщение РЕАЛЬНО пустое, тогда отдаем точки
    if not user_input and not file:
        return jsonify({"answer": "..."})

    prompts = {
        "finik": f"You are FinikAI. Answer in {lang}. Be witty, ironic, use Reddit style. If user asks for image/link, provide them using Markdown. BE BRIEF.",
        "pomni": f"You are Pomni. Answer in {lang}. Anxious, paranoid. SHORT sentences.",
        "jax": f"You are Jax. Answer in {lang}. Mean, cynical prankster. VERY BRIEF.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. Energetic, naive. SHORT.",
        "patrick": f"You are Patrick. Answer in {lang}. Confused, slow. Max 5 words."
    }
    
    system_prompt = prompts.get(role, prompts["finik"])

    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_prompt
        )

        content = user_input if user_input else ""
        if file:
            content += f" (Пользователь прикрепил файл: {file.filename})"

        response = model.generate_content(content)
        return jsonify({"answer": response.text})
        
    except Exception as e:
        # Если ошибка в ключе или API, мы это увидим
        return jsonify({"answer": f"Ошибка системы: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)