from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
# Разрешаем CORS для всех запросов, чтобы GitHub Pages мог общаться с сервером
CORS(app)

@app.route('/api/analytics', methods=['POST', 'OPTIONS'])
def log_analytics():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Пустые данные"}), 400

        user_ip = data.get('ip', 'Неизвестный IP')
        user_agent = data.get('userAgent', 'Неизвестный браузер')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Запись в файл logs.txt в корне проекта
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{current_time}] IP: {user_ip} | Browser: {user_agent}\n")
            
        print(f"[SERVER] Успешно записан лог для IP: {user_ip}")
        return jsonify({"status": "success", "message": "Данные сохранены"}), 200
        
    except Exception as e:
        print(f"[SERVER] Ошибка при записи: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # В интернете Render сам передает нужный порт через переменную окружения PORT
    port = int(os.environ.get('PORT', 5000))
    # Хост '0.0.0.0' обязателен, чтобы сервер принимал внешние запросы
    app.run(host='0.0.0.0', port=port)
