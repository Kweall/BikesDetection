import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
import cv2
import uuid

# Инициализация модели YOLOv8
model = YOLO('yolov8n.pt')

# Класс велосипеда в COCO = 1
BICYCLE_CLASS_ID = [1]

def process_image(image_path):
    results = model(image_path, classes=BICYCLE_CLASS_ID)
    annotated_frame = results[0].plot()
    
    output_path = f"results/{uuid.uuid4()}.jpg"
    cv2.imwrite(output_path, annotated_frame)

    # Подсчет велосипедов (по количеству боксов)
    num_bicycles = len(results[0].boxes)
    return output_path, results[0], num_bicycles


def process_video(video_path):
    os.makedirs("results", exist_ok=True)  # <- Добавлено
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Не удалось открыть видео.")

    uid = uuid.uuid4()
    out_path = f"results/{uid}.mp4"

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Исправленный кодек
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))

    unique_ids = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, classes=BICYCLE_CLASS_ID, persist=True, tracker="bytetrack.yaml")
        annotated_frame = results[0].plot()

        if results[0].boxes.id is not None:
            ids = results[0].boxes.id.int().tolist()
            unique_ids.update(ids)

        out.write(annotated_frame)

    cap.release()
    out.release()
    
    # Проверка файла
    if os.path.getsize(out_path) == 0:
        raise Exception("Ошибка: видеофайл не был записан")
    
    return out_path, len(unique_ids)
