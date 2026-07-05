from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# Включаем CORS, чтобы браузер разрешал нашему HTML-файлу общаться с этим сервером
CORS(app)

@app.route('/api/analytics', methods=['POST', 'OPTIONS'])
def log_analytics():
    # 1. Сначала обрабатываем проверочный запрос OPTIONS от браузера
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    # 2. Если это реальный POST-запрос с данными, обрабатываем его
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Пустые данные"}), 400

        user_ip = data.get('ip', 'Неизвестный IP')
        user_agent = data.get('userAgent', 'Неизвестный браузер')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Запись в файл logs.txt (файл создаётся сам в той же папке)
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{current_time}] IP: {user_ip} | Browser: {user_agent}\n")
            
        print(f"[SERVER] Успешно записан лог для IP: {user_ip}")
        return jsonify({"status": "success", "message": "Данные сохранены"}), 200
        
    except Exception as e:
        print(f"[SERVER] Ошибка при записи: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Сервер аналитики запущен на http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)