import cv2


def open_camera(index: int = 0) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Caméra non accessible")
    return cap


def read_frame(cap: cv2.VideoCapture):
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Impossible de lire la frame")
    return frame


def close_camera(cap: cv2.VideoCapture):
    cap.release()
    cv2.destroyAllWindows()
