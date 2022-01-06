import random
import Main, Paint, CherryBlossom, CustomStar, CustomStar2, CustomRect

from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CView(QGraphicsView):

    PA = None

    lineIndex = 0
    effectIndex = 0

    # 휘날리는 1
    Cherry_list = []

    # 휘날리는 2
    Fallin_list = []
    Dot_list = []

    # 휘날리는 3
    Spread_list = []
    Star_list = []

    # 휘날리는 4
    Sparkle1_list = []
    Sparkle2_list = []
    Star2_list = []

    # 모션
    M2_colorType = 0
    M3_colorType = 0
    M4_colorType = 0

    def __init__(self, parent):
        self.PA = parent
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 선택한 사진 불러오기
        pixmap = QPixmap(Main.DESIGN_LIST[self.parent().img_i])
        pixmap = pixmap.scaled(Paint.GV_size[0], Paint.GV_size[1])
        self.img = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.img)

        # 리스트
        self.items = []
        self.temp_items = []
        self.model = QStandardItemModel()

        self.start = QPointF()
        self.end = QPointF()

        # 애니메이션 그룹
        self.Fallin_Ani_Group = QParallelAnimationGroup(self)
        self.Spread_Ani_Group = QParallelAnimationGroup(self)
        self.Sparkle_Ani_Group = QParallelAnimationGroup(self)

        self.setRenderHint(QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)
        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        # Qt.LeftButton == 마우스 좌측 버튼.
        if e.button() == Qt.LeftButton:
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.end = e.pos()
            pen = QPen(self.PA.pencolor, self.PA.Line_tk.currentIndex())

            if self.PA.BRUSH:
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.temp_items.append(self.scene.addPath(path, pen))
                self.start = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.PA.BRUSH :
                self.model.appendRow(QStandardItem("line " + str(self.lineIndex)))
                self.PA.used_list.setModel(self.model)
                self.items.append(self.temp_items.copy())
                self.lineIndex += 1

        self.temp_items.clear()

    def BtnCherry(self):
        self.model.appendRow(QStandardItem("Effect " + str(self.effectIndex)))
        self.PA.used_list.setModel(self.model)
        self.effectIndex += 1

        num = 40
        if Paint.MODE[self.PA.Combo_effect1.currentIndex()] == "물감":
            num = 5

        for i in range(num):
            t_object = CherryBlossom.CherryBlossom(self)

            self.Cherry_list.append(t_object.img)
            self.temp_items.append(t_object.img)
            self.scene.addItem(t_object.img)

        self.items.append(self.temp_items.copy())
        self.temp_items.clear()

    def BtnFallin(self):
        for i in range(len(self.Fallin_list), len(self.Fallin_list)+Paint.EFFECT):
            self.Dot_list.append(CustomRect.CustomRect(self))
            self.Dot_list[i].setOpacity(random.random())
            self.scene.addItem(self.Dot_list[i])

        for i in range(len(self.Fallin_list), len(self.Fallin_list)+Paint.EFFECT):
            sx = random.randint(0, Paint.GV_size[0])
            sy = random.randint(-1000, 0)
            ey = random.randint(Paint.GV_size[1], Paint.GV_size[1]+100)

            rt = random.randint(6000, 12000)

            anim = QPropertyAnimation(self.Dot_list[i], b'pos')
            anim.setDuration(rt)
            anim.setStartValue(QPointF(sx, sy))
            anim.setEndValue(QPointF(sx, ey))
            anim.setLoopCount(-1)

            self.Fallin_list.append(anim)
            self.Fallin_Ani_Group.addAnimation(anim)

        self.Fallin_Ani_Group.start()

    def BtnSpread(self):
        for i in range(len(self.Spread_list), len(self.Spread_list)+Paint.EFFECT):
            self.Star_list.append(CustomStar.CustomStar(self))
            self.Star_list[i].setOpacity(random.random())
            self.scene.addItem(self.Star_list[i])

        for i in range(len(self.Spread_list), len(self.Spread_list) + Paint.EFFECT):
            sx = random.randint(0, Paint.GV_size[0])
            sy = random.randint(0, Paint.GV_size[1])
            ex = random.randint(0, Paint.GV_size[0])
            ey = random.randint(Paint.GV_size[1], Paint.GV_size[1] + 100)

            rt = random.randint(12000, 20000)

            anim = QPropertyAnimation(self.Star_list[i], b'pos')
            anim.setDuration(rt)
            anim.setStartValue(QPointF(sx, sy))

            if sx < Paint.GV_size[0] / 2 and sy < Paint.GV_size[1] / 2:
                anim.setEndValue(QPointF(sx - Paint.GV_size[0], sy - Paint.GV_size[1]))
            if sx < Paint.GV_size[0] / 2 and sy >= Paint.GV_size[1] / 2:
                anim.setEndValue(QPointF(sx - Paint.GV_size[0], sy + Paint.GV_size[1]))
            if sx >= Paint.GV_size[0] / 2 and sy < Paint.GV_size[1] / 2:
                anim.setEndValue(QPointF(sx + Paint.GV_size[0], sy - Paint.GV_size[1]))
            if sx >= Paint.GV_size[0] / 2 and sy >= Paint.GV_size[1] / 2:
                anim.setEndValue(QPointF(sx + Paint.GV_size[0], sy + Paint.GV_size[1]))

            anim.setEasingCurve(QEasingCurve.InCubic)
            anim.setLoopCount(-1)

            self.Spread_list.append(anim)
            self.Spread_Ani_Group.addAnimation(anim)
        self.Spread_Ani_Group.start()

    def BtnSparkle(self):
        for i in range(len(self.Sparkle1_list), len(self.Sparkle1_list) + Paint.EFFECT):
            self.Star2_list.append(CustomStar2.CustomStar2(self))
            self.Star2_list[i].setOpacity(random.random())
            self.scene.addItem(self.Star2_list[i])

        for i in range(len(self.Sparkle1_list), len(self.Sparkle1_list) + Paint.EFFECT):
            sx = random.randint(0, Paint.GV_size[0])
            sy = random.randint(0, Paint.GV_size[1])
            ex = random.randint(0, 60)
            ey = random.randint(Paint.GV_size[1], Paint.GV_size[1] + 100)
            plus_minus = random.choice([-1,1])

            rt = random.randint(6000, 12000)

            anim = QPropertyAnimation(self.Star2_list[i], b'pos')
            anim.setDuration(rt)
            anim.setStartValue(QPointF(sx, sy))
            anim.setEndValue(QPointF(sx-(ex*plus_minus), sy))
            anim.setEasingCurve(QEasingCurve.InQuad)

            anim2 = QPropertyAnimation(self.Star2_list[i], b'opacity')
            anim2.setDuration(rt)
            anim2.setStartValue(random.random())
            anim2.setEndValue(0)
            anim2.setEasingCurve(QEasingCurve.InOutQuad)

            anim.setLoopCount(-1)
            anim2.setLoopCount(-1)

            self.Sparkle1_list.append(anim)
            self.Sparkle2_list.append(anim2)
            self.Sparkle_Ani_Group.addAnimation(anim)
            self.Sparkle_Ani_Group.addAnimation(anim2)

        self.Sparkle_Ani_Group.start()
