import cv2
import threading
from PyQt5.QtCore import pyqtSignal, QObject, QSize
from PyQt5.QtGui import QImage
import numpy as np
from FeatureExtraction import HandLandmarksDetector


class Camera(QObject):
    image_data = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(1)
        self.camera_thread = threading.Thread(target=self.stream, daemon=True)
        self.running = False


    def start(self):
        self.running = True
        self.camera_thread.start()

    def stop(self):
        self.running = False
        self.camera_thread.join()

    def stream(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                extract_landmarks = HandLandmarksDetector()
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                landmarks = extract_landmarks.extract_landmarks(frame)
                # converting the landmarks into array of values
                landmarks_arr = np.array(landmarks)
                print(landmarks_arr.shape)

                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_data.emit(qt_image)

    def get_frame_size(self):
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return QSize(width, height)
