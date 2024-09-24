from libs import web
from aiohttp import WSMsgType

DEFAULT_ROUTE = "/api"
serial_queue = []

async def __handle_ping(request):
    return web.Response(text="pong")

async def __handle_ws_cam(request):
    return web.Response(text="WebSockets CAM")

async def __handle_ws_serial(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    serial_queue.append(ws)
    async for message in ws:
        if message.type ==  WSMsgType.TEXT:
            print(message.data)
            if message.data == 'CLOSE':
                await ws.close()
    return ws

app = web.Application()
routes = [
    web.get(DEFAULT_ROUTE + '/ws/cam', __handle_ws_cam),
    web.get(DEFAULT_ROUTE + '/ws/serial', __handle_ws_serial),
    web.get(DEFAULT_ROUTE + '/ping', __handle_ping),
]
app.add_routes(routes)

def start():
    web.run_app(app)