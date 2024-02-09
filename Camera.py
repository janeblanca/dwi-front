import cv2
import numpy as np
import tensorflow as tf
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QSize
from PyQt5.QtGui import QImage
# from plyer import notification
from FeatureExtraction import HandLandmarksDetector
# from Audio import Audio 
# from WristPosition import WristPositionSection


class Camera(QObject):
    image_data = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(1)
        # threading
        self.camera_thread = QThread()
        self.moveToThread(self.camera_thread)
        # connect to stream function for displaying live video
        self.camera_thread.started.connect(self.stream)
        # initializing mediapipe
        self.landmarks_detector = HandLandmarksDetector()
        # initialize model
        self.model = tf.keras.models.load_model('C:/Users/DeLL/OneDrive/Documents/dwi-latest/model/lstm_4-new.h5')
        self.running = False

        # for audio classification 
        # self.audio = Audio(self)

    def start(self):
        self.running = True
        self.camera_thread.start()

    def stop(self):
        self.running = False
        self.camera_thread.quit()
        self.camera_thread.wait()

    def stream(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # extracting landmarks from mediapipe
                landmarks = self.landmarks_detector.extract_landmarks(frame)
                # converting into array for reshaping before feeding into the model
                landmarks_arr = np.array(landmarks)


                # apply error handling
                if landmarks_arr.shape != (126, ):
                    print("Align both hands in the camera")
                else:
                    # print(landmarks_arr.shape)
                    # reshape to fit the model
                    reshape_landmarks = landmarks_arr.reshape(1, 1, landmarks_arr.shape[0])
                    # feed into the data into the model
                    classify = self.model.predict(reshape_landmarks)

                    # classifying
                    if classify > 0.5:
                        print("Correct position")
                    else:
                        print("Incorrect position")
                        # self.audio.speak_text()
                        

                # receive and process image data for display
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_data.emit(qt_image)

    def get_frame_size(self):
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return QSize(width, height)
