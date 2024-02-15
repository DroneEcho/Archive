import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import *
import design
from drawing import *
from functions import *


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.colorButton.clicked.connect(self.ColorButtonClicked)
        self.fillButton.clicked.connect(self.Draw)

        self.color = QColor(0, 0, 0)
        self.SyncColorButton()
        self.img = self.CreateImage()
        self.Redraw()

        
    def Draw(self):
        try:
            c = self.xInput.text().split('; ')
            xmin = float(c[0])
            xmax = float(c[1])
            xstep = float(c[2])
        except:
            self.errorLabel.setText('Неверно введены пределы x')
            return

        try:
            c = self.zInput.text().split('; ')
            zmin = float(c[0])
            zmax = float(c[1])
            zstep = float(c[2])
        except:
            self.errorLabel.setText('Неверно введены пределы z')
            return

        try:
            c = self.angleInput.text().split('; ')
            xangle = float(c[0]) * pi / 180
            yangle = float(c[1]) * pi / 180
            zangle = float(c[2]) * pi / 180
        except:
            self.errorLabel.setText('Неверно введены углы вращения')
            return

        if self.comboBox.currentIndex() == 0:
            func = f1
        elif self.comboBox.currentIndex() == 1:
            func = f2
        elif self.comboBox.currentIndex() == 2:
            func = f3
        elif self.comboBox.currentIndex() == 3:
            func = f4
        elif self.comboBox.currentIndex() == 4:
            func = f5


        self.img = self.CreateImage()
        painter = QPainter(self.img)
        painter.setPen(QPen(self.color))
        floating_horizon(painter, func, [xmin, xmax, xstep], 
                                        [zmin, zmax, zstep],
                                        [xangle, yangle, zangle],
                                        [self.canvas.width() / 2, self.canvas.height() / 2, 60])
        
        self.Redraw()
        


    def ClearButtonClicked(self):
        self.Clear()


    def ColorButtonClicked(self):
        self.color = QColorDialog.getColor()
        self.SyncColorButton()


    def SyncColorButton(self):
        self.colorButton.setStyleSheet("QWidget { background-color: %s}" % self.color.name())


    def Clear(self):
        self.timeLabel.setText("")
        self.points = [[]]
        if self.img:
            self.img.fill(QColor(255, 255, 255, 255).rgb())
            self.Redraw()


    def Redraw(self):
        pix = QPixmap.fromImage(self.img)
        pix = pix.scaled(self.canvas.width(), self.canvas.height())
        self.canvas.clear()
        self.canvas.setPixmap(pix)

    
    def DrawLine(self, x1, y1, x2, y2):
        painter = QPainter(self.img)
        painter.setPen(QPen(self.color, 1))
        painter.drawLine(x1, y1, x2, y2)
        self.Redraw()


    def CreateImage(self):
        img = QImage(self.canvas.width(),
                     self.canvas.height(),
                     QImage.Format_ARGB32)
        img.fill(QColor(255, 255, 255, 255).rgb())
        return img


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
