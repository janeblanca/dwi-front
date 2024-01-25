import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPixmap, QPen


class BreakIntervalSection:
    def __init__(self, painter, width, height):
        self.painter = painter
        self.width = width
        self.height = height

    def paint_break_interval(self):
        pen = QPen(QColor("#FFFFFF"), 0)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor("#FFFFFF"))
        breakinterval = QRect(529, 115, 200, 230)
        self.painter.drawRoundedRect(breakinterval, 8, 8)

        # small square ICON (Yellow Clock)
        self.painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(540, self.height - 593, 50, 50)
        self.painter.drawRoundedRect(square_yellow_box, 8, 8)

        # small square(Break Interval)
        self.painter.setBrush(QColor("#FFF7AE"))
        square_yellow_box = QRect(607, self.height - 583, 105, 30)
        self.painter.drawRoundedRect(square_yellow_box, 8, 8)

        # Image YELLOW clock
        image_yellow = QPixmap("./images/yellow_clock.png")
        self.painter.drawPixmap(500, self.height - 605, 130, 75, image_yellow)

        # --- Texts ---
        font_title = QFont()
        font_title.setPointSize(9)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(613, self.height - 577, 450, 270, Qt.AlignLeft, "Break Interval")

        font_title = QFont()
        font_title.setPointSize(7)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#282828"))
        self.painter.drawText(630, 205, 400, 270, Qt.AlignLeft, "mins")

        # Descrption breakinterval
        font_title = QFont()
        font_title.setPointSize(8)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(545, 280, 450, 270, Qt.AlignLeft, "This section shows how")
        self.painter.drawText(545, 297, 450, 270, Qt.AlignLeft, "often breaks should be")
        self.painter.drawText(545, 314, 450, 270, Qt.AlignLeft, "taken.")
