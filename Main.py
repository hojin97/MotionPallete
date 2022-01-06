import sys, Paint
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

IMG_LIST = ['./이미지/명화/고흐_별이빛나는밤.jpg',
            './이미지/명화/고흐_생트마리해변의고깃배.jpg',
            './이미지/명화/뭉크_절규.jpg',
            './이미지/명화/밀레_만종.jpg',
            './이미지/명화/밀레_이삭줍는사람들.jpg',
            './이미지/명화/조르주피에르쇠라_그랑드자트섬의일요일오후.jpg',
            './이미지/명화/클로드모네_트루빌해안의판잣길.PNG',
            './이미지/명화/피터르브뤼헐_새덫이있는겨울풍경.PNG',
            './이미지/명화/구스타프클림트_키스.jpg',
            './이미지/명화/반고흐_아를의방.jpg',
            './이미지/명화/반고흐_해바라기2.jpg',
            './이미지/명화/흰배경.jpg',        
            './이미지/명화/검은배경.jpg'
            ]

DESIGN_LIST = [
            './이미지/도안/고흐_별이빛나는밤.jpg',
            './이미지/도안/고흐_생트마리해변의고깃배.jpg',
            './이미지/도안/뭉크_절규.jpg',
            './이미지/도안/밀레_만종.jpg',
            './이미지/도안/밀레_이삭줍는사람들.jpg',
            './이미지/도안/조르주피에르쇠라_그랑드자트섬의일요일오후.jpg',
            './이미지/도안/클로드모네_트루빌해안의판잣길.jpg',
            './이미지/도안/피터르브뤼헐_새덫이있는겨울풍경.jpg',
            './이미지/도안/구스타프클림트_키스.jpg',
            './이미지/도안/반고흐_아를의방.jpg',
            './이미지/도안/반고흐_해바라기2.jpg',
            './이미지/도안/흰배경.jpg',        
            './이미지/도안/검은배경.jpg'
            ]

# GV 사이즈
GV_main_size = [640, 340]
GV_sub_main_size = [140, 100]
GV_sub_etc_size = [100, 80]

# 0 => 메인,      1 => 서브 메인,         2 => 서브 기타
GV_size = [GV_main_size, GV_sub_main_size, GV_sub_etc_size]

class MainForm(QDialog):

    GV_list = ()
    img_i = 0

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.page_main = uic.loadUi('./Main.ui', self)       # UI Load

        # 버튼 이벤트 추가하기
        self.Btn_prev.clicked.connect(self.PrevClick)
        self.Btn_next.clicked.connect(self.NextClick)
        self.Btn_com.clicked.connect(self.GoPaint)

        self.GV_list = (self.GV_sub_1, self.GV_sub_2, self.GV_sub_main, self.GV_sub_3, self.GV_sub_4)

        # 이미지 초기화
        self.setMainImg(self.img_i)
        self.setSubImg()

        self.page_main.show()

    def GoPaint(self):
        print(self.img_i)
        Paint.PaintForm.img_i = self.img_i
        Paint.PaintForm()

    def PrevClick(self):
        self.img_i = (self.img_i - 1) % len(IMG_LIST)
        self.setMainImg(self.img_i)
        self.setSubImg()

    def NextClick(self):
        self.img_i = (self.img_i + 1) % len(IMG_LIST)
        self.setMainImg(self.img_i)
        self.setSubImg()


    def setMainImg(self, img_i):
        pixmap = QPixmap(IMG_LIST[img_i])
        pixmap = pixmap.scaled(GV_size[0][0], GV_size[0][1])
        self.GV_main.setPixmap(QPixmap(pixmap))

    def setSubImg(self):
        i = -2
        for GV in self.GV_list:
            pmap = QPixmap(IMG_LIST[(self.img_i + i) % len(IMG_LIST)])
            if i == 0:
                pmap = pmap.scaled(GV_size[1][0], GV_size[1][1])
            else:
                pmap = pmap.scaled(GV_size[2][0], GV_size[2][1])
            GV.setPixmap(QPixmap(pmap))
            i += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_dialog = MainForm()
    app.exec_()