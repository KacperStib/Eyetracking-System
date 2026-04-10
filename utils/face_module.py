import cv2
import dlib
from imutils import face_utils

# Dlib - detector twarzy i predictor punktow twarzy
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# kamera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

def get_frame_and_eyes():
    ret, frame = cap.read()
    if not ret:
        return None, None, None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    leftEye = None
    rightEye = None

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Punkty z dlib odpowiadajace za oczy
        leftEye = shape[36:42]
        rightEye = shape[42:48]

    return frame, leftEye, rightEye


def release_camera():
    cap.release()