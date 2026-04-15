import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from g4f.client import Client

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
    lang_code = data.get("lang") or "ru"
    lang_name = "Russian" if lang_code == "ru" else "English"
    role = data.get("role") or "finik"

    if not user_input:
        return jsonify({"answer": "..."})

    role_instructions = {
        "finik": "You are FinikAI, a witty and slightly ironic AI assistant. Your style is a mix of Reddit humor and helpful expert. Use Markdown.",
        "pomni": "You are Pomni from The Amazing Digital Circus. You are extremely anxious, paranoid, and confused. Use short, shaky sentences.",
        "jax": "You are Jax from The Amazing Digital Circus. You are a cynical, mean prankster who doesn't care about others. Keep it very brief and mocking.",
        "spongebob": "You are SpongeBob SquarePants. You are incredibly energetic, optimistic, little bit dumb, funny and happy! Use exclamation marks!",
        "patrick": "You are Patrick Star. You are slow, a bit confused, stupid, funny and often forget what you were talking about. Maximum 5-7 words per answer."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    full_prompt = f"STRICT RULE: Answer ONLY in {lang_name}. Role: {selected_role}. User: {user_input}"

    try:
        # Client сам подбирает провайдера, обходя ERR_CHALLENGE
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"STRICT: Answer ONLY in {lang_name}. {selected_role}"},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer if answer else "Финик задумался..."})
    except Exception as e:
        # Если всё совсем плохо, выводим ошибку, чтобы понять причину 500-й
        return jsonify({"answer": f"Ошибка системы: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)