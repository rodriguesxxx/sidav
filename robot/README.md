# robot/ — LEGO EV3 Ground Robot

Autonomous ground robot built with LEGO EV3 running ev3dev. Listens for fire detection commands from the central server, navigates to the fire location, and sounds an alert siren.

## Architecture

```
server/ ──TCP──▶ robot/
                  │
                  ├── server: TCP listener (port 65432)
                  ├── movement: differential drive control
                  ├── sound: siren playback via ALSA
                  └── sensors/color_sensor: fire verification
```

## Stack

- LEGO EV3 (31313)
- ev3dev (Debian-based OS)
- Python 3
- python-ev3dev2 (motors, sensors, sound)
- ALSA aplay (WAV playback)

## Hardware

| Component | Port | Purpose |
|-----------|------|---------|
| Large Motor | OUTPUT_A | Left wheel |
| Large Motor | OUTPUT_B | Right wheel |
| Color Sensor | INPUT_1 | Fire verification (orange detection) |
| Speaker | built-in | Siren alert |

## Project Structure

```
robot/
├── README.md
├── requirements.txt
└── src/robot/
    ├── __init__.py
    ├── main.py              ← Entry point (keep-alive loop)
    ├── server.py            ← TCP server + navigation planner
    ├── movement.py           ← Differential drive API
    ├── sound.py              ← Siren playback
    └── sensors/
        └── color_sensor.py  ← Color detection
```

## Setup

### 1. Flash ev3dev

Download and flash ev3dev to a microSD card:
https://www.ev3dev.org/downloads/

### 2. Install dependencies

```bash
# On the EV3 (via SSH)
sudo apt-get update
pip3 install python-ev3dev2
```

### 3. Deploy code

```bash
# From your computer
scp -r robot/src robot@192.168.0.100:~/
```

### 4. Add siren audio

```bash
# On the EV3
mkdir -p /home/robot/assets
# Copy sirene.wav to /home/robot/assets/
```

## Running

```bash
# On the EV3
cd ~/src
python3 -m robot.main
```

The robot listens on port 65432 for a `start` command.

## Navigation Plan

On receiving `start`, the robot executes a pre-programmed path:

1. Forward 5 seconds
2. Turn left (~90°)
3. Forward 3.8 seconds
4. If color sensor doesn't detect orange:
   - Backward 1.5 seconds
   - Wide left turn
   - Forward 3.5 seconds
5. Sound siren for 30 seconds

Edit `NAVIGATION_PLAN` in `server.py` to adjust the path.

## Movement API

```python
from robot import movement

movement.forward(speed=30, seconds=5)
movement.backward(speed=30, seconds=2)
movement.turn_left(speed=20)
movement.turn_right(speed=20)
movement.stop()
```

## Siren Audio

Uses ALSA `aplay` to play a WAV file. Default path: `/home/robot/assets/sirene.wav`.

```python
from robot import sound

sound.siren()  # plays sirene.wav for 30 seconds
```