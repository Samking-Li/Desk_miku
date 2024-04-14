from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class TablePet(QWidget):
    def __init__(self):
        super(TablePet, self).__init__()
        self.initUi()
        self.tray()
        self.is_follow_mouse = False
        self.mouse_drag_pos = self.pos()
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.timeout.connect(self.walk)
        self.timer.start(300)


    def randomAct(self):
        if self.key < 4:
            self.key += 1
        else:
            self.key = 1
        self.pic_url = 'source\miku_' + self.path + '\miku_' + str(self.key) + '.png'
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)
        if self.key ==4 and self.flag =='falling':
            self.path = 'walk'
            self.flag ='walking'


    #移动
    def walk(self):
        if not self.is_follow_mouse and self.flag =='walking':
            if self.w > 0:
                self.w -= 6
            else:
                self.w = 1800
            self.move(self.w, self.h)
        self.lbl.setPixmap(self.pm)

    #晃荡
    #def swing(self):
    #    self.pic_url = 'source\diana_swing\diana_' + str(self.key) + '.png'
    #    self.pm = QPixmap(self.pic_url)
    #    self.lbl.setPixmap(self.pm)

    # 摔倒
    #def fall(self):
    #    self.pic_url = 'source\diana_fall\diana_' + str(self.key) + '.png'
    #    self.pm = QPixmap(self.pic_url)
    #    self.lbl.setPixmap(self.pm)


    def initUi(self):
        screen = QDesktopWidget().screenGeometry()
        self.w = 1800
        self.h = 900
        self.path = 'walk'
        self.flag = 'walking'
        self.setGeometry(self.w, self.h, 300, 300)
        self.lbl = QLabel(self)
        self.key = 1
        self.pic_url = 'source\miku_' + self.path + '\miku_' + str(self.key) + '.png'
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

        # 背景透明等效果
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()

        # 系统托盘
    def tray(self):
        tp = QSystemTrayIcon(self)
        tp.setIcon(QIcon('source\miku_walk\miku_0.png'))
        ation_quit = QAction('QUIT', self, triggered=self.quit)
        tpMenu = QMenu(self)
        tpMenu.addAction(ation_quit)
        tp.setContextMenu(tpMenu)
        tp.show()


    # 鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.path = 'walk'
            event.accept()

        if event.button() == Qt.RightButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            #for self.key in (1, 5):
            #    self.timer.timeout.connect(self.swing)
            #    if self.key == 5:
            #        print('OK')
            self.path = 'swing'
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.RightButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.w, self.h = xy.x(), xy.y()
        event.accept()


    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        #for self.key in (1, 5):
        #    self.timer.timeout.connect(self.fall)
        self.path = 'fall'
        self.key = 1
        self.flag = 'falling'
        event.accept()




    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myPet = TablePet()
    sys.exit(app.exec_())
