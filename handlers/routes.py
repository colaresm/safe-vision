# handlers/routes.py

from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)

@routes.route('/home')
def home():
    return jsonify({"message": "hello world."})
