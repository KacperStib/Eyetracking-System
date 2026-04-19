import csv
import cv2
import time

class Logger:
    def __init__(self,
                 csv_file="logs/log.csv",
                 video_file="logs/output.avi",
                 fps=20,
                 width=640,
                 height=480):

        self.start_time = time.time()

        # .csv
        self.file = open(csv_file, mode='w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["time", "PERCLOS", "blinks", "window_sec"])
        self.last_log_time = time.time()

        # .avi
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(video_file, fourcc, fps, (width, height))

    # zapis danych do CSV
    def log(self, perclos, blinks, window_sec):

        current_time = time.time()

        # zapis co 1 s
        if current_time - self.last_log_time >= 1.0:
            self.writer.writerow([
                round(current_time - self.start_time),
                round(perclos, 3),
                blinks,
                window_sec
            ])
            self.last_log_time = current_time

    # zapis klatki video
    def write_frame(self, frame):
        self.video.write(frame)

    # zamknięcie plików
    def close(self):
        self.file.close()
        self.video.release()