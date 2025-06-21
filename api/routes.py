
from flask import Blueprint, request, jsonify
import asyncio
from ws import server
from flask import Response
from services import stream

routes = Blueprint('routes', __name__)
@routes.route("/send", methods=["GET"])
def send_message():
    msg = request.args.get("msg", "Hello from the Flask server!")
    asyncio.run(server.broadcast_to_all(msg))
    return jsonify({"status": "message sent", "msg": msg})

@routes.route('/video_feed')
def video_feed():
    return Response(stream.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@routes.route('/home')
def home():
    return jsonify({"message": "hello world."})