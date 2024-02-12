import cv2
import numpy as np
import tensorflow as tf
import time
import urllib.request
import http
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QSize
from PyQt5.QtGui import QImage
from plyer import notification

from FeatureExtraction import HandLandmarksDetector
from Audio import Audio

class Camera(QObject):
    image_data = pyqtSignal(QImage)

    def __init__(self, camera_index=None):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_index if camera_index is not None else 0)
        self.camera_thread = QThread()
        self.moveToThread(self.camera_thread)
        self.camera_thread.started.connect(self.stream)
        self.running = False

        # initializing mediapipe
        self.landmarks_detector = HandLandmarksDetector()

        # initializing audio
        self.audio = Audio(self)

        # initializing time
        self.duration = 0
        self.audio_threshold = 1 * 60 # for 5 minutes
        self.last_frametime = time.time() # initialize the last frame time

        # initializing the notification display
        self.notification_display = False

        # initializing the display in main window
        self.audio_holder = False

        # initializing wrist position display in main window
        self.correct_position = True
        self.hands_detect = True

        # initialize model
        self.model = tf.keras.models.load_model('./model/lstm_4-new.h5')

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
                landmarks = self.landmarks_detector.extract_landmarks(frame)
                landmarks_arr = np.array(landmarks)

                if landmarks_arr.shape != (126, ):
                    print("Align both hands in the camera")
                    if not self.notification_display:
                        self.show_notification("Missing both hands", "Align both hands in the camera")
                        self.notification_display = True
                        self.audio_holder = False
                        self.hands_detect = False
                        self.transfer("0")
                else:
                    self.hands_detect = True
                    self.notification_display = False
                    reshape_landmarks = landmarks_arr.reshape(1, 1, landmarks_arr.shape[0])
                    classify = self.model.predict(reshape_landmarks)

                    if classify > 0.5:
                        print("Correct position")
                        self.duration = 0
                        self.audio_holder = False
                        self.correct_position = True
                        self.transfer("0")

                    else:
                        self.correct_position = False
                        current_time = time.time()
                        time_elapsed = current_time - self.last_frametime
                        self.duration += time_elapsed
                        self.last_frametime = current_time
                        self.transfer("1")

                        if self.duration >= self.audio_threshold:
                            self.audio.speak_text()
                            self.duration = 0
                            self.audio_holder = True

                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_data.emit(qt_image)

    def transfer(self, data1):
        try:
            #n = urllib.request.urlopen("http://192.168.100.82/" + data1).read()
            n = urllib.request.urlopen("http://192.168.158.19/" + data1).read()
            n = n.decode("utf-8")
            return n
        except http.client.HTTPException as e:
            return e

    def get_frame_size(self):
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return QSize(width, height)

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Don't Wrist It",
            timeout=10
        )
