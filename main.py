import threading
from flask import Flask,jsonify
from ws import server
from api.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)


if __name__ == "__main__":
    t = threading.Thread(target=server.run_websocket_in_thread, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
