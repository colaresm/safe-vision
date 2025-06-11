from flask import Flask, Response
import cv2
import time

app = Flask(__name__)
video = cv2.VideoCapture("movies/video.mp4")

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

@app.route('/stream')
def stream():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Server online at http://localhost:8081/stream")
    app.run(host='0.0.0.0', port=8081, threaded=True)
