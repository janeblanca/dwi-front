import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPixmap, QPen, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout


class BreaktimeSection:
    def __init__(self, painter, width, height):
        self.painter = painter
        self.width = width
        self.height = height

    def paint_breaktime(self):
        pen = QPen(QColor("#FFFFFF"), 0)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor("#FFFFFF"))
        breaktime = QRect(317, 115, 200, 230)
        self.painter.drawRoundedRect(breaktime, 8, 8)

        # small square ICON (Blue Clock)
        self.painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(329, self.height - 593, 50, 50)
        self.painter.drawRoundedRect(square_blue_box, 8, 8)

        # small square
        self.painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(395, self.height - 583, 105, 30)
        self.painter.drawRoundedRect(square_blue_box, 8, 8)

        # Image BLUE clock
        image_blue = QPixmap("./images/blue_clock.png")
        self.painter.drawPixmap(290, self.height - 605, 130, 75, image_blue)

        # --- Texts ---
        font_title = QFont()
        font_title.setPointSize(9)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(413, self.height - 577, 450, 270, Qt.AlignLeft, "Break Time")

        font_title = QFont()
        font_title.setPointSize(7)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#282828"))
        self.painter.drawText(420, 205, 400, 270, Qt.AlignLeft, "mins")

        # Description breaktime
        font_title = QFont()
        font_title.setPointSize(8)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(333, 280, 450, 270, Qt.AlignLeft, "This section shows the")
        self.painter.drawText(333, 297, 450, 270, Qt.AlignLeft, "period of breaks the ")
        self.painter.drawText(333, 314, 450, 270, Qt.AlignLeft, "individuals should take.")
