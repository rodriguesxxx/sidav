# TODO: Remover necessidade de ID de camera

from libs import web, WSMsgType, queue, aiohttp_jinja2, jinja2, os

DEFAULT_ROUTE = "/api"
serial_queue = []
cams_queue = queue.Queue(maxsize=10)

async def __handle_ping(request):
    return web.Response(text="pong")

async def __handle_ws_cam(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    data = []
    cam = None
    async for message in ws:
        # print(message.type, message.data)
        if message.type == WSMsgType.ERROR:
            print("erro: ", ws.exception())
            await ws.close()
        elif message.type == WSMsgType.TEXT:
            if message.data.startswith('START'):
                print("Iniciando captura do ID da câmera...")
                cam = message.data.replace('START:', '')
                data = []
            elif message.data == 'STOP':
                print("Finalizando captura do ID/FRAME da câmera...")
                cams_queue.put([cam, data])
        elif message.type == WSMsgType.BINARY:
            print("Iniciando captura do FRAME da câmera...")
            data.append(message.data)
            print("DADOS: ", message.data)
    return ws
    
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

@aiohttp_jinja2.template("index.html")
async def index(request):
    return {}

def start():
    
    app = web.Application()
    
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    
    routes = [
        web.get('/', index, name="index"),
        web.get(DEFAULT_ROUTE + '/ws/cam', __handle_ws_cam),
        web.get(DEFAULT_ROUTE + '/ws/serial', __handle_ws_serial),
        web.get(DEFAULT_ROUTE + '/ws/ping', __handle_ping),
    ]
    
    app.add_routes(routes)
    web.run_app(app)