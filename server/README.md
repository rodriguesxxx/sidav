# server/ — Central Server

Backend for the SIDAV fire detection system. Receives drone camera frames via WebSocket, processes them with OpenCV for fire detection, and orchestrates the ground robot response.

## Architecture

```
ESP32-CAM ──WebSocket──▶ server ──TCP──▶ EV3 Robot
                          │
                          ├── OpenCV fire detection (HSV orange segmentation)
                          ├── Frame broadcast to browser dashboard
                          └── Robot notification on fire detection
```

## Stack

- Python 3.10+
- aiohttp (async HTTP + WebSocket)
- OpenCV (computer vision)
- Jinja2 (HTML templates)
- imutils (image utilities)

## Project Structure

```
server/
├── README.md
├── requirements.txt
├── src/server/
│   ├── __init__.py
│   ├── config.py           ← HSV ranges, IPs, ports, thresholds
│   ├── fire_detector.py    ← Orange color segmentation + contour detection
│   ├── camera_handler.py   ← Frame decoding, detection pipeline, broadcast
│   ├── robot_client.py     ← TCP client for EV3 notification
│   ├── routes.py           ← aiohttp app, HTTP + WebSocket routes
│   └── main.py             ← Entry point
├── templates/
│   └── index.html          ← Live view dashboard
└── tests/
    ├── test_fire_detector.py
    └── test_routes.py
```

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
PYTHONPATH=src python3 -m server.main
```

Server starts on `http://0.0.0.0:8080`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Dashboard with live camera feed |
| `GET` | `/api/ws/ping` | Health check — returns `pong` |
| `WS` | `/api/ws/cam` | ESP32-CAM frame ingestion |
| `WS` | `/api/ws/serial` | Browser live view stream |

## WebSocket Protocol

### Camera Ingestion (`/api/ws/cam`)

ESP32-CAM sends frames in batches:

```
TEXT: START:drone
BINARY: <jpeg bytes>
BINARY: <jpeg bytes>
...
TEXT: STOP
```

On `STOP`, accumulated frames are pushed to the processing queue.

### Live View (`/api/ws/serial`)

Browser receives base64-encoded JPEG frames after fire detection processing.

## Fire Detection

Uses HSV color space segmentation targeting orange hues:

- `ORANGE_LOWER`: (0, 120, 70)
- `ORANGE_UPPER`: (10, 255, 255)

Morphological operations (erode + dilate) reduce noise. Contours above minimum area trigger detection.

## Configuration

All constants in `src/server/config.py`:

```python
ROBOT_HOST = "192.168.0.100"
ROBOT_PORT = 65432
SERVER_PORT = 8080
ORANGE_LOWER = (0, 120, 70)
ORANGE_UPPER = (10, 255, 255)
FRAME_QUEUE_MAXSIZE = 10
```

## Testing

```bash
pip install pytest pytest-aiohttp
PYTHONPATH=src python3 -m pytest tests/ -v
```

## Quality

- Cyclomatic complexity: all functions ≤ 8 (limit: 10)
- Measured with `radon cc`