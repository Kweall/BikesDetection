from ultralytics import YOLO
import cv2
import os
import uuid

model = YOLO('yolov8n.pt')
# results = model('image.jpg')
# results[0].show()

def process_image(image_path):
    results = model(image_path)
    output_path = f"results/{uuid.uuid4()}.jpg"
    results[0].save(filename=output_path)
    return output_path, results[0]

# def process_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     uid = uuid.uuid4()
#     out_path = f"results/{uid}.mp4"
#     out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 30,
#                           (int(cap.get(3)), int(cap.get(4))))
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame)
#         annotated_frame = results[0].plot()
#         out.write(annotated_frame)
#     cap.release()
#     out.release()
#     return out_path

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Не удалось открыть видео.")

    uid = uuid.uuid4()
    out_path = f"results/{uid}.mp4"
    
    # Получаем параметры видео (ширина, высота и FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Инициализация записи видео с использованием кодека mp4v
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()

    return out_path