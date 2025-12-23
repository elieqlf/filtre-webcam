import cv2
import numpy as np
import random
import time
from camera import open_camera, read_frame, close_camera
from detection import load_face_detector, load_smile_detector, detect_faces, detect_smiles
FACE_CASCADE_PATH = "assets/haarcascade_frontalface_alt.xml"
SMILE_CASCADE_PATH = "assets/haarcascade_smile.xml"
HAT_PATH = "assets/hat.png"
MASK_PATH = "assets/mask.png"
WINDOW_NAME = "TD7 : Projet (q quitter)"
# Question 2.a Filtre global
def apply_gray_filter(frame_bgr):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
# Question 2.b  Incrustation 
def overlay_png(frame, png, x, y, w, h):
    if png is None or w <= 0 or h <= 0:
        return frame
    H, W = frame.shape[:2]
    png = cv2.resize(png, (w, h), interpolation=cv2.INTER_AREA)
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x + w), min(H, y + h)
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
# Question 3.a et question 3.b : Rond qui tombe + collision
class FallingCircle:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.reset()
    def reset(self):
        self.x = random.randint(40, max(41, self.W - 40))
        self.y = -30
        self.r = 20
        self.speed = random.randint(5, 8)
    def update(self):
        self.y += self.speed
        if self.y - self.r > self.H:
            self.reset()
    def draw(self, frame, color_bgr):
        cv2.circle(frame, (int(self.x), int(self.y)), self.r, color_bgr, -1)
    def touch_face(self, face_bbox):
        fx, fy, fw, fh = face_bbox
        return (fx <= self.x <= fx + fw) and (fy <= self.y <= fy + fh)
# Question3 .c  Nouvel objet quand on sourit (petits ronds qui montent)
class SmileBubble:
    def __init__(self, x, y):
        self.x = int(x) + random.randint(-15, 15)
        self.y = int(y) + random.randint(-10, 10)
        self.r = random.randint(6, 10)
        self.vy = random.uniform(1.5, 3.0)
        self.birth = time.time()
        self.ttl = 1.2
    def alive(self):
        return (time.time() - self.birth) < self.ttl
    def update(self):
        self.y -= self.vy
    def draw(self, frame):
        cv2.circle(frame, (int(self.x), int(self.y)), self.r, (0, 0, 255), -1)
# question4:  menu interactif
def draw_menu(frame, state):
    lines = [
        "Menu:",
        "  q : quitter",
        "  g : filtre gris ON/OFF",
        "  h : chapeau ON/OFF",
        "  m : lunettes/masque ON/OFF",
        "  d : rond qui tombe ON/OFF",
        "  s : sourire ON/OFF (bulles)",
        "  r : miroir ON/OFF",
    ]
    y = 25
    for t in lines:
        cv2.putText(frame, t, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)
        y += 22
    status = (
        f"Etat -> gris:{state['gray']} chapeau:{state['hat']} masque:{state['mask']} "
        f"drop:{state['drop']} sourire:{state['smile']} miroir:{state['mirror']}"
    )
    cv2.putText(frame, status, (10, frame.shape[0] - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)
#main
def main():
    face_detector = load_face_detector(FACE_CASCADE_PATH)
    smile_detector = load_smile_detector(SMILE_CASCADE_PATH)
    hat_img = cv2.imread(HAT_PATH, cv2.IMREAD_UNCHANGED)
    mask_img = cv2.imread(MASK_PATH, cv2.IMREAD_UNCHANGED)
    if hat_img is None:
        raise FileNotFoundError(f"Image introuvable: {HAT_PATH}")
    if mask_img is None:
        raise FileNotFoundError(f"Image introuvable: {MASK_PATH}")
    state = {
        "gray": False,
        "hat": True,
        "mask": True,
        "drop": True,
        "smile": True,
        "mirror": True,
    }
    cap = open_camera(0)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1200, 750)
    circle = None
    bubbles = []
    last_bubble = 0.0
    bubble_cooldown = 0.20
    try:
        while True:
            frame = read_frame(cap)
            if state["mirror"]:
                frame = cv2.flip(frame, 1)
            H, W = frame.shape[:2]
            if circle is None:
                circle = FallingCircle(W, H)
            else:
                circle.W, circle.H = W, H
            if state["gray"]:
                frame = apply_gray_filter(frame)
            faces = detect_faces(frame, face_detector)
            # Rond qui tombe 
            if state["drop"]:
                circle.update()
            # Couleur par défaut 
            circle_color = (255, 0, 0)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (60, 180, 60), 2)
                # Chapeau
                if state["hat"]:
                    hat_w = int(w * 1.25)
                    hat_h = int(h * 0.60)
                    hat_x = int(x - (hat_w - w) / 2)
                    hat_y = int(y - hat_h * 1.00)
                    overlay_png(frame, hat_img, hat_x, hat_y, hat_w, hat_h)
                # Lunettes/masque
                if state["mask"]:
                    mask_w = int(w * 1.10)
                    mask_h = int(h * 0.38)
                    mask_x = int(x - (mask_w - w) / 2)
                    mask_y = int(y + h * 0.22)
                    overlay_png(frame, mask_img, mask_x, mask_y, mask_w, mask_h)
                # Collision => VERT 
                if state["drop"] and circle.touch_face((x, y, w, h)):
                    circle_color = (0, 255, 0)
                # Sourire => bulles 
                if state["smile"]:
                    smiles = detect_smiles(frame, smile_detector, (x, y, w, h))
                    if len(smiles) > 0:
                        cv2.putText(frame, "SOURIRE", (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        now = time.time()
                        if now - last_bubble > bubble_cooldown:
                            bubbles.append(SmileBubble(x + w * 0.5, y))
                            last_bubble = now
            # Afficher le rond qui tombe
            if state["drop"]:
                circle.draw(frame, circle_color)
            # Afficher bulles
            bubbles = [b for b in bubbles if b.alive()]
            for b in bubbles:
                b.update()
                b.draw(frame)
            draw_menu(frame, state)
            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("g"):
                state["gray"] = not state["gray"]
            elif key == ord("h"):
                state["hat"] = not state["hat"]
            elif key == ord("m"):
                state["mask"] = not state["mask"]
            elif key == ord("d"):
                state["drop"] = not state["drop"]
            elif key == ord("s"):
                state["smile"] = not state["smile"]
            elif key == ord("r"):
                state["mirror"] = not state["mirror"]
    finally:
        close_camera(cap)
if __name__ == "__main__":
    main()
