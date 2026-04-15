import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- НАСТРОЙКА GEMINI ---
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBkdfyrFv3-j1L2aojIxEKmeNHpDuARzHo")
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
    # Твои старые добрые параметры из FormData
    user_input = request.form.get("message")
    lang = request.form.get("lang", "ru")
    role = request.form.get("role", "finik")
    file = request.files.get("file")

    if not user_input and not file:
        return jsonify({"answer": "..."})

    # Описание ролей (сохранил твою логику)
    prompts = {
        "finik": f"You are FinikAI. Answer in {lang}. Be witty, ironic, use Reddit style. If user asks for image/link, provide them using Markdown. BE BRIEF.",
        "pomni": f"You are Pomni. Answer in {lang}. Anxious, paranoid. SHORT sentences.",
        "jax": f"You are Jax. Answer in {lang}. Mean, cynical prankster. VERY BRIEF.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. Energetic, naive. SHORT.",
        "patrick": f"You are Patrick. Answer in {lang}. Confused, slow. Max 5 words."
    }
    
    system_prompt = prompts.get(role, prompts["finik"])

    try:
        # Инициализируем модель с нужной ролью
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_prompt
        )

        content = user_input if user_input else ""
        if file:
            content += f" (Пользователь прикрепил файл: {file.filename})"

        # Генерируем ответ
        response = model.generate_content(content)
        
        return jsonify({"answer": response.text})
        
    except Exception as e:
        return jsonify({"answer": f"Ошибка Gemini: {str(e)}"})

if __name__ == '__main__':
    # На Vercel порт подхватится автоматически, для локала оставил 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)