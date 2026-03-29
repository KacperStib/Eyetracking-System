import cv2
import dlib
import numpy as np
from imutils import face_utils
from scipy.spatial import distance

# załaduj detector twarzy i predictor punktów
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# uruchom kamerę
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

def eye_aspect_ratio(eye):
    # EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[36:42]
        rightEye = shape[42:48]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # rysowanie punktów na oczach
        for (x, y) in np.concatenate((leftEye, rightEye)):
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # wyświetlanie EAR
        cv2.putText(frame, f"EAR: {ear:.2f}", (30,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Eye EAR Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
