import numpy as np
import cv2 as cv
import pytest

from server.fire_detector import detect_fire


def _make_solid_frame(hsv_color, width=640, height=480):
    hsv = np.full((height, width, 3), hsv_color, dtype=np.uint8)
    return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)


def _make_orange_frame():
    return _make_solid_frame((5, 200, 200))


def _make_non_fire_frame():
    return _make_solid_frame((60, 100, 100))


class TestFireDetector:

    def test_detects_orange_as_fire(self):
        frame, fire = detect_fire(_make_orange_frame())
        assert fire is True

    def test_ignores_non_fire_colors(self):
        frame, fire = detect_fire(_make_non_fire_frame())
        assert fire is False

    def test_resizes_to_720_width(self):
        original = _make_orange_frame()
        processed, _ = detect_fire(original)
        assert processed.shape[1] == 720
        assert processed.shape[0] > 0

    def test_black_frame_no_fire(self):
        frame, fire = detect_fire(np.zeros((480, 640, 3), dtype=np.uint8))
        assert fire is False

    def test_all_white_no_fire(self):
        frame, fire = detect_fire(np.ones((480, 640, 3), dtype=np.uint8) * 255)
        assert fire is False