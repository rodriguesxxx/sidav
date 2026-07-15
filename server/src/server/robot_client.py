"""TCP client for communicating with the LEGO EV3 ground robot.

Sends a 'start' command to the robot when fire is detected.
"""

import logging
import socket

from .config import ROBOT_HOST, ROBOT_PORT

logger = logging.getLogger(__name__)


def notify_robot() -> None:
    """Send a 'start' command to the EV3 robot over TCP."""
    message = "start"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((ROBOT_HOST, ROBOT_PORT))
            sock.sendall(message.encode("utf-8"))
            logger.info("Robot notified: '%s' sent to %s:%d", message, ROBOT_HOST, ROBOT_PORT)
    except (ConnectionRefusedError, socket.timeout, OSError) as exc:
        logger.warning("Failed to notify robot at %s:%d: %s", ROBOT_HOST, ROBOT_PORT, exc)