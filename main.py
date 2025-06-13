from flask import Flask, render_template
import asyncio
import websockets
import datetime
import threading

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

async def ws_handler(websocket):
    print("Cliente WebSocket conectado")
    try:
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            message = f"Mensagem enviada às {now}"
            await websocket.send(message)
            print(f"Enviado: {message}")
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        print("Cliente WebSocket desconectado")

def start_websocket_server():
    print("Iniciando servidor WebSocket...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        server = await websockets.serve(ws_handler, "localhost", 3000)
        print("Servidor WebSocket rodando em ws://localhost:3000")
        await server.wait_closed()

    loop.run_until_complete(main())
    loop.run_forever()

if __name__ == "__main__":
    ws_thread = threading.Thread(target=start_websocket_server)
    ws_thread.daemon = True
    ws_thread.start()

    print("Iniciando servidor Flask...")
    app.run(debug=True, host="0.0.0.0", port=5000)
