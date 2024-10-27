from routes import start, cams_queue, serial_queue
from cam import handle_cams
from libs import threading

if __name__ == '__main__':
    _ = threading.Thread(target=handle_cams, args=((cams_queue, serial_queue)))
    _.start()

    start()
