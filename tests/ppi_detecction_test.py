import os
import cv2
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
import matplotlib.pyplot as plt

model_path = 'models/ppi_detecction.pt'
image_path = 'tests/test.jpg'

model = YOLO(model_path)

results = model(image_path)

for result in results:
    img = result.plot()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()
