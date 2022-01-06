import sys, os, random
import Main, CView

from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PIL import Image
from glob import glob

MODE = ['눈', '돈', '물감', '물방울', '벚꽃', '잎', '하트']

GV_size = [768, 500]
EFFECT = 50

class PaintForm(QWidget):

    img_i = -1
    selItem = -1
    BRUSH = True

    def __init__(self):
        super().__init__()

        self.selItem = "-1"

        # 테스트
        print(f"Image : {self.img_i}")

        # UI 로드
        self.page_paint = uic.loadUi('./Paint.ui', self)
        self.page_paint.show()

        # 시작 색 설정
        self.pencolor = QColor(0, 0, 0)
        self.effectColor2 = QColor(0, 0, 0)
        self.effectColor3 = QColor(0, 0, 0)
        self.effectColor4 = QColor(0, 0, 0)

        # 콤보 박스 초기화
        self.Line_tk.setCurrentIndex(3)

        # 버튼 구현
        self.Brush_On.clicked.connect(self.radioClicked)
        self.Brush_On.setChecked(True)
        self.Btn_color.clicked.connect(self.ColorBtn)
        self.Btn_color.setStyleSheet('background-color: rgb(0,0,0)')

        self.Btn_del_1.clicked.connect(self.DelBtn)
        self.Btn_del_2.clicked.connect(self.DelBtn)
        self.used_list.clicked[QModelIndex].connect(self.list_clicked)

        self.Btn_effect1.clicked.connect(self.CherryBlossom)

        # 휘날리는 2
        self.Btn_effect2_color.clicked.connect(self.ColorBtn)
        self.Btn_effect2_color.setStyleSheet('background-color: rgb(0,0,0)')
        self.Btn_effect2_1.clicked.connect(self.Fallin)
        self.Btn_effect2_2.clicked.connect(self.Fallin)
        self.Btn_effect2_motion_1.clicked.connect(self.Effect_motion2)
        self.Btn_effect2_motion_2.clicked.connect(self.Effect_motion2)

        # 휘날리는 3
        self.Btn_effect3_color.clicked.connect(self.ColorBtn)
        self.Btn_effect3_color.setStyleSheet('background-color: rgb(0,0,0)')
        self.Btn_effect3_1.clicked.connect(self.Spread)
        self.Btn_effect3_2.clicked.connect(self.Spread)
        self.Btn_effect3_motion_1.clicked.connect(self.Effect_motion3)
        self.Btn_effect3_motion_2.clicked.connect(self.Effect_motion3)

        # 휘날리는 4
        self.Btn_effect4_color.clicked.connect(self.ColorBtn)
        self.Btn_effect4_color.setStyleSheet('background-color: rgb(0,0,0)')
        self.Btn_effect4_1.clicked.connect(self.Sparkle)
        self.Btn_effect4_2.clicked.connect(self.Sparkle)
        self.Btn_effect4_motion_1.clicked.connect(self.Effect_motion4)
        self.Btn_effect4_motion_2.clicked.connect(self.Effect_motion4)

        self.Btn_paint_type1.clicked.connect(self.ChangePaint)
        self.Btn_paint_type2.clicked.connect(self.ChangePaint)

        self.Btn_com_1.clicked.connect(self.Commit)
        self.Btn_com_2.clicked.connect(self.makeGIF)

        #그림 불러오기기
        self.view = CView.CView(self)
        self.L_layout.addWidget(self.view)

        rn = random.randint(0,10000)
        self.fileName.setText("명작"+str(rn))

        self.uLabel = QTimer(self)
        self.uLabel.timeout.connect(self.UpdateLabel)
        self.uLabel.start(100)

    def Commit(self):
        self.timer = QTimer(self)
        self.plot_times = 0
        self.timer.timeout.connect(self.time_Event)
        self.timer.start(100)

    def time_Event(self):
        self.plot_times += 1

        if self.plot_times >= 10000:
            plot_times_str = str(self.plot_times)
        elif self.plot_times >= 1000:
            plot_times_str = "0" + str(self.plot_times)
        elif self.plot_times >= 100:
            plot_times_str = "00" + str(self.plot_times)
        elif self.plot_times >= 10:
            plot_times_str = "000" + str(self.plot_times)
        else:
            plot_times_str = "0000" + str(self.plot_times)

        self.view.grab().save("./temp/temp" + plot_times_str + ".png")

    def makeGIF(self):
        try:
            self.timer.stop()
            images = []
            file_num = glob("./temp/**.png")

            file_num.sort()

            for i in range(0, len(file_num), 1):
                im = Image.open(file_num[i], 'r')
                fp = im.copy()
                im.close()
                images.append(fp)

            # duraton uints is micro seconds
            images[0].save(f"./GIF/{self.fileName.text()}.gif",
                           save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

            for i in range(0, len(file_num), 1):
                os.remove(file_num[i])
            self.plot_times = 0
        except Exception :
            print("저장 안됌.")
            pass

    def ChangePaint(self):
        sender = self.sender()
        self.view.scene.removeItem(self.view.img)

        # Clear
        self.view.scene.clear()
        self.view.Cherry_list.clear()
        self.view.model.clear()
        self.used_list.setModel(self.view.model)
        self.view.items.clear()

        self.view.Dot_list.clear()
        self.view.Fallin_list.clear()
        self.view.Fallin_Ani_Group.clear()

        self.view.Star_list.clear()
        self.view.Spread_list.clear()
        self.view.Spread_Ani_Group.clear()

        self.view.Star2_list.clear()
        self.view.Sparkle1_list.clear()
        self.view.Sparkle2_list.clear()
        self.view.Sparkle_Ani_Group.clear()

        self.selItem = "-1"

        # 버튼 보고 그림 선택
        if sender == self.Btn_paint_type1:
            pixmap = QPixmap(Main.IMG_LIST[self.img_i])
            print("명화위에그리기")
        else:
            pixmap = QPixmap(Main.DESIGN_LIST[self.img_i])
            print("도안위에그리기")
        pixmap = pixmap.scaled(GV_size[0], GV_size[1])

        self.view.img = QGraphicsPixmapItem(pixmap)
        self.view.scene.addItem(self.view.img)

    def DelBtn(self):
        sender = self.sender()
        if sender == self.Btn_del_1:
            if self.selItem == "-1":
                print("선택 안됌.")
                pass
            else:
                for i in self.view.items[self.selItem.index().row()]:
                    self.view.scene.removeItem(i)
                self.view.items.pop(self.selItem.index().row())
                self.view.model.removeRow(self.selItem.index().row())

        elif sender == self.Btn_del_2:
            for i in self.view.items:
                for j in i:
                    self.view.scene.removeItem(j)
            self.view.items.clear()
            self.view.model.clear()

        self.selItem = "-1"

    def list_clicked(self, index):
        self.selItem = self.view.model.itemFromIndex(index)
        print(f"Selected Index : {self.selItem.index().row()}")

    def radioClicked(self):
        if self.Brush_On.isChecked():
            self.BRUSH = True
        else:
            self.BRUSH = False
        print(self.BRUSH)

    def ColorBtn(self):
        color = QColorDialog.getColor()
        sender = self.sender()

        if sender == self.Btn_color and color.isValid():
            self.pencolor = color
            self.Btn_color.setStyleSheet('background-color: {}'.format(color.name()))

        elif sender == self.Btn_effect2_color and color.isValid():
            self.effectColor2 = color
            self.Btn_effect2_color.setStyleSheet('background-color: {}'.format(color.name()))
            self.view.M2_colorType = 0
            print(self.effectColor2.name())

        elif sender == self.Btn_effect3_color and color.isValid():
            self.effectColor3 = color
            self.Btn_effect3_color.setStyleSheet('background-color: {}'.format(color.name()))
            self.view.M3_colorType = 0
            print(self.effectColor3.name())

        elif sender == self.Btn_effect4_color and color.isValid():
            self.effectColor4 = color
            self.Btn_effect4_color.setStyleSheet('background-color: {}'.format(color.name()))
            self.view.M4_colorType = 0
            print(self.effectColor4.name())

    def CherryBlossom(self):
        print("효과 1 : 체리블라썸")
        self.view.BtnCherry()

    def Fallin(self):
        sender = self.sender()
        if sender == self.Btn_effect2_1:
            print("효과 2 : 떨어지는 효과")
            self.view.BtnFallin()
        elif sender == self.Btn_effect2_2:
            if len(self.view.Fallin_list) == 0:
                print("휘날리는 2 : 비어있습니다.")
                pass
            else:
                for i in range(EFFECT - 1, -1, -1):
                    self.view.Fallin_Ani_Group.removeAnimation(self.view.Fallin_list[i])
                    self.view.scene.removeItem(self.view.Dot_list[i])
                    self.view.Fallin_list.pop(i)
                    self.view.Dot_list.pop(i)
                print(f"휘날리는 2 : {len(self.view.Fallin_list)}개 남았습니다.")

    def Effect_motion2(self):
        sender = self.sender()
        if sender == self.Btn_effect2_motion_1:
            print("휘날리는2 모션 1")
            self.view.M2_colorType = 1
        elif sender == self.Btn_effect2_motion_2:
            print("휘날리는2 모션 2")
            self.view.M2_colorType = 2

    def Effect_motion3(self):
        sender = self.sender()
        if sender == self.Btn_effect3_motion_1:
            print("휘날리는3 모션 1")
            self.view.M3_colorType = 1
        elif sender == self.Btn_effect3_motion_2:
            print("휘날리는3 모션 2")
            self.view.M3_colorType = 2

    def Effect_motion4(self):
        sender = self.sender()
        if sender == self.Btn_effect4_motion_1:
            print("휘날리는4 모션 1")
            self.view.M4_colorType = 1
        elif sender == self.Btn_effect4_motion_2:
            print("휘날리는4 모션 2")
            self.view.M4_colorType = 2

    def Spread(self):
        sender = self.sender()
        if sender == self.Btn_effect3_1:
            print("효과 3: 퍼지는 모션 추가")
            self.view.BtnSpread()

        elif sender == self.Btn_effect3_2:
            print("효과 3: 퍼지는 모션 삭제")
            if len(self.view.Star_list) == 0:
                print("휘날리는 3 : 비어있습니다.")
                pass
            else:
                for i in range(EFFECT - 1, -1, -1):
                    self.view.Spread_Ani_Group.removeAnimation(self.view.Spread_list[i])
                    self.view.scene.removeItem(self.view.Star_list[i])
                    self.view.Spread_list.pop(i)
                    self.view.Star_list.pop(i)
                print(f"휘날리는 3 : {len(self.view.Star_list)}개 남았습니다.")

    def Sparkle(self):
        sender = self.sender()
        if sender == self.Btn_effect4_1:
            print("효과 4: 흩어지기 모션 추가")
            self.view.BtnSparkle()

        elif sender == self.Btn_effect4_2:
            print("효과 4: 흩어지기 모션 삭제")
            if len(self.view.Sparkle1_list) == 0:
                print("휘날리는 4 : 비어있습니다.")
                pass
            else:
                for i in range(EFFECT - 1, -1, -1):
                    self.view.Sparkle_Ani_Group.removeAnimation(self.view.Sparkle1_list[i])
                    self.view.Sparkle_Ani_Group.removeAnimation(self.view.Sparkle2_list[i])
                    self.view.scene.removeItem(self.view.Star2_list[i])
                    self.view.Sparkle1_list.pop(i)
                    self.view.Sparkle2_list.pop(i)
                    self.view.Star2_list.pop(i)

                print(f"휘날리는 4 : {len(self.view.Star_list)}개 남았습니다.")

    def UpdateLabel(self):
        self.Effect2_label.setText(f"[ 내리는 ] :  {len(self.view.Dot_list)}")
        self.Effect3_label.setText(f"[ 퍼져가는 ] :  {len(self.view.Star_list)}")
        self.Effect4_label.setText(f"[ 떠다니는 ] :  {len(self.view.Star2_list)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PaintForm()
    w.show()
    sys.exit(app.exec_())
