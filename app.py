import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Настройка Groq через библиотеку OpenAI
# Ключ GROQ_API_KEY должен быть прописан в Environment Variables на Vercel
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    role = data.get("role") or "finik"
    # Определяем язык, чтобы промпт не ломался
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"

    # Твои каноничные роли без сокращений
    role_instructions = {
        "finik": "Ты — ФиникAI, ироничный ассистент. Стиль: Reddit.",
        "pomni": "Ты — Помни. У тебя паника, ты в Цифровом Цирке. Трясущиеся короткие фразы.",
        "jax": "Ты — Джекс. Циничный кролик-тролль. Короткие издевки.",
        "spongebob": "Ты — Губка Боб! Ты ГИПЕР-энергичный, безумно добрый, но очень глупенький и наивный. Смейся 'А-ха-ха-ха!' в конце каждой фразы.",
        "patrick": "Ты — Патрик Стар. Ты ОЧЕНЬ ТУПОЙ. Твои мысли текут как улитка. Максимум 5 слов. Пиши полную чепуху невпопад."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Формируем четкую инструкцию для модели
    full_prompt = f"STRICT: Answer ONLY in {lang}. Role context: {selected_role}. User: {user_input}"

    selected_role = role_instructions.get(role, role_instructions["finik"])

    try:
        # ЗАМЕНЯЕМ МОДЕЛЬ НА ТУ, ЧТО ТОЧНО РАБОТАЕТ В 2026:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Актуальная замена старой 70b модели
            messages=[
                {"role": "system", "content": f"STRICT: Answer ONLY in {lang}. Role: {selected_role}"},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        # Если Groq снова выдаст ошибку, мы увидим её тут
        return jsonify({"answer": f"Блин, затык: {str(e)}"})

@app.route('/')
def index(): 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)