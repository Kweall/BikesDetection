from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(history):
    filename = f'reports/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    c = canvas.Canvas(filename)
    c.drawString(100, 800, "Отчет: Учёт велосипедов")
    y = 750
    for record in history:
        c.drawString(100, y, f"{record['timestamp']} — {record['file']} — Найдено: {record['bikes']}")
        y -= 30
    c.save()
    return filename
