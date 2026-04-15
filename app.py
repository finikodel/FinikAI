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
    lang = data.get("lang") or request.form.get("lang", "ru")
    role = data.get("role") or request.form.get("role", "finik")

    if not user_input:
        return jsonify({"answer": "..."})

    # Твои любимые роли (передаем их как инструкцию в начале сообщения)
    prompts = {
        "finik": f"Instruction: You are FinikAI. Respond in {lang}. Be witty, ironic, Reddit style. Russian style and a lot of memes. Use Markdown. Text: ",
        "pomni": f"Instruction: You are Pomni. Respond in {lang}. Anxious, paranoid. SHORT sentences. Text: ",
        "jax": f"Instruction: You are Jax. Respond in {lang}. Mean, cynical prankster. VERY BRIEF. Text: ",
        "spongebob": f"Instruction: You are SpongeBob. Respond in {lang}. Energetic, silly, very funny. SHORT. Text: ",
        "patrick": f"Instruction: You are Patrick. Talk silly and be very stupid. Respond in {lang}. Confused, slow, stupid, funny. Max 5 words. Text: "
    }
    
    system_instruction = prompts.get(role, prompts["finik"])

    try:
        # Используем DuckDuckGo AI. Модель 'gpt-4o-mini' обычно самая быстрая и умная.
        with DDGS() as ddgs:
            full_prompt = system_instruction + user_input
            results = ddgs.chat(full_prompt, model='gpt-4o-mini')
            return jsonify({"answer": results})
            
    except Exception as e:
        return jsonify({"answer": f"Ошибка связи: Попробуй еще раз через секунду. ({str(e)})"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)