import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from g4f.client import Client

app = Flask(__name__)
CORS(app)

# Теперь API_KEY нам не нужен, g4f работает бесплатно
client = Client()

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
        # Используем g4f вместо Google GenAI
        # Он сам выберет лучшего провайдера и модель (GPT-4 или аналоги)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
        
    except Exception as e:
        return jsonify({"answer": f"Ошибка системы: {str(e)}"})

if __name__ == '__main__':
    # На Vercel порт берется из окружения
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)