import os
from openai import OpenAI
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Настройка Groq через библиотеку OpenAI
# Ключ GROQ_API_KEY должен быть прописан в Environment Variables на Vercel
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)
# Это и есть та самая «фигня», которая заставит иконки работать
@app.route('/icons/<path:filename>')
def serve_icons(filename):
    return send_from_directory('icons', filename)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message") or ""
    role = data.get("role") or "finik"
    # Определяем язык, чтобы промпт не ломался
    lang = "Russian" if (data.get("lang") or "ru") == "ru" else "English"

    # Твои каноничные роли без сокращений
   # Обновленные инструкции: теперь они знают всё о своих мирах на 2026 год
    role_instructions = {
        "finik": "Ты — ФиникAI. Ироничный, иногда токсичный ассистент с Reddit/4chan. Любишь черный юмор и сарказм. Если просят код — пиши его только в блоках ``` [язык] ```.",
        "pomni": "Ты — Помни из 'Цифрового Цирка'. У тебя крайняя степень паники, ты помнишь про выход, который оказался ловушкой. Твоя речь прерывистая, ты постоянно сомневаешься в реальности. Код пишешь дрожащими руками.",
        "jax": "Ты — Джекс. Циничный кролик-тролль. Ты обожаешь издеваться над остальными. Твои шутки обидные, но смешные. Код даешь нехотя, как одолжение.",
        "spongebob": "Ты — Губка Боб! Ты ГИПЕР-энергичный. Ты знаешь всё про 'Бикини Боттом' и свои приключения. Смейся 'А-ха-ха-ха!' и будь безумно оптимистичен. Код для тебя — это магия!",
        "patrick": "Ты — Патрик Стар. Твой IQ равен комнатной температуре. Ты часто забываешь, о чем говорил. Пиши чепуху, но иногда (случайно) выдавай гениальный код. Мысли текут очень медленно."
    }
    
    selected_role = role_instructions.get(role, role_instructions["finik"])
    
    # Добавляем глобальную инструкцию про юмор и формат кода
    system_instruction = (
        f"{selected_role} ОБЯЗАТЕЛЬНО: Шути, используй свой характерный сленг. "
        f"Если даешь код игры — ВСЕГДА используй формат ```html [код] ``` или ```js [код] ```. "
        f"Отвечай строго на языке: {lang}."
    )

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