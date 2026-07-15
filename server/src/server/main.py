"""Entry point for the SIDAV server.

Starts the camera frame processing pipeline in a background thread and
launches the aiohttp web server.
"""

import logging
import threading

from aiohttp import web

from .camera_handler import handle_frames
from .routes import create_app, frame_queue, serial_clients

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start frame processor thread and run the web server."""
    logger.info("Starting SIDAV server v2.0.0")

    processor = threading.Thread(
        target=handle_frames,
        args=(frame_queue, serial_clients),
        daemon=True,
    )
    processor.start()
    logger.info("Frame processor started")

    app = create_app()
    logger.info("Web server listening on port 8080")
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()