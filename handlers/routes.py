from flask import Blueprint, jsonify
from flask import Response
from services import stream
routes = Blueprint("routes", __name__)

@routes.route('/home')
def home():
    return jsonify({"message": "hello world."})

@routes.route('/stream')
def stream():
    return Response(stream.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
