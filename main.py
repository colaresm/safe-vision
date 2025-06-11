#import cv2

#cap = cv2.VideoCapture("http://localhost:8081/stream")

#while cap.isOpened():
  #  ret, frame = cap.read()
  #  if not ret:
  #      break
 #   cv2.imshow("MJPEG de Go", frame)
 #   if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    print("acionado")
    # renderiza o arquivo templates/home.html
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
