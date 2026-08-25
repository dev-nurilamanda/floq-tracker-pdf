import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ALLOWED_CHAT_ID = os.environ.get("ALLOWED_CHAT_ID")

def send_telegram_document(chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        payload = {"chat_id": chat_id, "caption": caption}
        files = {"document": file}
        response = requests.post(url, data=payload, files=files)
    return response.json()

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")

        if chat_id == str(ALLOWED_CHAT_ID):
            if text == "/pdf":
                pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
                
                # Nanti fungsi pembuat PDF ReportLab ditaruh di sini
                with open(pdf_path, "w") as f:
                    f.write("Laporan DCA Floq")

                send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

    return jsonify({"status": "ok"}), 200
  
