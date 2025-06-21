import cv2
import time

video = cv2.VideoCapture("static/video.mp4")
def generate_frames():
    global video
    while True:
        success, frame = video.read()
        if not success:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)
