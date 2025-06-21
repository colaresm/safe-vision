import websockets
import asyncio

connected_clients = set()
async def websocket_handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("Received:", message)
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def start_websocket_server():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        print("WebSocket server running on port 8765")
        await asyncio.Future() 

def run_websocket_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server())


async def broadcast_to_all(msg):
    if connected_clients:
        await asyncio.gather(*(ws.send(msg) for ws in connected_clients))
    else:
        print("No connected clients")

