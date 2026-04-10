from collections import deque
import time
import subprocess

class Perclos:
    def __init__(self, fps=30, window_sec=60, threshold=0.4):
        self.buffer = deque(maxlen=fps * window_sec)
        self.threshold = threshold

    def update(self, eye_closed):
        # eye_closed: 1 lub 0
        self.buffer.append(eye_closed)

    def get_value(self):
        if len(self.buffer) == 0:
            return 0.0
        return sum(self.buffer) / len(self.buffer)

    def update_alarm(self):
        perclos = self.get_value()

        if perclos > self.threshold:
            if not self.alarm_active:
                self.alarm_active = True
                self.last_alarm_time = time.time()

                # 🔊 pipnięcie
                subprocess.Popen([
                    "paplay",
                    "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"
                ])

        else:
            self.alarm_active = False

    def is_drowsy(self):
        return self.alarm_active