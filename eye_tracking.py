import cv2
import numpy as np

# Import pomocniczych
from utils.face_module import get_frame_and_eyes, release_camera
from utils.ear import eye_aspect_ratio
from utils.perclos import Perclos
from utils.logger import Logger
import time

logger = Logger()

perclos_calc = Perclos(fps=30, window_sec=5)

EAR_THRESHOLD = 0.25

while True:

    # Pobierz pozycje oczu z klatki
    frame, leftEye, rightEye = get_frame_and_eyes()

    if frame is None:
        break

    status = "No Face"

    if leftEye is not None and rightEye is not None:

        # EAR osobno
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        # Srednia z EAR
        ear = (leftEAR + rightEAR) / 2.0

        # Status otwarcia oczu
        if ear < EAR_THRESHOLD:
            status = "Eye Closed"
            eye_closed = 1
            color = (0, 0, 255)
        else:
            status = "Eye Open"
            eye_closed = 0
            color = (0, 255, 0)

        # Perclos
        perclos_calc.update(eye_closed)
        perclos = perclos_calc.get_value()

        # Rysowanie na wykresie
        for (x, y) in np.concatenate((leftEye, rightEye)):
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.putText(frame, status, (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.putText(frame, f"PERCLOS: {perclos:.2f}", (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Eye Tracking System", frame)
    
    # Logi
    logger.write_frame(frame)
    logger.log(time.time(), ear, perclos)

    if cv2.waitKey(1) & 0xFF == 27:
        break

logger.close()
release_camera()
cv2.destroyAllWindows()