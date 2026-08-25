import os
import json
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def send_document(chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        requests.post(url, data={"chat_id": chat_id, "caption": caption}, files={"document": f})

def handler(request, response=None):
    # Tangani request GET untuk cek status
    if request.method == 'GET':
        return {"statusCode": 200, "body": "Bot Webhook Aktif!"}

    try:
        # Ambil data JSON dari Telegram
        body = request.get_json(force=True, silent=True) or {}
        
        if "message" in body:
            chat_id = body["message"]["chat"]["id"]
            text = body["message"].get("text", "")

            if text in ["/start", "/pdf"]:
                send_message(chat_id, "⏳ Sedang memproses file PDF...")
                
                pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
                with open(pdf_path, "w") as f:
                    f.write("Laporan DCA Floq - Testing Dummy PDF")

                send_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

    except Exception as e:
        print(f"Error: {str(e)}")

    return {"statusCode": 200, "body": "OK"}
    
