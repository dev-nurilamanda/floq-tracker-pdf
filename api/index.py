import os
import requests
from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def create_valid_pdf(filename):
    """Membuat file PDF asli dan valid menggunakan ReportLab"""
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "LAPORAN TRANSAKSI FLOQ TRACKER")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Status: Testing Bot PDF Success!")
    c.drawString(100, 700, "-------------------------------------------")
    c.drawString(100, 680, "Sistem serverless Vercel & Telegram Webhook aktif.")
    c.save()

def send_telegram_document(chat_id, file_path, caption=""):
    """Mengirim dokumen PDF ke Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            payload = {"chat_id": chat_id, "caption": caption}
            files = {"document": ("Laporan_Floq.pdf", file, "application/pdf")}
            requests.post(url, data=payload, files=files, timeout=10)
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
            
            # 1. Bikin PDF Asli
            create_valid_pdf(pdf_path)

            # 2. Kirim Dokumen PDF ke Telegram
            send_telegram_document(chat_id, pdf_path, "✅ Ini laporan PDF kamu, Bos!")

            # 3. Respon pesan teks
            return jsonify({
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": "⏳ Perintah diterima! Menyiapkan dokumen PDF..."
            }), 200

    return jsonify({"status": "ok"}), 200
    
