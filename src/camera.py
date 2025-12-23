import cv2 # Bibliothèque OpenCV
def open_camera(index: int = 0) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(index) # Ouvre la webcam
    if not cap.isOpened():
        raise RuntimeError("Caméra non accessible") # Erreur si webcam indisponible
    return cap  # Retourne la caméra
def read_frame(cap: cv2.VideoCapture):
    ret, frame = cap.read()  #Lit une image depuis la webcam
    if not ret:
        raise RuntimeError("Impossible de lire la frame")# Erreur lecture
    return frame  # Retourne l’image
def close_camera(cap: cv2.VideoCapture):
    cap.release() # Libère la webcam
    cv2.destroyAllWindows() # Ferme les fenêtres
