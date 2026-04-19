import cv2
import numpy as np
import time
import os

# Import pomocniczych
from utils.face_module import get_frame_and_eyes, release_camera
from utils.ear import eye_aspect_ratio
from utils.perclos import Perclos
from utils.logger import Logger
from utils.settings import Settings

# Instancje
logger = Logger()
settings = Settings()

# Okna wideo i ustawienia
cv2.namedWindow("Settings")
cv2.namedWindow("Eye Tracking System")
cv2.setMouseCallback("Settings", settings.mouse)

# Perclos
perclos_calc = Perclos(fps=30, window_sec=5)
last_face_time = time.time()
NO_FACE_RESET_TIME = 5

while True:

    # Pobierz pozycje oczu z klatki
    frame, leftEye, rightEye = get_frame_and_eyes()

    if frame is None:
        break

    status = "No Face"

    # Ustawienia
    ear_threshold = settings.get_ear()
    perclos_threshold = settings.get_perclos()
    window_sec = settings.get_window()

    if perclos_threshold != perclos_calc.threshold:
        perclos_calc.set_threshold(perclos_threshold)

    if window_sec != perclos_calc.window_sec:
        perclos_calc.set_window(30, window_sec)

    if settings.consume_reset():
        perclos_calc.reset()
        continue

    settings_frame = settings.draw()
    cv2.imshow("Settings", settings_frame)

    # Brak twarzy
    if leftEye is None or rightEye is None:

        status = "No Face"

        # reset po 5 sekundach braku twarzy
        if time.time() - last_face_time >= NO_FACE_RESET_TIME:
            perclos_calc.reset()

        cv2.imshow("Eye Tracking System", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        continue

    # Twarz wykryta
    last_face_time = time.time()

    # EAR osobno
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    # Srednia z EAR
    ear = (leftEAR + rightEAR) / 2.0

    # Status otwarcia oczu
    if ear < ear_threshold:
        status = "Eye Closed"
        eye_closed = 1
        color = (0, 0, 255)
    else:
        status = "Eye Open"
        eye_closed = 0
        color = (0, 255, 0)

    # Perclos
    perclos_calc.update(eye_closed)
    perclos_calc.update_alarm()
    perclos = perclos_calc.get_value()
    blinks = perclos_calc.get_blinks()

    # Mruganie jesli alarm
    if perclos_calc.is_drowsy():
        if int(time.time() * 2) % 2 == 0:
            cv2.putText(frame, "DROWSINESS ALERT!",
                        (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        4)

    # Rysowanie na wykresie
    for (x, y) in np.concatenate((leftEye, rightEye)):
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.putText(frame, status, (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.putText(frame, f"PERCLOS: {perclos:.2f}", (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
    cv2.putText(frame, f"Blinks: {blinks}", (30, 120),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Logi
    logger.write_frame(frame)
    logger.log(perclos, blinks, perclos_calc.window_sec)

    cv2.imshow("Eye Tracking System", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

logger.close()
release_camera()
cv2.destroyAllWindows()