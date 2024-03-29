import cv2
import numpy as np
import tensorflow as tf
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QSize
from PyQt5.QtGui import QImage
import time
from plyer import notification
import urllib.request
import http
import time
import threading
#import asyncio


from FeatureExtraction import HandLandmarksDetector
from Audio import Audio 


class Camera(QObject):
    image_data = pyqtSignal(QImage)
   

    def __init__(self, cam_index = None):
        super().__init__()
        self.camera = cv2.VideoCapture(cam_index)
        # threading
        self.camera_thread = QThread()
        self.moveToThread(self.camera_thread)
        # connect to stream function for displaying live video
        self.camera_thread.started.connect(self.stream)
        # initializing mediapipe
        self.landmarks_detector = HandLandmarksDetector()
        # initialize model
        self.model = tf.keras.models.load_model('model\lstm_5-new.h5')
        self.running = False

        # initializing audio 
        self.audio = Audio(self)
        # initializing time 
        self.duration = 0 
        self.audio_threshold = 2 * 60 # for 5 minutes
        self.last_frametime = time.time() # initialize the last frame time

        # initializing the notification display
        self.notification_display = False 
        # initializing the display in main window 
        self.audio_holder = False 
        # initializing wrist position display in main waindow 
        self.correct_position = True 
        self.hands_detect = True
        # initializing notification counter
        self.notification_counter = 0
    
    def start(self):
        self.running = True
        self.camera_thread.start()

    def stop(self):
        self.running = False
        self.camera_thread.quit()
        self.camera_thread.wait()

    def stream(self):
        notification_counter = 0
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
                    #self.transfer("0")
                    notification_counter += 1
                    if notification_counter % 500 == 0:
                        self.show_notification("Missing both hands", "Align both hands in the camera")
                    
                    self.notification_display = True
                    self.audio_holder = False 
                    self.hands_detect = False

                else:
                    # print(landmarks_arr.shape)
                    # reshape to fit the model
                    self.hands_detect = True 
                    self.notification_display = False 
                    reshape_landmarks = landmarks_arr.reshape(1, 1, landmarks_arr.shape[0])
                    # feed into the data into the model
                    classify = self.model.predict(reshape_landmarks)

                    # classifying
                    if classify > 0.5:
                        print("Correct position")
                        #self.transfer("0")
                        self.duration = 0
                        self.audio_holder = False
                        self.correct_position = True
                    
                    else: 
                        self.correct_position = False
                        #self.transfer("1")
                        current_time = time.time()
                        time_elapsed = current_time - self.last_frametime
                        self.duration += time_elapsed
                        self.last_frametime = current_time


                        if self.duration >= self.audio_threshold:
                            self.audio.speak_text()
                            self.duration = 0
                            self.audio_holder = True


                # receive and process image data for display
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_data.emit(qt_image)
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

    def transfer(self, data1):
        def send_request():
            try:
                n = urllib.request.urlopen("http://192.168.158.19/" + data1).read()
                n = n.decode("utf-8")
                
            except http.client.HTTPException as e:
                pass 

        # Start a new thread for sending the request
        threading.Thread(target=send_request).start()