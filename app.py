import asyncio
import json
from aiohttp import web

routes = web.RouteTableDef()
clients = {}

@routes.get("/")
async def index(request):
    return web.FileResponse("index.html")

@routes.get("/ws")
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    peer_id = str(id(ws))
    clients[peer_id] = ws
    print("Client connected:", peer_id)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = json.loads(msg.data)
            for pid, client in clients.items():
                if pid != peer_id:
                    await client.send_json(data)

    del clients[peer_id]
    print("Client disconnected:", peer_id)
    return ws

app = web.Application()
app.add_routes(routes)

web.run_app(app, port=8080)
