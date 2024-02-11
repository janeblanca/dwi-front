from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont, QPixmap, QPen

class WristPositionSection:
    def __init__(self, painter, width, height):
        self.painter = painter
        self.width = width
        self.height = height

    def paint_wristposition(self, hands_detected=True, correct_position=True):
        pen = QPen(QColor("#FFFFFF"), 0)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor("#FFFFFF"))
        wristposition = QRect(105, 360, 200, 230)
        self.painter.drawRoundedRect(wristposition, 8, 8)

        # small square ICON (Blue Clock)
        self.painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(119, self.height - 347, 50, 50)
        self.painter.drawRoundedRect(square_blue_box, 8, 8)

        # small square
        self.painter.setBrush(QColor("#D0FBFF"))
        square_blue_box = QRect(183, 382, 105, 30)
        self.painter.drawRoundedRect(square_blue_box, 8, 8)

        # Image wrist
        image_wrist = QPixmap("./images/wrist.png")
        self.painter.drawPixmap(45, 340, 200, 115, image_wrist)

        # --- Texts ---
        font_title = QFont()
        font_title.setPointSize(9)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(193, 388, 450, 270, Qt.AlignLeft, "Wrist Position")

        # Description of wrist position
        font_title = QFont()
        font_title.setPointSize(8)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(122, 540, 450, 270, Qt.AlignLeft, "This section displays the")
        self.painter.drawText(122, 557, 450, 270, Qt.AlignLeft, "status of your wrist position")

        if not hands_detected:
            self.no_hands()
        else:
            if correct_position:
                self.paint_correct()
            else:
                self.paint_incorrect()

    def no_hands(self): 
        font_title = QFont()
        font_title.setPointSize(9)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#303030"))
        self.painter.drawText(150, 470, 450, 270, Qt.AlignLeft, "Align both hands")
        self.painter.drawText(155, 487, 450, 270, Qt.AlignLeft, "in the camera")

    def paint_correct(self):
        font_title = QFont()
        font_title.setPointSize(11)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#2093C3"))
        self.painter.drawText(175, 470, 450, 270, Qt.AlignLeft, "Correct")
    
    def paint_incorrect(self):
        font_title = QFont()
        font_title.setPointSize(11)
        self.painter.setFont(font_title)
        self.painter.setPen(QColor("#FF8A8A"))
        self.painter.drawText(178, 470, 450, 270, Qt.AlignLeft, "Incorrect")


    

