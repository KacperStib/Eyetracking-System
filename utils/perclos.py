from collections import deque

class Perclos:
    def __init__(self, fps=30, window_sec=60):
        self.buffer = deque(maxlen=fps * window_sec)

    def update(self, eye_closed):
        # eye_closed: 1 lub 0
        self.buffer.append(eye_closed)

    def get_value(self):
        if len(self.buffer) == 0:
            return 0.0
        return sum(self.buffer) / len(self.buffer)