from ultralytics import YOLO
import cv2
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def iou(box1, box2):
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0

    box1Area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2Area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    return interArea / float(box1Area + box2Area - interArea)

detect_ppe_model = YOLO('models/ppi_detecction.pt')
base_model = YOLO('models/yolov8n.pt')

video_path = 'static/movie2.mp4'
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Salva temporariamente o frame para enviar ao modelo
    temp_frame_path = "temp.jpg"
    cv2.imwrite(temp_frame_path, frame)

    results_ppe = detect_ppe_model(temp_frame_path)
    results_base = base_model(temp_frame_path)

    ppe_boxes = []
    for r_ppe in results_ppe:
        for box in r_ppe.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            ppe_boxes.append((x1, y1, x2, y2))

    for r in results_base:
        for box in r.boxes:
            class_id = int(box.cls[0])
            class_name = base_model.names[class_id]

            if class_name == 'person':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_box = (x1, y1, x2, y2)

                has_ppe = any(iou(person_box, eb) > 0.1 for eb in ppe_boxes)

                label = 'With PPE' if has_ppe else 'Without PPE'
                color = (0, 255, 0) if has_ppe else (0, 0, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1 + 20, y2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("PPE Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
