"""Fire detection using HSV color segmentation and contour analysis.

Detects fire in a video frame by isolating orange regions via HSV thresholding,
morphological filtering, and contour detection.
"""

import logging
from typing import Optional

import cv2 as cv
import imutils
import numpy as np

from .config import (
    BLACK,
    ERODE_ITERATIONS,
    DILATE_ITERATIONS,
    ORANGE_LOWER,
    ORANGE_UPPER,
)

logger = logging.getLogger(__name__)


def detect_fire(frame: np.ndarray) -> tuple[np.ndarray, bool]:
    """Process a frame and detect fire using orange HSV segmentation.

    Args:
        frame: BGR image as numpy array.

    Returns:
        Tuple of (annotated_frame, fire_detected).
        annotated_frame has bounding boxes drawn on detected fire regions.
    """
    frame = imutils.resize(frame, width=720)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, ORANGE_LOWER, ORANGE_UPPER)
    mask = cv.erode(mask, None, iterations=ERODE_ITERATIONS)
    mask = cv.dilate(mask, None, iterations=DILATE_ITERATIONS)

    fire_detected = _process_contours(frame, mask)

    return frame, fire_detected


def _process_contours(frame: np.ndarray, mask: np.ndarray) -> bool:
    """Find the largest orange contour and annotate the frame.

    Returns True if at least one contour was found.
    """
    contours = cv.findContours(
        mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )[-2]

    if not contours:
        return False

    largest = max(contours, key=cv.contourArea)
    rect = cv.minAreaRect(largest)
    box = cv.boxPoints(rect)
    box = np.int32(box)

    moments = cv.moments(largest)
    center = _compute_center(moments)
    label = "Fire Detected" if center else None

    cv.drawContours(frame, [box], 0, ORANGE_UPPER, 2)

    if center and label:
        cv.putText(
            frame, label,
            (center[0] - 80, center[1] - 10),
            cv.FONT_HERSHEY_SIMPLEX, 0.6, BLACK, 2,
        )

    return True


def _compute_center(moments: dict) -> Optional[tuple[int, int]]:
    """Compute centroid from image moments. Returns None if area is zero."""
    area = moments.get("m00", 0)
    if area == 0:
        return None
    cx = int(moments["m10"] / area)
    cy = int(moments["m01"] / area)
    return (cx, cy)