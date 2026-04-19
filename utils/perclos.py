from collections import deque
import time
import subprocess

class Perclos:
    def __init__(self, fps=30, window_sec=60, threshold=0.4):
        # Przesuwajace sie okno czasowe
        self.buffer = deque(maxlen=fps * window_sec)            
        self.threshold = threshold
        self.alarm_active = False
        self.window_sec = window_sec
        # Licznik mrugniec
        self.blinks = deque() 
        self.prev_closed = 0

    def update(self, eye_closed):
        # eye_closed: 1 lub 0
        self.buffer.append(eye_closed)

        # wykrycie mrugnięcia
        if eye_closed == 1 and self.prev_closed == 0:
            self.blinks.append(time.time())

        self.prev_closed = eye_closed

    def get_blinks(self):
        current_time = time.time()

        # usuwamy stare mrugnięcia poza oknem
        while self.blinks and (current_time - self.blinks[0] > self.window_sec):
            self.blinks.popleft()

        return len(self.blinks)

    # Wartosc PERCLOS
    def get_value(self):
        if len(self.buffer) == 0:
            return 0.0
        return sum(self.buffer) / len(self.buffer)

    # Alarm w przypadku przekroczenia progu PERCLOS
    def update_alarm(self):
        perclos = self.get_value()

        if perclos > self.threshold:
            if not self.alarm_active:
                self.alarm_active = True
                self.last_alarm_time = time.time()

                # Beep
                subprocess.Popen([
                    "paplay",
                    "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"
                ])

        else:
            self.alarm_active = False

    def is_drowsy(self):
        return self.alarm_active
    
    def set_threshold(self, threshold):
        self.threshold = threshold

    # Zmiana okna czasowego
    def set_window(self, fps, window_sec):
        self.fps = fps
        self.window_sec = window_sec
        self.maxlen = fps * window_sec
        self.buffer = deque(maxlen=self.maxlen)
        self.blinks = deque()

    # Reset przy nacisnieciu RESET
    def reset(self):
        self.buffer.clear()
        self.blinks.clear()
        self.alarm_active = False
        self.prev_closed = 0