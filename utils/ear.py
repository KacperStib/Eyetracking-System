from scipy.spatial import distance

def eye_aspect_ratio(eye):
    # EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    A = distance.euclidean(eye[1], eye[5])  # p2 - p6
    B = distance.euclidean(eye[2], eye[4])  # p3 - p5
    C = distance.euclidean(eye[0], eye[3])  # p1 - p4
    
    return (A + B) / (2.0 * C)