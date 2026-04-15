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
        # Используем прямой вызов без создания Client
        # Это исключает ошибку "Add a api_key"
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4, # Можно попробовать gpt_4o или оставить gpt_4
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
        )
        
        # Если ответ пустой, пробуем еще раз с другой моделью автоматически
        if not response:
             response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": system_prompt + " " + user_input}],
            )

        return jsonify({"answer": response})
        
    except Exception as e:
        return jsonify({"answer": f"Ошибка системы: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)