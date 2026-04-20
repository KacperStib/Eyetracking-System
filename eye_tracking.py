import cv2
import numpy as np
import time
import os

# Import pomocniczych
from utils.face_module import get_frame_and_eyes, release_camera
from utils.perclos import Perclos
from utils.logger import Logger
from utils.settings import Settings
from utils.ear import EARManager

# Instancje
logger = Logger()
settings = Settings()
ear_manager = EARManager(target_frames=100)

# Okna wideo i ustawienia
cv2.namedWindow("Settings")
cv2.namedWindow("Eye Tracking System")
cv2.setMouseCallback("Settings", settings.mouse)

# Perclos
perclos_calc = Perclos(window_sec=5)
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

    # Perclos treshold
    if perclos_threshold != perclos_calc.threshold:
        perclos_calc.set_threshold(perclos_threshold)

    # Dlugosc okna czasowego
    if window_sec != perclos_calc.window_sec:
        perclos_calc.set_window(30, window_sec)

    # Reset
    if settings.consume_reset():
        perclos_calc.reset()
        continue
    
    # Kalibracja
    if settings.consume_calibrate():
        ear_manager.start_calibration()

    # Aktualizacja suwaka po kalibracji
    if ear_manager.is_calibrated and len(ear_manager.ear_values) == ear_manager.target_frames:
        new_val = ear_manager.get_threshold()
        settings.ear = new_val 
        ear_manager.ear_values = [] 

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

    # Wyliczanie EAR i Kalibracja (jesli wymagana)
    ear, calibrating = ear_manager.update(leftEye, rightEye, frame)

    if calibrating:
        cv2.imshow("Eye Tracking System", frame)
        if cv2.waitKey(1) & 0xFF == 27: break
        continue

    # Pobierz dynamiczny próg
    ear_threshold = ear_manager.get_threshold()

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
    frame = logger.draw_info(frame, leftEye, rightEye, ear, status, color, perclos, blinks, perclos_threshold=perclos_calc.threshold)
    
    # Logi
    logger.write_frame(frame)
    logger.log(perclos, blinks, perclos_calc.window_sec)

    cv2.imshow("Eye Tracking System", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

logger.close()
release_camera()
cv2.destroyAllWindows()