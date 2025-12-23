import cv2 #OpenCV
def load_face_detector(cascade_path: str) -> cv2.CascadeClassifier:
    cascade = cv2.CascadeClassifier(cascade_path) # Charge la cascade visage
    if cascade.empty():
        raise FileNotFoundError("Cascade visage introuvable") # Erreur chargement
    return cascade  # Retourne le détecteur
def load_smile_detector(cascade_path: str) -> cv2.CascadeClassifier:
    cascade = cv2.CascadeClassifier(cascade_path) # Charge la cascade sourire
    if cascade.empty():
        raise FileNotFoundError("Cascade sourire introuvable")  # Erreur chargement
    return cascade # Retourne le détecteur
def detect_faces(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Image en niveaux de gris
    faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60)) # Détection visage
    return faces  # Liste des visages détectés
def detect_smiles(frame, smile_cascade, face):
    x, y, w, h = face  # Coordonnées du visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Image grise
    roi = gray[y:y+h, x:x+w]  # Zone du visage
    smiles = smile_cascade.detectMultiScale(roi, 1.7, 20) # Détection sourire
    return smiles  # Liste des sourires
