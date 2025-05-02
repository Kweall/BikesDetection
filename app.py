import streamlit as st
from detect import process_image, process_video
from report_generator import generate_excel_report
import os
import json
from datetime import datetime


st.set_page_config(page_title="Велопарковка: детектирование", layout="centered")
st.title("🚲 Обнаружение велосипедов с помощью YOLOv8")
uploaded_file = st.file_uploader("Загрузите изображение или видео", type=["jpg", "jpeg", "png", "mp4"])

history_file = "history.json"
history = []

# Загрузка истории (с проверкой на пустой файл)
if os.path.exists(history_file):
    try:
        with open(history_file, "r") as f:
            content = f.read().strip()
            if content:
                history = json.loads(content)
    except json.JSONDecodeError:
        st.warning("Файл history.json повреждён. Начинаем с пустой истории.")
        history = []

# Обработка изображения
if uploaded_file and uploaded_file.type.startswith("image"):
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp.jpg", caption="Исходное изображение", use_column_width=True)

    if st.button("Обработать изображение"):
        result_path, result, count = process_image("temp.jpg")
        st.image(result_path, caption="Результат обработки", use_column_width=True)
        st.info(f"Обнаружено велосипедов: {count}")

        # Сохраняем в историю
        entry = {
            "type": "image",
            "filename": uploaded_file.name,
            "timestamp": datetime.now().isoformat(),
            "count": count
        }
        history.append(entry)
        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)

# Обработка видео
if uploaded_file and uploaded_file.type.startswith("video"):
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video("temp_video.mp4")  # Показываем исходное видео

    if st.button("Обработать видео"):
        result_path, count = process_video("temp_video.mp4")
        st.success(f"Видео обработано! Обнаружено велосипедов: {count}")

        if os.path.exists(result_path):
            with open(result_path, "rb") as vid_file:
                video_bytes = vid_file.read()
            st.video(video_bytes)  # Показываем обработанное видео

            # Сохраняем в историю
            entry = {
                "type": "video",
                "filename": uploaded_file.name,
                "timestamp": datetime.now().isoformat(),
                "count": count
            }
            history.append(entry)
            with open(history_file, "w") as f:
                json.dump(history, f, indent=4)

# Вывод истории
if history:
    st.markdown("### 📜 История запросов")
    if st.button("📊 Сформировать Excel-отчет"):
        report_path = generate_excel_report(history)
        with open(report_path, "rb") as f:
            st.download_button("⬇️ Скачать отчет", f, file_name=os.path.basename(report_path))
    for item in reversed(history[-5:]):  # последние 5 записей
        count_info = f" — Велосипедов: {item['count']}" if "count" in item else ""
        st.write(f"{item['timestamp']} — {item['type']} — {item['filename']}{count_info}")
