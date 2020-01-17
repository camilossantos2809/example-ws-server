import asyncio
import websockets
import json


async def ws_handler(websocket, path):
    host = await websocket.recv()
    print(f"{host} conectado")

    greeting = f"Client {host} conectado ao WS"
    await websocket.send(greeting)

    async for message in websocket:
        data = json.loads(message)



start_server = websockets.serve(ws_handler, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
