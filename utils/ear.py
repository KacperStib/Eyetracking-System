from scipy.spatial import distance
import numpy as np
import cv2

class EARManager:
    def __init__(self, target_frames=100, default_threshold=0.25):
        self.target_frames = target_frames
        self.ear_values = []
        self.is_calibrated = True
        self.current_threshold = default_threshold
    
    # Prywatna funkcja do liczenia EAR
    @staticmethod
    def calculate_ear(eye):
        if eye is None or len(eye) < 6:
            return 0.0
        # EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
        A = distance.euclidean(eye[1], eye[5])  # p2 - p6
        B = distance.euclidean(eye[2], eye[4])  # p3 - p5
        C = distance.euclidean(eye[0], eye[3])  # p1 - p4
        
        return (A + B) / (2.0 * C)
    
    # Aktualizacja sredniego EAR, EAR manager
    def update(self, left_eye, right_eye, frame):

        l_ear = self.calculate_ear(left_eye)
        r_ear = self.calculate_ear(right_eye)
        avg_ear = (l_ear + r_ear) / 2.0

        if not self.is_calibrated:
            self._run_calibration(avg_ear, frame)
            return avg_ear, True
        
        return avg_ear, False

    def start_calibration(self):
        self.ear_values = []
        self.is_calibrated = False

    def _run_calibration(self, avg_ear, frame):

        if len(self.ear_values) < self.target_frames:
            # Odrzuc klatki w ktorych mrugnieto
            if avg_ear < 0.15:
                return
            self.ear_values.append(avg_ear)
            
            # Wizualizacja na klatce
            h, w = frame.shape[:2]
            progress = int((len(self.ear_values) / self.target_frames) * 100)
            
            color = (0, 255, 255) # Żółty
            msg = f"KALIBRACJA EAR: {progress}%"
            cv2.putText(frame, msg, (w//2 - 120, h//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Pasek postępu
            cv2.rectangle(frame, (w//2 - 100, h//2 + 20), (w//2 + 100, h//2 + 35), (255, 255, 255), 1)
            cv2.rectangle(frame, (w//2 - 100, h//2 + 20), (w//2 - 100 + progress * 2, h//2 + 35), (0, 255, 0), -1)
        else:
            # Finalizacja
            mean_ear = np.mean(self.ear_values)
            # Próg ustawiamy na 75% średniego otwarcia (można dostosować)
            self.current_threshold = mean_ear * 0.75
            self.is_calibrated = True
            print(f"[*] Kalibracja zakończona. Średni EAR: {mean_ear:.3f}, Próg: {self.current_threshold:.3f}")

    def get_threshold(self):
        return self.current_threshold

    def reset(self):
        self.ear_values = []
        self.is_calibrated = False