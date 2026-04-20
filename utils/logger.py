import csv
import cv2
import time
import numpy as np
import collections

class Logger:
    def __init__(self,
                 csv_file="logs/log.csv",
                 video_file="logs/output.avi",
                 fps=20,
                 width=640,
                 height=480):

        self.width = width
        self.height = height
        self.start_time = time.time()

        # .csv
        self.file = open(csv_file, mode='w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["time", "PERCLOS", "blinks", "window_sec"])
        self.last_log_time = time.time()

        # .avi
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(video_file, fourcc, fps, (width, height))

        # Wykres
        self.perclos_history = collections.deque(maxlen=200)

    # Zapis danych do CSV
    def log(self, perclos, blinks, window_sec):

        current_time = time.time()

        # Zapis co 1 s
        if current_time - self.last_log_time >= 1.0:
            self.writer.writerow([
                round(current_time - self.start_time),
                round(perclos, 3),
                blinks,
                window_sec
            ])
            self.last_log_time = current_time

    # Zapis klatki video
    def write_frame(self, frame):
        if self.video is not None:
            # Dynamiczne dopasowanie rozmiaru
            h, w = frame.shape[:2]
            if (w, h) != (self.width, self.height):
                frame = cv2.resize(frame, (self.width, self.height))
            self.video.write(frame)

    # Zamknięcie plików
    def close(self):
        self.file.close()
        self.video.release()

    # Logi na wykresie
    def draw_info(self, frame, leftEye, rightEye, ear, status, color, perclos, blinks, perclos_threshold):

        # Polprzezroczyste OSD
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (250, 150), (40, 40, 40), -1) 
        alpha = 0.6  
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Punkty oczu
        if leftEye is not None and rightEye is not None:
            for (x, y) in np.concatenate((leftEye, rightEye)):
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # Font
        font = cv2.FONT_HERSHEY_DUPLEX 
        f_size = 0.6
        f_color = (240, 240, 240)
        thick = 1

        # OSD
        # EAR i Stan 
        state_label = "CLOSED" if "Closed" in status else "OPEN"
        text_color = (0, 0, 255) if state_label == "CLOSED" else f_color
        cv2.putText(frame, f"EYES: {ear:.2f} [{state_label}]", (20, 40),
                    font, f_size, text_color, thick)

        # PERCLOS 
        cv2.putText(frame, f"PERCLOS: {perclos*100:.1f}%", (20, 75),
                    font, f_size, f_color, thick)

        # Mrugnięcia
        cv2.putText(frame, f"BLINK COUNT: {blinks}", (20, 110),
                    font, f_size, f_color, thick)

        # Pasek wizualny dla PERCLOS 
        cv2.rectangle(frame, (20, 130), (230, 135), (100, 100, 100), -1)
        ratio = min(perclos / perclos_threshold, 1.0) if perclos_threshold > 0 else 0
        bar_w = int(210 * ratio)
        bar_color = (0, 0, 255) if perclos > 0.4 else (0, 255, 0)
        cv2.rectangle(frame, (20, 130), (20 + bar_w, 135), bar_color, -1)
        
        # WYkres PERCLOS
        self.perclos_history.append(perclos)
        self.draw_perclos_graph(frame, perclos_threshold)

        return frame

    # Wykres historyczyny PERCLOS
    def draw_perclos_graph(self, frame_to_draw, perclos_threshold):
        graph_h, graph_w = 80, 200
        margin = 15
        x_start = self.width - graph_w - margin
        y_end = self.height - margin
        y_start = y_end - graph_h

        # Tło wykresu 
        overlay = frame_to_draw.copy()
        cv2.rectangle(overlay, (x_start - 5, y_start - 5), 
                      (self.width - margin + 5, y_end + 15), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, frame_to_draw, 0.3, 0, frame_to_draw)

        # Rysowanie osi
        cv2.line(frame_to_draw, (x_start, y_start), (x_start, y_end), (150, 150, 150), 1) # Y
        cv2.line(frame_to_draw, (x_start, y_end), (self.width - margin, y_end), (150, 150, 150), 1) # X

        # Dynamiczna Linia Threshold 
        thresh_y = int(y_end - (perclos_threshold * graph_h))
        if y_start <= thresh_y <= y_end:
            cv2.line(frame_to_draw, (x_start, thresh_y), (self.width - margin, thresh_y), (0, 0, 255), 1)
    
        # Rysowanie linii trendu
        if len(self.perclos_history) > 1:
            points = []
            for i, val in enumerate(self.perclos_history):
                px = int(x_start + i * (graph_w / 200))
                py = int(y_end - (val * graph_h))
                points.append((px, py))
            
            for i in range(1, len(points)):
                cv2.line(frame_to_draw, points[i-1], points[i], (0, 255, 255), 1)