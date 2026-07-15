"""Camera frame processing pipeline.

Receives raw frames from ESP32-CAM via WebSocket queues, runs fire detection,
and broadcasts processed frames back to connected WebSocket clients.
"""

import asyncio
import base64
import logging
from queue import Queue

import cv2 as cv
import numpy as np

from .fire_detector import detect_fire
from .robot_client import notify_robot

logger = logging.getLogger(__name__)


def handle_frames(frame_queue: Queue, serial_queue: list) -> None:
    """Continuously process frames from the queue.

    Each queue item is [cam_id, list_of_binary_frames].
    Processed frames are base64-encoded and broadcast to all serial WebSocket clients.

    Args:
        frame_queue: Queue receiving [cam_id, frames] from WebSocket handlers.
        serial_queue: List of active aiohttp WebSocket connections for broadcast.
    """
    loop = asyncio.new_event_loop()

    while True:
        if frame_queue.empty():
            continue

        item = frame_queue.get()
        cam_id = item[0]
        raw_frames = item[1]

        try:
            img = _decode_frame(raw_frames)
            processed, fire_detected = detect_fire(img)
        except Exception:
            logger.exception("Frame processing failed for camera '%s'", cam_id)
            continue

        retval, buffer = cv.imencode(".jpg", processed)
        jpg_b64 = base64.b64encode(buffer).decode("utf-8")

        if fire_detected:
            logger.info("Fire detected by camera '%s' — notifying robot", cam_id)
            notify_robot()

        _broadcast(loop, serial_queue, jpg_b64)


def _decode_frame(raw_frames: list[bytes]) -> np.ndarray:
    """Decode a list of binary chunks into an OpenCV BGR image."""
    data = np.array(raw_frames).tobytes()
    buf = np.frombuffer(data, dtype=np.uint8)
    img = cv.imdecode(buf, flags=cv.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode frame")
    return img


def _broadcast(loop: asyncio.AbstractEventLoop, clients: list, data: str) -> None:
    """Send data to all connected WebSocket serial clients."""
    disconnected: list = []
    for ws in clients:
        try:
            loop.run_until_complete(ws.send_str(data))
        except Exception:
            logger.debug("WebSocket client disconnected, removing from broadcast")
            disconnected.append(ws)

    for ws in disconnected:
        if ws in clients:
            clients.remove(ws)