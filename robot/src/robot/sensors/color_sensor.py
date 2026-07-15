from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

_sensor = ColorSensor(INPUT_1)

COLORS = {0: "unknown", 1: "black", 5: "orange"}


def read() -> str:
    return COLORS.get(_sensor.color, "unknown")