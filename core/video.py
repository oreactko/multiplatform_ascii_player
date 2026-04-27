import cv2

def open_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    return cap, fps