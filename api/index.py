import os
import requests
from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Langsung pasang token di sini biar tidak terhalang Vercel Env
TELEGRAM_TOKEN = "8902273230:AAEcaTTOLYuDGb5mgC4-xKLaI1-43OIi2H0"

def create_valid_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "LAPORAN TRANSAKSI FLOQ TRACKER")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Status: Testing Bot PDF Success!")
    c.drawString(100, 700, "-------------------------------------------")
    c.drawString(100, 680, "Sistem serverless Vercel & Telegram Webhook aktif.")
    c.save()

def send_telegram_document(chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            payload = {"chat_id": chat_id, "caption": caption}
            files = {"document": ("Laporan_Floq.pdf", file, "application/pdf")}
            res = requests.post(url, data=payload, files=files, timeout=15)
            print("Response status code:", res.status_code)
            print("Response body:", res.text)
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
            pdf_path = "/tmp/Laporan_DCA_Floq.pdf"
            
            # 1. Bikin PDF
            create_valid_pdf(pdf_path)

            # 2. Kirim PDF
            send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

    return jsonify({"status": "ok"}), 200
    
