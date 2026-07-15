from ev3dev2.sound import Sound
import subprocess
import time
import os

_sound = Sound()
_sound.set_volume(100)


def play(filepath: str, seconds: float = 0):
    process = subprocess.Popen(
        ["/usr/bin/aplay", "-q", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if seconds > 0:
        time.sleep(seconds)
        _stop_process(process)
    return process


def siren() -> None:
    play("/home/robot/assets/sirene.wav", 30)


def _stop_process(process: subprocess.Popen) -> None:
    os.system(f"kill -2 {process.pid}")