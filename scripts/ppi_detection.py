from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

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

detect_ppe_model = YOLO('../models/ppi_detecction.pt')
base_model = YOLO('../models/yolov8n.pt')

source_path = 'kx.37.12.png'

results_ppe = detect_ppe_model(source_path)
results_base = base_model(source_path)

ppe_boxes = []
for r_ppe in results_ppe:
    for box in r_ppe.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        ppe_boxes.append((x1, y1, x2, y2))

image = cv2.imread(source_path)

for r in results_base:
    for box in r.boxes:
        class_id = int(box.cls[0])
        class_name = base_model.names[class_id]

        if class_name == 'person':
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            person_box = (x1, y1, x2, y2)

            has_ppe = False
            for eb in ppe_boxes:
                if iou(person_box, eb) > 0.1:
                    has_ppe = True
                    break

            if  has_ppe:
                label = 'With PPE'
                color = (0, 255, 0)   
            else:
                label = 'Without PPE'
                color = (0, 0, 255)   

            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, label, (x1 + 20, y2),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, color, 3)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.show()
