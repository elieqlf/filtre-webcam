import cv2
import numpy as np


def apply_gray_filter(frame_bgr):
    """Convert to gray while keeping 3 channels for consistent downstream use."""
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def overlay_png(frame, png, x, y, w, h):
    """Overlay a PNG (possibly with alpha) onto the frame at the given position."""
    if png is None or w <= 0 or h <= 0:
        return frame

    frame_h, frame_w = frame.shape[:2]
    png = cv2.resize(png, (w, h), interpolation=cv2.INTER_AREA)
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(frame_w, x + w), min(frame_h, y + h)
    if x1 >= x2 or y1 >= y2:
        return frame

    px1, py1 = x1 - x, y1 - y
    px2, py2 = px1 + (x2 - x1), py1 + (y2 - y1)
    roi = frame[y1:y2, x1:x2]

    if png.shape[2] == 3:
        roi[:] = png[py1:py2, px1:px2]
        frame[y1:y2, x1:x2] = roi
        return frame

    b, g, r, a = cv2.split(png)
    alpha = (a.astype(np.float32) / 255.0)[py1:py2, px1:px2]
    b = b[py1:py2, px1:px2].astype(np.float32)
    g = g[py1:py2, px1:px2].astype(np.float32)
    r = r[py1:py2, px1:px2].astype(np.float32)

    roi_b = roi[:, :, 0].astype(np.float32)
    roi_g = roi[:, :, 1].astype(np.float32)
    roi_r = roi[:, :, 2].astype(np.float32)

    roi[:, :, 0] = (b * alpha + roi_b * (1 - alpha)).astype(np.uint8)
    roi[:, :, 1] = (g * alpha + roi_g * (1 - alpha)).astype(np.uint8)
    roi[:, :, 2] = (r * alpha + roi_r * (1 - alpha)).astype(np.uint8)
    frame[y1:y2, x1:x2] = roi
    return frame
