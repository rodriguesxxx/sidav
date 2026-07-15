import socket
import time

from . import movement
from .sensors import color_sensor
from . import sound

LISTEN_HOST = ""
LISTEN_PORT = 65432

NAVIGATION_PLAN = [
    (movement.forward, {"seconds": 5}),
    (movement.turn_left, {}),
    (movement.forward, {"seconds": 3.8}),
]


def start() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LISTEN_HOST, LISTEN_PORT))
        server.listen()
        print(f"Listening on port {LISTEN_PORT}")

        conn, addr = server.accept()
        with conn:
            print(f"Connected to {addr}")
            _handle_connection(conn)


def _handle_connection(conn: socket.socket) -> None:
    while True:
        data = conn.recv(1024)
        if not data:
            break

        command = data.decode("utf-8")

        if command == "start":
            _go_to_fire()
        else:
            print(f"Unknown command: {command}")


def _go_to_fire() -> None:
    for action, kwargs in NAVIGATION_PLAN:
        action(**kwargs)
        time.sleep(0.5)

    if color_sensor.read() != "orange":
        movement.backward(seconds=1.5)
        movement.turn_left_wide()
        movement.forward(seconds=3.5)

    sound.siren()