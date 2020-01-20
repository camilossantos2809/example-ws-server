import asyncio
import websockets
import json
from typing import Dict


STATUS = ""


async def ws_handler(websocket, path):
    global STATUS
    host = await websocket.recv()
    print(f"msg: {host}", STATUS)

    async for message in websocket:
        data: Dict[str, any] = json.loads(message)
        if data["type"] == "voos":
            await websocket.send(json.dumps({
                "type": "voos",
                "data": [{
                    "cod": 4027,
                    "desc": "AD 4027"
                }, {
                    "cod": 2500,
                    "desc": "AD 2500"
                }]
            }))
        elif data["type"] == "start_embarque":
            await asyncio.sleep(5)
            STATUS = "boarding"
            await websocket.send(json.dumps({
                "type": "start_embarque",
                "data": {"success": True}
            }))
        elif data["type"] == "init_embarque":
            STATUS = "processing"
            await asyncio.sleep(5)
            await websocket.send(json.dumps({
                "type": "init_embarque",
                "data": {"success": True}
            }))
            STATUS = "initiated"
        elif data["type"] == "end_embarque":
            await asyncio.sleep(5)
            STATUS = "not_boarding"
            await websocket.send(json.dumps({
                "type": "end_embarque",
                "data": {"success": True}
            }))
        elif data["type"] == "status":
            await websocket.send(json.dumps({
                "type": "status",
                "data": STATUS
            }))

start_server = websockets.serve(ws_handler, "0.0.0.0", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
