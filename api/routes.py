
from flask import Blueprint, request, jsonify, render_template
import asyncio
from ws import server
from flask import Response
from services import stream

routes = Blueprint('routes', __name__)
@routes.route("/send-test", methods=["GET"])
def send_message():
    msg = request.args.get("msg", "Hello from the Flask server!")
    asyncio.run(server.broadcast_to_all(msg))
    return jsonify({"status": "message sent", "msg": msg})

@routes.route('/video_feed')
def video_feed():
    return Response(stream.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@routes.route('/healthy')
def healthy():
    return jsonify({"message": "is healthy"})

@routes.route('/home')
def home():
    return render_template('index.html')