import time

import cv2

from camera import close_camera, open_camera, read_frame
from detection import (
    detect_faces,
    detect_smiles,
    load_face_detector,
    load_smile_detector,
)
from effects import apply_gray_filter, overlay_png
from entities import FallingCircle, SmileBubble
from state import AppState
from ui import draw_menu

FACE_CASCADE_PATH = "assets/haarcascade_frontalface_alt.xml"
SMILE_CASCADE_PATH = "assets/haarcascade_smile.xml"
HAT_PATH = "assets/hat.png"
MASK_PATH = "assets/mask.png"
WINDOW_NAME = "Filtre"


class InteractiveCameraApp:
    def __init__(self):
        self.face_detector = load_face_detector(FACE_CASCADE_PATH)
        self.smile_detector = load_smile_detector(SMILE_CASCADE_PATH)
        self.hat_img = self._load_asset(HAT_PATH)
        self.mask_img = self._load_asset(MASK_PATH)
        self.state = AppState()
        self.circle = None
        self.bubbles = []
        self.last_bubble = 0.0
        self.bubble_cooldown = 0.20

    def run(self):
        cap = open_camera(0)
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_NAME, 1200, 750)
        try:
            while True:
                frame = read_frame(cap)
                processed = self._process_frame(frame)
                cv2.imshow(WINDOW_NAME, processed)
                if not self._handle_keys():
                    break
        finally:
            close_camera(cap)

    def _process_frame(self, frame):
        if self.state.mirror:
            frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]
        self._ensure_circle(width, height)

        if self.state.gray:
            frame = apply_gray_filter(frame)

        faces = detect_faces(frame, self.face_detector)
        circle_color = (255, 0, 0)

        if self.state.drop and self.circle:
            self.circle.update()

        for face in faces:
            circle_color = self._decorate_face(frame, face, circle_color)

        if self.state.drop and self.circle:
            self.circle.draw(frame, circle_color)

        self._update_bubbles(frame)
        draw_menu(frame, self.state)
        return frame

    def _decorate_face(self, frame, face, circle_color):
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (60, 180, 60), 2)
        if self.state.hat:
            hat_w = int(w * 1.25)
            hat_h = int(h * 0.60)
            hat_x = int(x - (hat_w - w) / 2)
            hat_y = int(y - hat_h * 1.00)
            overlay_png(frame, self.hat_img, hat_x, hat_y, hat_w, hat_h)

        if self.state.mask:
            mask_w = int(w * 1.10)
            mask_h = int(h * 0.38)
            mask_x = int(x - (mask_w - w) / 2)
            mask_y = int(y + h * 0.22)
            overlay_png(frame, self.mask_img, mask_x, mask_y, mask_w, mask_h)

        if self.state.drop and self.circle and self.circle.touch_face(face):
            circle_color = (0, 255, 0)

        if self.state.smile:
            self._handle_smile(frame, face)

        return circle_color

    def _handle_smile(self, frame, face):
        x, y, w, h = face
        smiles = detect_smiles(frame, self.smile_detector, face)
        if len(smiles) > 0:
            cv2.putText(frame, "SOURIRE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            now = time.time()
            if now - self.last_bubble > self.bubble_cooldown:
                self.bubbles.append(SmileBubble(x + w * 0.5, y))
                self.last_bubble = now

    def _update_bubbles(self, frame):
        self.bubbles = [b for b in self.bubbles if b.alive()]
        for bubble in self.bubbles:
            bubble.update()
            bubble.draw(frame)

    def _ensure_circle(self, width, height):
        if self.circle is None:
            self.circle = FallingCircle(width, height)
        else:
            self.circle.W, self.circle.H = width, height

    def _handle_keys(self):
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return False

        toggles = {
            ord("g"): "gray",
            ord("h"): "hat",
            ord("m"): "mask",
            ord("d"): "drop",
            ord("s"): "smile",
            ord("r"): "mirror",
        }
        if key in toggles:
            self.state.toggle(toggles[key])
        return True

    @staticmethod
    def _load_asset(path):
        asset = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if asset is None:
            raise FileNotFoundError(f"Image introuvable: {path}")
        return asset


def main():
    InteractiveCameraApp().run()


if __name__ == "__main__":
    main()
