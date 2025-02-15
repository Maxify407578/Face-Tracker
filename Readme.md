# Face Tracker

Dieses Projekt ist ein Gesichts- und Gestenerkennungssystem, das die OpenCV- und Mediapipe-Bibliotheken verwendet. Es ermöglicht die Erkennung von Gesichtern und spezifischen Handgesten in Echtzeit über eine Webcam.

## Funktionen

- **Gesichtserkennung**: Das System erkennt Gesichter in einem Video-Stream und zeichnet Rechtecke um die erkannten Gesichter.
- **Gestenerkennung**: Es erkennt zwei spezifische Handgesten:
  - **OK-Geste**: Die Hand zeigt die "OK"-Geste an.
  - **Herz-Geste**: Die Hand zeigt die "Herz"-Geste an.
- **Echtzeit-Video**: Das System zeigt den Video-Stream mit den erkannten Gesichtern und Gesten an.
- **Screenshot-Funktion**: Möglichkeit, einen Screenshot des aktuellen Frames zu speichern.

## Voraussetzungen

- Python 3.x
- OpenCV
- Mediapipe

## Installation

1. Klone das Repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Installiere die erforderlichen Pakete:
   ```bash
   pip install opencv-python mediapipe
   ```

## Verwendung

1. Stelle sicher, dass eine Webcam angeschlossen ist.
2. Führe das Skript aus:
   ```bash
   python face_tracker.py
   ```

3. Drücke `q`, um das Programm zu beenden, oder `s`, um einen Screenshot zu speichern.

## Code-Überblick

- **initialize_camera(camera_id)**: Initialisiert die Kamera mit der angegebenen ID.
- **detect_faces_and_gestures(frame, face_cascade, hands, face_mesh)**: Erkennt Gesichter und Gesten im gegebenen Frame.
- **is_ok_gesture(hand_landmarks)**: Überprüft, ob die Handgeste "OK" gemacht wird.
- **is_heart_gesture(hand_landmarks)**: Überprüft, ob die Handgeste "Herz" gemacht wird.
- **draw_hand_rectangle(frame, hand_landmarks, color, text)**: Zeichnet ein Rechteck um die Hand und zeigt den Text an.
- **process_key_input()**: Verarbeitet Tasteneingaben für das Beenden oder Speichern eines Screenshots.
- **process_frames(cap, face_cascade, hands, face_mesh)**: Verarbeitet die Frames von der Kamera.
- **main()**: Hauptfunktion zur Ausführung des Face Trackers.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
