from libs import asyncio, cv, np, base64
from mask import process_frame

def handle_cams(cams_queue, serial_queue):
    loop = asyncio.new_event_loop()
    while True:
        if not cams_queue.empty():
            cam = cams_queue.get()
            cam_id = cam[0]
            image_bytes = np.array(cam[1]).tobytes()
            image_bytes = np.frombuffer(image_bytes, dtype=np.uint8) 
            img = cv.imdecode(image_bytes, flags=cv.IMREAD_COLOR)
            img = process_frame(img)
            retval, buffer = cv.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buffer).decode("utf-8")
            for ws in serial_queue:
                try:
                    loop.run_until_complete(ws.send_str(jpg_as_text))
                except:
                    print('[WS] Comunicação encerrada!')
