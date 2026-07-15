"""HTTP and WebSocket route definitions for the SIDAV server.

Provides:
- Web page serving (Jinja2 template)
- WebSocket endpoint for ESP32-CAM frame ingestion (/api/ws/cam)
- WebSocket endpoint for browser live view (/api/ws/serial)
- Health check (/api/ws/ping)
"""

import logging
from queue import Queue

import jinja2
import aiohttp_jinja2
from aiohttp import web, WSMsgType

from .config import API_PREFIX, FRAME_QUEUE_MAXSIZE

logger = logging.getLogger(__name__)

# Shared state between routes and camera handler
frame_queue: Queue = Queue(maxsize=FRAME_QUEUE_MAXSIZE)
serial_clients: list[web.WebSocketResponse] = []


async def _handle_ping(request: web.Request) -> web.Response:
    return web.Response(text="pong")


async def _handle_ws_cam(request: web.Request) -> web.WebSocketResponse:
    """Handle ESP32-CAM frame ingestion over WebSocket.

    Protocol: START:<cam_id> → BINARY frames → STOP
    On STOP, the accumulated frames are pushed to the processing queue.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    frames: list[bytes] = []
    cam_id: str = ""

    async for message in ws:
        if message.type == WSMsgType.ERROR:
            logger.error("WebSocket error: %s", ws.exception())
            await ws.close()
            break

        if message.type == WSMsgType.TEXT:
            if message.data.startswith("START:"):
                cam_id = message.data.replace("START:", "")
                frames = []
                logger.info("Camera '%s' started sending frames", cam_id)
            elif message.data == "STOP":
                logger.info("Camera '%s' finished frame batch (%d frames)", cam_id, len(frames))
                if frames:
                    frame_queue.put([cam_id, frames])

        elif message.type == WSMsgType.BINARY:
            frames.append(message.data)

    return ws


async def _handle_ws_serial(request: web.Request) -> web.WebSocketResponse:
    """Handle browser client connection for receiving processed frames."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    serial_clients.append(ws)

    logger.info("Serial client connected (total: %d)", len(serial_clients))

    async for message in ws:
        if message.type == WSMsgType.TEXT and message.data == "CLOSE":
            await ws.close()
            break

    serial_clients.remove(ws)
    logger.info("Serial client disconnected (total: %d)", len(serial_clients))
    return ws


@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> dict:
    return {}


def create_app() -> web.Application:
    """Create and configure the aiohttp application."""
    import os

    app = web.Application()

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", "..", "templates")
        ),
    )

    app.add_routes([
        web.get("/", index, name="index"),
        web.get(f"{API_PREFIX}/ws/cam", _handle_ws_cam),
        web.get(f"{API_PREFIX}/ws/serial", _handle_ws_serial),
        web.get(f"{API_PREFIX}/ws/ping", _handle_ping),
    ])

    return app