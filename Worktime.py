import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPixmap


class WorktimeSection:
    def __init__(self, painter, width, height):
        self.painter = painter
        self.width = width
        self.height = height

    def paint_worktime(self):
        self.painter.setBrush(QColor("#FFFFFF"))
        worktime = QRect(105, 115, 200, 230)
        self.painter.drawRoundedRect(worktime, 8, 8)

        # small square ICON (Green Clock)
        self.painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(119, self.height - 593, 50, 50)
        self.painter.drawRoundedRect(square_green_box, 8, 8)

        # small square (Worktime)
        self.painter.setBrush(QColor("#D0FFCF"))
        square_green_box = QRect(185, self.height - 583, 105, 30)
        self.painter.drawRoundedRect(square_green_box, 8, 8)

        # Image GREEN clock
        image_green = QPixmap("./images/green_clock.png")
        self.painter.drawPixmap(80, self.height - 605, 130, 75, image_green)

        font_title = QFont()
        font_title.setPointSize(9)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(
            203, self.height - 577, 450, 270, Qt.AlignLeft, "Work Time"
        )

        # Description worktime
        font_title = QFont()
        font_title.setPointSize(8)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(
            122, 280, 450, 270, Qt.AlignLeft, "This section presents the"
        )
        self.painter.drawText(
            122, 297, 450, 270, Qt.AlignLeft, "duration of engagement"
        )
        self.painter.drawText(122, 314, 450, 270, Qt.AlignLeft, "in your work.")

        font_counter = QFont()
        font_counter.setPointSize(10)
        self.painter.setFont(font_counter)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(140, 200, 150, 30, Qt.AlignLeft, "Total Work Time:")