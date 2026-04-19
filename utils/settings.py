import cv2
import numpy as np

class Settings:
    def __init__(self):
        # Defaultowe wartosci
        self.ear = 0.25
        self.perclos = 0.40
        self.window = 5

        self.dragging = None  # sldier dragger
        self.reset_clicked = False

    # Reset parametrow
    def reset(self):
        self.ear = 0.25
        self.perclos = 0.40
        self.window = 5

    def draw(self):
        # Okno ustawien
        frame = np.zeros((260, 600, 3), dtype=np.uint8)

        # Slidery ustawien
        self.draw_slider(frame, "EAR", 0.1, 0.5, self.ear, 50)
        self.draw_slider(frame, "PERCLOS", 0.0, 1.0, self.perclos, 100)
        self.draw_slider(frame, "WINDOW", 1, 60, self.window, 150)

        # Reset btn
        self.reset_rect = (100, 180, 250, 220)
        x1, y1, x2, y2 = self.reset_rect
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, "RESET", (130, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        return frame

    def draw_slider(self, frame, name, min_val, max_val, value, y):
        x1, x2 = 50, 300

        # linia
        cv2.line(frame, (x1, y), (x2, y), (200, 200, 200), 3)

        # pozycja suwaka
        pos = int(x1 + (value - min_val) / (max_val - min_val) * (x2 - x1))

        # kółko
        cv2.circle(frame, (pos, y), 8, (0, 255, 255), -1)

        # tekst
        cv2.putText(frame, f"{name}: {value:.2f}", (320, y+5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # Detekcja nacisniecia
    def mouse(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            # RGuzik reset
            x1, y1, x2, y2 = self.reset_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.reset()
                self.reset_clicked = True
                return

            # sliders
            if 40 < y < 60:
                self.dragging = "ear"
            elif 90 < y < 110:
                self.dragging = "perclos"
            elif 140 < y < 160:
                self.dragging = "window"

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = None

        elif event == cv2.EVENT_MOUSEMOVE and self.dragging:
            val = (x - 50) / (300 - 50)
            val = max(0, min(1, val))

            if self.dragging == "ear":
                self.ear = 0.1 + val * (0.5 - 0.1)

            elif self.dragging == "perclos":
                self.perclos = val

            elif self.dragging == "window":
                self.window = int(1 + val * (60 - 1))

    # Przeprowadz reset w main
    def consume_reset(self):
        if self.reset_clicked:
            self.reset_clicked = False
            return True
        return False

    # Getters
    def get_ear(self):
        return self.ear

    def get_perclos(self):
        return self.perclos

    def get_window(self):
        return self.window