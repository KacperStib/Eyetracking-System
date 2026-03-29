import cv2

# załaduj klasyfikatory
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# uruchom kamerę
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Nie można otworzyć kamery")
    exit()

while True:

    ret, frame = cap.read()
    if not ret:
        print("Nie można pobrać obrazu")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # wykrywanie twarzy
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        # prostokąt twarzy
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # wykrywanie oczu
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:

            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex+ew, ey+eh),
                (0,255,0),
                2
            )

    # wyświetlanie obrazu
    cv2.imshow("Eye Detection", frame)

    # ESC kończy program
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
