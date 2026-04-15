import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import g4f

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
    lang = data.get("lang") or request.form.get("lang", "ru")
    role = data.get("role") or request.form.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    prompts = {
        "finik": f"You are FinikAI. Answer in {lang}. Be witty, ironic, Reddit style. Use Markdown.",
        "pomni": f"You are Pomni. Answer in {lang}. Anxious, paranoid. SHORT.",
        "jax": f"You are Jax. Answer in {lang}. Mean, cynical prankster. BRIEF.",
        "spongebob": f"You are SpongeBob. Answer in {lang}. Energetic. SHORT.",
        "patrick": f"You are Patrick. Answer in {lang}. Confused. Max 5 words."
    }
    system_prompt = prompts.get(role, prompts["finik"])

    try:
        # Список провайдеров, которые реже всего "китайничают"
        # Мы пробуем их по очереди
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o, # gpt_4o сейчас самая стабильная
            messages=[
                {"role": "system", "content": system_prompt + " ВАЖНО: Отвечай ТОЛЬКО на выбранном языке пользователя!"},
                {"role": "user", "content": user_input}
            ],
            # Явно указываем игнорировать проблемных провайдеров, если они будут лезть
            ignore_working_providers=False, 
        )
        
        if not response:
             return jsonify({"answer": "Финик задумался... Попробуй еще раз."})

        return jsonify({"answer": response})
        
    except Exception as e:
        # Если GPT-4o не сработал, пробуем самый простой и быстрый вариант
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Answer in {lang}: {user_input}"}],
            )
            return jsonify({"answer": response})
        except:
            return jsonify({"answer": f"Ошибка системы: {str(e)}"})