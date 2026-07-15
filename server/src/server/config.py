"""Central configuration for the SIDAV server.

All constants, thresholds, IP addresses, and HSV color ranges are defined here.
No hardcoded values should exist in logic modules.
"""

from typing import Final

# --- Network ---
SERVER_HOST: Final[str] = "0.0.0.0"
SERVER_PORT: Final[int] = 8080

ROBOT_HOST: Final[str] = "192.168.0.100"
ROBOT_PORT: Final[int] = 65432

# --- API Routes ---
API_PREFIX: Final[str] = "/api"

# --- Camera ---
CAMERA_WIDTH: Final[int] = 720
DEFAULT_WEBCAM_INDEX: Final[int] = 0

# --- Fire Detection (HSV color ranges) ---
ORANGE_LOWER: Final[tuple[int, int, int]] = (0, 120, 70)
ORANGE_UPPER: Final[tuple[int, int, int]] = (10, 255, 255)

DARK_BLUE_LOWER: Final[tuple[int, int, int]] = (100, 150, 0)
DARK_BLUE_UPPER: Final[tuple[int, int, int]] = (140, 255, 255)

GREEN_LOWER: Final[tuple[int, int, int]] = (35, 100, 100)
GREEN_UPPER: Final[tuple[int, int, int]] = (85, 255, 255)

BLACK: Final[tuple[int, int, int]] = (0, 0, 0)
WHITE: Final[tuple[int, int, int]] = (255, 255, 255)

# --- Morphological Operations ---
ERODE_ITERATIONS: Final[int] = 2
DILATE_ITERATIONS: Final[int] = 2

# --- Camera Frame Queue ---
FRAME_QUEUE_MAXSIZE: Final[int] = 10