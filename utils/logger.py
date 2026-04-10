import csv
import cv2

class Logger:
    def __init__(self,
                 csv_file="logs/log.csv",
                 video_file="logs/output.avi",
                 fps=20,
                 width=640,
                 height=480):

        # ===== CSV =====
        self.file = open(csv_file, mode='w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["time", "EAR", "PERCLOS"])

        # ===== VIDEO =====
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(video_file, fourcc, fps, (width, height))

    # zapis danych do CSV
    def log(self, t, ear, perclos):
        self.writer.writerow([t, ear, perclos])

    # zapis klatki video
    def write_frame(self, frame):
        self.video.write(frame)

    # zamknięcie plików
    def close(self):
        self.file.close()
        self.video.release()