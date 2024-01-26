from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPixmap, QPen

class ReminderSection:
    def __init__(self, painter, width, height):
        self.painter = painter
        self.width = width
        self.height = height

    def paint_reminder(self):
        pen = QPen(QColor("#FFFFFF"), 0)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor("#FFFFFF"))
        reminder = QRect(317, 360, self.width - 788, 230)
        self.painter.drawRoundedRect(reminder, 8, 8)

        # Icon
        reminder_icon = QPixmap("./images/notif-icon.png")
        self.painter.drawPixmap(665, self.height - 345, 45, 40, reminder_icon)

        font_title = QFont()
        font_title.setPointSize(11)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(330, 380, 450, 270, Qt.AlignLeft, "Reminders")
