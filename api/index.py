import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_telegram_document(chat_id, file_path, caption=""):
    """Fungsi khusus pengiriman dokumen"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            payload = {"chat_id": chat_id, "caption": caption}
            files = {"document": file}
            requests.post(url, data=payload, files=files, timeout=5)
    except Exception as e:
        print(f"Error sending doc: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "Bot Webhook Status: Active", 200

    data = request.get_json(force=True, silent=True) or {}

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text in ["/start", "/pdf"]:
            # Buat file dummy & pastikan file langsung ditutup
            pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
            with open(pdf_path, "w", encoding="utf-8") as f:
                f.write("Laporan DCA Floq - Testing Dummy PDF")

            # Kirim dokumen
            send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

            # Balas langsung via payload response Webhook ke Telegram
            return jsonify({
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": "⏳ Perintah diterima! Laporan PDF sedang dikirim..."
            }), 200

    return jsonify({"status": "ok"}), 200
    
