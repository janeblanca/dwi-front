import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QSize, QRect, Qt
from PyQt5.QtGui import QImage, QFont, QPixmap, QColor
from plyer import notification
from FeatureExtraction import HandLandmarksDetector


class Camera(QObject):
    image_data = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(1)
        self.camera_thread = QThread()
        self.moveToThread(self.camera_thread)
        self.camera_thread.started.connect(self.stream)
        self.landmarks_detector = HandLandmarksDetector()
        self.running = False

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
                # print(landmarks_arr.shape)

                if landmarks_arr.shape != (126, ):
                    print("Align both hands in the camera")
                    self.show_notification("Align both hands in the camera", " ")
                else:
                    print(landmarks_arr.shape)

                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_data.emit(qt_image)

    def get_frame_size(self):
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return QSize(width, height)

    # def cam_holder(self, painter, parent):
    #     image_cam = QPixmap("./src/cam.png")
    #     image_cam_rect = QRect(parent.width() - 380, 380, 300, 210)
    #     painter.drawPixmap(image_cam_rect, image_cam)
    #     click_font = QFont()
    #     click_font.setPointSize(9)
    #     painter.setFont(click_font)
    #     painter.setPen(QColor("#ffffff"))
    #     painter.drawText(parent.width() - 445, 480, 450, 270, Qt.AlignCenter, "Click to set-up your camera")

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Don't Wrist It",
            timeout=10
        )
