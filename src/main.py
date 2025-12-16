import cv2

from camera import close_camera, open_camera, read_frame
from detection import detect_faces, draw_faces, load_face_detector

CASCADE_PATH = "assets/haarcascade_frontalface_alt.xml"


def main() -> None:
    face_detector = load_face_detector(CASCADE_PATH)
    cap = open_camera()

    try:
        while True:
            frame = read_frame(cap)
            faces = detect_faces(frame, face_detector)
            annotated_frame = draw_faces(frame, faces)
            cv2.imshow("Detection Visage", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        close_camera(cap)


if __name__ == "__main__":
    main()
