from ultralytics import YOLO
import cv2

modelo_path = 'models/ppe_detection.pt'
imagem_path = 'tests/image (3).png'


modelo = YOLO(modelo_path)
resultados = modelo(imagem_path,conf=0.85)

imagem = cv2.imread(imagem_path)
for r in resultados:
    for box in r.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Resultado", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
