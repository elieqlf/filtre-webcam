import random
import time
import cv2


class FallingCircle:
    def __init__(self, width, height):
        self.W = width
        self.H = height
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
