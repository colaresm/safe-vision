from ultralytics import YOLO
import cv2
import time
from services.ppi_detection import detect_ppe
from ws import server
import asyncio
from flask import request


model = YOLO('models/yolov8n.pt')
video = cv2.VideoCapture("static/movie2.mp4")

base_model = YOLO('models/yolov8n.pt')
ppe_model = YOLO('models/ppe_detection.pt')   

def generate_frames():
    global video

    while True:
        success, frame = video.read()
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results_base = base_model(frame)
        results_ppe = ppe_model(frame)

        annotated_frame, has_notification = detect_ppe(frame, results_base, results_ppe, base_model)
        print(has_notification)
        if has_notification:
            asyncio.run(server.broadcast_to_all( "Ausência EPI detectada!"))
        
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)


