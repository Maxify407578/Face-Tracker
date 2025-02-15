import cv2
import threading
import mediapipe as mp

# Funktion zum Initialisieren der Kamera
def initialize_camera(camera_id=0):
    """Initialisiert die Kamera mit der gegebenen ID."""
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Kamera mit ID {camera_id} konnte nicht geöffnet werden.")
        return None
    return cap

# Funktion zur Erkennung von Gesichtern und Gesten
def detect_faces_and_gestures(frame, face_cascade, hands, face_mesh):
    """Erkennt Gesichter und Gesten im gegebenen Frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Bild glätten
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Gestenerkennung
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Rechtecke um Gesichter zeichnen
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rechteck rot

        # Gesichtsmerkmale erkennen
        face_roi = frame[y:y+h, x:x+w]
        face_roi_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        face_results = face_mesh.process(face_roi_rgb)

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, face_landmarks, mp.solutions.face_mesh.FACE_CONNECTIONS)

    # Gesten anzeigen
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if is_ok_gesture(hand_landmarks):
                # Rechteck um die Hand zeichnen
                draw_hand_rectangle(frame, hand_landmarks, (0, 255, 0), 'Geste: OK')
            elif is_heart_gesture(hand_landmarks):
                # Rechteck um die Hand zeichnen
                draw_hand_rectangle(frame, hand_landmarks, (255, 0, 255), 'Geste: Herz')

            # Zeichne die Handlandmarks
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    return len(faces)

def is_ok_gesture(hand_landmarks):
    """Überprüft, ob die Handgeste 'OK' gemacht wird."""
    thumb_tip = hand_landmarks.landmark[4]  # Daumen-Spitze
    index_tip = hand_landmarks.landmark[8]  # Zeigefinger-Spitze
    middle_tip = hand_landmarks.landmark[12]  # Mittelfinger-Spitze

    # Beispielbedingungen für die 'OK'-Geste
    if (thumb_tip.y < index_tip.y) and (index_tip.y < middle_tip.y):
        return True
    return False

def is_heart_gesture(hand_landmarks):
    """Überprüft, ob die Handgeste 'Herz' gemacht wird."""
    # Hier definieren wir die Bedingungen für die 'Herz'-Geste
    # Beispielbedingungen (müssen möglicherweise angepasst werden)
    thumb_tip = hand_landmarks.landmark[4]  # Daumen-Spitze
    index_tip = hand_landmarks.landmark[8]  # Zeigefinger-Spitze
    middle_tip = hand_landmarks.landmark[12]  # Mittelfinger-Spitze
    ring_tip = hand_landmarks.landmark[16]  # Ringfinger-Spitze
    pinky_tip = hand_landmarks.landmark[20]  # Kleiner Finger-Spitze

    # Beispielbedingungen für die 'Herz'-Geste
    if (thumb_tip.y < index_tip.y) and (index_tip.y < middle_tip.y) and (ring_tip.y > middle_tip.y) and (pinky_tip.y > middle_tip.y):
        return True
    return False

def draw_hand_rectangle(frame, hand_landmarks, color, text):
    """Zeichnet ein Rechteck um die Hand und zeigt den Text an."""
    x_min = int(hand_landmarks.landmark[0].x * frame.shape[1])
    y_min = int(hand_landmarks.landmark[0].y * frame.shape[0])
    x_max = int(hand_landmarks.landmark[9].x * frame.shape[1])  # Daumen-Spitze
    y_max = int(hand_landmarks.landmark[9].y * frame.shape[0])
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)  # Rechteck
    cv2.putText(frame, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

# Funktion zum Verarbeiten von Tasteneingaben
def process_key_input():
    """Verarbeitet Tasteneingaben für das Beenden oder Speichern eines Screenshots."""
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        return False
    elif key == ord('s'):  # Screenshot speichern
        return True
    return None

# Funktion zur Verarbeitung von Frames
def process_frames(cap, face_cascade, hands, face_mesh):
    """Verarbeitet die Frames von der Kamera."""
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera konnte nicht gelesen werden. Breche ab.")
            break

        # Reduziere die Bildgröße für schnellere Verarbeitung
        frame = cv2.resize(frame, (640, 480))

        # Erkenne Gesichter und Gesten
        face_count = detect_faces_and_gestures(frame, face_cascade, hands, face_mesh)
        cv2.putText(frame, f'Gesichter erkannt: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Zeige das Bild mit den erkannten Gesichtern und Gesten an
        cv2.imshow('Face Tracker', frame)

        # Tasteneingaben verarbeiten
        key_action = process_key_input()
        if key_action is False:
            break

    # Beende die Webcam und schließe alle Fenster
    cap.release()
    cv2.destroyAllWindows()

# Hauptfunktion
def main():
    """Hauptfunktion zur Ausführung des Face Trackers."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    hands = mp.solutions.hands.Hands()
    face_mesh = mp.solutions.face_mesh.FaceMesh()

    # Initialisiere die Kamera
    cap = initialize_camera(0) or initialize_camera(1)
    if cap is None:
        print("Keine Kamera verfügbar. Programm wird beendet.")
        return

    # Setze die Auflösung
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Starte die Frame-Verarbeitung in einem separaten Thread
    frame_thread = threading.Thread(target=process_frames, args=(cap, face_cascade, hands, face_mesh))
    frame_thread.start()
    frame_thread.join()

# Programmstart
if __name__ == "__main__":
    main()