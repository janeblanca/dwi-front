import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QIntValidator


from Worktime import WorktimeSection
from Breaktime import BreaktimeSection
from Breakinterval import BreakIntervalSection


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.main_window()

        # Disable maximized window
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        #  Break time user input display section
        self.user_input_break = QLineEdit(self)
        self.user_input_break.setGeometry(355, 195, 50, 30)
        self.user_input_break.setStyleSheet("background-color: #f3f1ec; border: none; color: #303030; font-size: 14px;")
        self.user_input_break.setValidator(QIntValidator())

        # Break interval user input display section
        self.user_input_breakint = QLineEdit(self)
        self.user_input_breakint.setGeometry(565, 195, 50, 30)
        self.user_input_breakint.setStyleSheet(
            "background-color: #f3f1ec; border: none; color: #303030; font-size: 14px;")
        self.user_input_break.setValidator(QIntValidator())

    def main_window(self):
        self.setWindowTitle("Don't Wrist It")
        self.setStyleSheet("background-color: #f3f1ec; border-radius: 20px;")
        self.setFixedSize(1200, 720)

    def paintEvent(self, event):
        painter = QPainter(self)

        # LEFT PANE
        pen = QPen(QColor("#e8e7e7"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#e8e7e7"))
        painter.drawRect(0, 0, 80, self.height())

        # CAMERA PANE
        painter.setBrush(QColor("#828E82"))
        painter.drawRect(self.width() - 450, 0, 450, self.height())

        # Logo
        image_logo = QPixmap("./images/logo.png")
        image_logo_x = self.width() - 450 + (450 - image_logo.width()) // 2
        painter.drawPixmap(image_logo_x, -70, image_logo.width(), image_logo.height(), image_logo)

        # --- Don't Wrist It Title---
        font_title = QFont()
        font_title.setPointSize(14)
        painter.setFont(font_title)
        painter.setPen(QColor("#303030"))
        painter.drawText(105, 38, 450, 270, Qt.AlignLeft, "DON'T WRIST IT")

        # Tagline
        font_title = QFont()
        font_title.setPointSize(9)
        painter.setFont(font_title)
        painter.setPen(QColor("#6A6969"))
        painter.drawText(105, 71, 450, 270, Qt.AlignLeft, "Prevent Carpal Tunnel Syndrome")

        # Text under the logo
        font_title2 = QFont()
        font_title2.setPointSize(13)
        painter.setFont(font_title2)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(self.width() - 450, 100, 450, 270, Qt.AlignCenter, "DON'T WRIST IT")

        # --- Worktime display section ---
        worktime_section = WorktimeSection(painter, self.width(), self.height())
        worktime_section.paint_worktime()

        # --- Breaktime display section ---
        breaktime_section = BreaktimeSection(painter, self.width(), self.height())
        breaktime_section.paint_breaktime()

        # --- Break interval display section ---
        breakint_section = BreakIntervalSection(painter, self.width(), self.height())
        breakint_section.paint_break_interval()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
