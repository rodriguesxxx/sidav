# drone/ — ESP32-CAM Firmware

Firmware for the AI-Thinker ESP32-CAM board. Captures images from the OV2640 camera and streams them over WiFi to the central server via WebSocket.

## Architecture

```
OV2640 Camera ──▶ ESP32 ──WiFi──▶ WebSocket ──▶ server/
                  │
                  ├── Camera: frame capture + JPEG encoding
                  ├── WiFiManager: network connection
                  └── WebSocketClient: frame streaming
```

## Stack

- ESP32-CAM (AI-Thinker)
- PlatformIO
- Arduino Framework
- links2004/WebSockets
- esp32-camera

## Pin Mapping (ESP32-CAM)

| Signal | GPIO |
|--------|------|
| XCLK | 0 |
| PCLK | 22 |
| VSYNC | 25 |
| HREF | 23 |
| SIOD | 26 |
| SIOC | 27 |
| Y2-Y9 | 5, 18, 19, 21, 36, 39, 34, 35 |
| PWDN | 32 |
| RESET | -1 |

## Project Structure

```
drone/
├── README.md
├── platformio.ini
├── src/
│   ├── main.cpp              ← Entry point
│   ├── Camera.cpp            ← OV2640 init + frame capture
│   ├── WiFiManager.cpp       ← WiFi connection
│   └── WebSocketClient.cpp   ← WebSocket client
└── include/
    ├── Camera.h
    ├── WiFiManager.h
    └── WebSocketClient.h
```

## Setup

### 1. Configure WiFi

Edit `src/main.cpp`:

```cpp
WiFiManager wifi("YOUR_SSID", "YOUR_PASSWORD");
```

### 2. Configure Server IP

Edit `src/WebSocketClient.cpp` default constructor:

```cpp
WebSocketClient::WebSocketClient()
    : ip("192.168.0.101"), port(8080), route("/api/ws") {}
```

## Build and Flash

```bash
# Install PlatformIO
pip install platformio

# Build
cd drone
pio run

# Upload to ESP32-CAM
pio run --target upload

# Monitor serial
pio device monitor
```

## Camera Configuration

- Resolution: SVGA (800×600)
- Quality: 20 (JPEG compression)
- Frequency: 20 MHz XCLK
- Format: JPEG

Adjust in `Camera.cpp`:

```cpp
config.frame_size = FRAMESIZE_SVGA;
config.jpeg_quality = 20;
```

## WebSocket Protocol

Each frame is sent as a batch:

```
START:<camera_id>
<binary JPEG frame>
STOP
```

The server accumulates frames between START/STOP and processes them as a batch.