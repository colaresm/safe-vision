
from flask import Blueprint, request, jsonify
import asyncio
from ws import server

routes = Blueprint('routes', __name__)
@routes.route("/send", methods=["GET"])
def send_message():
    msg = request.args.get("msg", "Hello from the Flask server!")
    asyncio.run(server.broadcast_to_all(msg))
    return jsonify({"status": "message sent", "msg": msg})

@routes.route('/home')
def home():
    return jsonify({"message": "hello world."})