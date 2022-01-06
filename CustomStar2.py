import random

from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CustomStar2(QGraphicsObject):
    PA = None

    # RGB, ALPHA
    rr = 0
    rg = 0
    rb = 0
    ra = 0

    # Type2 flags
    T2_1 = True
    T2_2 = False
    T2_3 = False
    T2_4 = False
    T2_5 = False
    T2_6 = False

    def __init__(self, parent):
        self.PA = parent
        super().__init__()

    def boundingRect(self):
        return QRectF(0, 0, 4, 4)  # <---

    def paint(self,painter,style,widget=None):
        # 빠른 색 변환
        if self.PA.M4_colorType == 1:
            self.rr = random.randint(0, 255)
            self.rg = random.randint(0, 255)
            self.rb = random.randint(0, 255)
            col = QColor(self.rr, self.rg, self.rb)

        # 천천히 색 변환
        elif self.PA.M4_colorType == 2:
            if self.T2_1:
                self.rr = 255
                self.rg = 0
                self.rb += 5
                if self.rb > 255:
                    self.rb = 255
                    self.T2_1 = False
                    self.T2_2 = True

            if self.T2_2:
                self.rr += -5
                self.rg = 0
                self.rb = 255
                if self.rr < 0:
                    self.rr = 0
                    self.T2_2 = False
                    self.T2_3 = True

            if self.T2_3:
                self.rr = 0
                self.rg += 5
                self.rb = 255
                if self.rg > 255:
                    self.rg = 255
                    self.T2_3 = False
                    self.T2_4 = True

            if self.T2_4:
                self.rr = 0
                self.rg = 255
                self.rb += -5
                if self.rb < 0:
                    self.rb = 0
                    self.T2_4 = False
                    self.T2_5 = True

            if self.T2_5:
                self.rr += 5
                self.rg = 255
                self.rb = 0
                if self.rr > 255:
                    self.rr = 255
                    self.T2_5 = False
                    self.T2_6 = True

            if self.T2_6:
                self.rr = 255
                self.rg += -5
                self.rb = 0
                if self.rg < 0:
                    self.rg = 0
                    self.T2_6 = False
                    self.T2_1 = True

            self.ra = 255
            # print(self.rr, self.rg, self.rb)
            col = QColor(self.rr, self.rg, self.rb, alpha=self.ra)

        else:
            col = self.PA.PA.effectColor4

        painter.setBrush(QBrush(col, style=Qt.SolidPattern))
        painter.setPen(QPen(col, 3))
        painter.drawEllipse(self.boundingRect())
