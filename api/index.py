import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = os.environ.get("ALLOWED_CHAT_ID")

def send_telegram_message(chat_id, text):
    """Fungsi pembantu untuk mengirim pesan teks biasa"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def send_telegram_document(chat_id, file_path, caption=""):
    """Fungsi untuk mengirim file dokumen ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        payload = {"chat_id": chat_id, "caption": caption}
        files = {"document": file}
        return requests.post(url, data=payload, files=files).json()

@app.route('/', methods=['GET', 'POST'])
@app.route('/api/index', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Bot Webhook Ready!", 200

    data = request.get_json(silent=True) or {}

    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")

        # Keamanan: Cek ID Pengirim
        if chat_id == str(ALLOWED_CHAT_ID):
            if text in ["/start", "/pdf"]:
                # Kirim pesan respons indikator awal
                send_telegram_message(chat_id, "⏳ Sedang memproses file PDF...")
                
                pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
                with open(pdf_path, "w") as f:
                    f.write("Laporan DCA Floq - Testing Dummy PDF")

                send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")
        else:
            send_telegram_message(chat_id, "Akses ditolak!")

    return jsonify({"status": "ok"}), 200

