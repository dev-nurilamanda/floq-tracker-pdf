import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_telegram_document(chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        payload = {"chat_id": chat_id, "caption": caption}
        files = {"document": file}
        return requests.post(url, data=payload, files=files).json()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        return "Bot Webhook Ready!", 200

    data = request.get_json(force=True, silent=True) or {}

    # Tangkap pesan dari Telegram
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Respon untuk tes koneksi
        if text in ["/start", "/pdf"]:
            send_telegram_message(chat_id, "⏳ Sedang memproses file PDF...")
            
            pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
            with open(pdf_path, "w") as f:
                f.write("Laporan DCA Floq - Testing Dummy PDF")

            send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

    return jsonify({"status": "ok"}), 200
    
