import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import *
import design
from algs import *


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.clearButton.clicked.connect(self.ClearButtonClicked)

        self.canvas.mousePressEvent = self.canvasClick

        self.polygon = []
        self.cropped = []
        self.cutter = []
        self.mode = 0

        self.polygonColor = QColor(0, 0, 0)
        self.cutterColor = QColor(70, 50, 200)
        self.croppedColor = QColor(250, 50, 70)

        self.img = self.CreateImage()
        self.Redraw()

    
    def canvasClick(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            if self.mode == 0:
                if len(self.polygon) > 2:
                    self.mode = 1

                    self.polygon.append(self.polygon[0])
                    self.Redraw()

            elif self.mode == 1:
                if len(self.cutter) > 2:
                    self.cutter.append(self.cutter[0])
                    self.Redraw()

                    self.errorLabel.setText('')
                    try:
                        self.cropped = Crop(self.polygon, self.cutter)
                    except:
                        self.errorLabel.setText('Отсекатель не является выпуклым многоугольником')

                    self.Redraw()
                    self.cutter = [] 
                    self.cropped = []
        
        else:
            x = event.x()
            y = event.y()

            if self.mode == 0:
                self.cutter = []
                self.cropped = []
                self.Redraw()

                arr = self.polygon
            else:
                arr = self.cutter

            if len(arr) > 0:
                modifiers = QtWidgets.QApplication.keyboardModifiers()

                if modifiers == QtCore.Qt.ShiftModifier:
                    dx = x - arr[-1][0]
                    dy = y - arr[-1][1]

                    if dx > dy:
                        if dx > -dy:
                            y = arr[-1][1]
                        else:
                            x = arr[-1][0]
                    else:
                        if dx < -dy:
                            y = arr[-1][1]
                        else:
                            x = arr[-1][0]

            arr.append( [x, self.canvas.height() - y] )
            self.Redraw()


    def ClearButtonClicked(self):
        self.Clear()


    def Clear(self):
        self.cutter = []
        self.polygon = []
        self.cropped = []
        self.mode = 0
        self.img.fill(QColor(255, 255, 255, 255).rgb())
        
        self.Update()


    def Redraw(self):
        self.img.fill(QColor(255, 255, 255, 255).rgb())

        
        for i in range(len(self.polygon) - 1):
            self.DrawLine(self.polygon[i][0], self.canvas.height() - self.polygon[i][1], 
                            self.polygon[i + 1][0], self.canvas.height() - self.polygon[i + 1][1], self.polygonColor, 2)

        for i in range(len(self.cropped) - 1):
            self.DrawLine(self.cropped[i][0], self.canvas.height() - self.cropped[i][1], 
                            self.cropped[i + 1][0], self.canvas.height() - self.cropped[i + 1][1], self.croppedColor, 4)
        
        for i in range(len(self.cutter) - 1):
            self.DrawLine(self.cutter[i][0], self.canvas.height() - self.cutter[i][1], 
                            self.cutter[i + 1][0], self.canvas.height() - self.cutter[i + 1][1], self.cutterColor, 2)

        self.Update()


    def Update(self):
        pix = QPixmap.fromImage(self.img)
        pix = pix.scaled(self.canvas.width(), self.canvas.height())
        self.canvas.clear()
        self.canvas.setPixmap(pix)

    
    def DrawLine(self, x1, y1, x2, y2, color, width):
        painter = QPainter(self.img)
        painter.setPen(QPen(color, width))
        painter.drawLine(x1, y1, x2, y2)

    
    def DrawRect(self, x1, y1, x2, y2, color):
        painter = QPainter(self.img)
        painter.setPen(QPen(color, 2))
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)

    
    def DrawPoint(self, x, y, color):
        painter = QPainter(self.img)
        painter.setPen(QPen(color, 2))
        painter.drawPoint(x, y)


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
