import cv2

cap = cv2.VideoCapture("http://localhost:8081/stream")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("MJPEG de Go", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
