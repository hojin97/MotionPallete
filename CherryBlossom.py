import random, Paint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CherryBlossom(QLabel):
    img = None

    def __init__(self, parent):
        super().__init__(parent)

        # 모드 타입 정하기
        mode = Paint.MODE[self.parent().PA.Combo_effect1.currentIndex()]
        if mode == '벚꽃':
            type = random.randint(1, 8)
            c_size = random.randint(10, 15)

        elif mode == '눈':
            type = random.randint(1, 4)
            c_size = random.randint(30, 30)

        elif mode == '돈':
            type = random.randint(1, 25)
            c_size = random.randint(20, 30)

        elif mode == '물감':
            type = random.randint(1, 12)
            c_size = random.randint(100, 150)

        elif mode == '물방울':
            type = random.randint(1, 8)
            c_size = random.randint(5, 10)

        elif mode == '잎':
            type = random.randint(1, 13)
            c_size = random.randint(10, 25)

        elif mode == '하트':
            type = random.randint(1, 13)
            c_size = random.randint(10, 25)

        Cherry_pixmap = QPixmap(f'./이미지/{mode}/{str(type)}.png')
        Cherry_pixmap = Cherry_pixmap.scaled(c_size, c_size)


        px = random.randint(0, Paint.GV_size[0])
        py = random.randint(0, Paint.GV_size[1])
        self.img = QGraphicsPixmapItem(Cherry_pixmap)
        self.img.setPos(px, py)