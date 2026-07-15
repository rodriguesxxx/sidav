from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
import time

_left = LargeMotor(OUTPUT_A)
_right = LargeMotor(OUTPUT_B)


def forward(speed: int = 30, seconds: float = 0) -> None:
    _left.on(SpeedPercent(speed), block=False)
    _right.on(SpeedPercent(speed + 0.5), block=False)
    if seconds > 0:
        time.sleep(seconds)
        stop()


def backward(speed: int = 30, seconds: float = 0) -> None:
    _left.on(SpeedPercent(-speed), block=False)
    _right.on(SpeedPercent(-(speed + 0.5)), block=False)
    if seconds > 0:
        time.sleep(seconds)
        stop()


def turn_left(speed: int = 20, duration: float = 1.83) -> None:
    _left.on_for_seconds(SpeedPercent(-speed), duration, block=False)
    _right.on_for_seconds(SpeedPercent(speed), duration, block=True)


def turn_left_wide(speed: int = 20, duration: float = 1.95) -> None:
    _left.on_for_seconds(SpeedPercent(-speed), duration, block=False)
    _right.on_for_seconds(SpeedPercent(speed), duration, block=True)


def turn_right(speed: int = 20, duration: float = 1.83) -> None:
    _left.on_for_seconds(SpeedPercent(speed), duration, block=False)
    _right.on_for_seconds(SpeedPercent(-speed), duration, block=True)


def stop() -> None:
    _left.off()
    _right.off()