import pandas as pd
from datetime import datetime
import os

def generate_excel_report(history):
    os.makedirs("reports", exist_ok=True)

    df = pd.DataFrame(history)
    df = df[["timestamp", "type", "filename", "count"]]
    df.columns = ["Время", "Тип", "Имя файла", "Количество велосипедов"]
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)

    return filename
