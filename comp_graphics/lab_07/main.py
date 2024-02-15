import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import *
import design
from drawing import *
from threading import Thread
import time


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.fillButton.clicked.connect(self.FillButtonClicked)
        self.clearButton.clicked.connect(self.ClearButtonClicked)

        self.canvas.mousePressEvent = self.canvasClick

        self.segments = []
        self.cropped = []
        self.rect = [None, None]
        self.prev = None
        self.mode = 0

        self.segmentsColor = QColor(0, 0, 0)
        self.rectColor = QColor(70, 50, 200)
        self.croppedColor = QColor(200, 50, 70)

        self.img = self.CreateImage()
        self.Redraw()

    
    def canvasClick(self, event):
        x = event.x()
        y = event.y()

        if self.mode == 0:
            self.rect = [None, None]
            self.cropped = []
            self.Redraw()
            
            if self.prev:
                modifiers = QtWidgets.QApplication.keyboardModifiers()

                if modifiers == QtCore.Qt.ShiftModifier:
                    dx = x - self.prev[0]
                    dy = y - self.prev[1]

                    if dx > dy:
                        if dx > -dy:
                            y = self.prev[1]
                        else:
                            x = self.prev[0]
                    else:
                        if dx < -dy:
                            y = self.prev[1]
                        else:
                            x = self.prev[0]

                self.segments.append( [self.prev, [x, y]] )
                self.prev = None
                self.Redraw()
                
            else:
                self.prev = [x, y]
                self.DrawPoint(x, y, self.segmentsColor)
                self.Update()
                
        elif self.mode == 1:
            self.DrawPoint(x, y, self.rectColor)
            self.Update()
            
            if self.rect[0]:
                self.rect[1] = (x, y)
                self.mode = 0

                self.cropped = Crop(self.segments, self.rect)
                self.Redraw()
                    
            else:
                self.rect[0] = (x, y)

        
    def FillButtonClicked(self):
        self.rect = [None, None]
        self.cropped = []
        self.Redraw()
        self.mode = 1


    def ClearButtonClicked(self):
        self.Clear()


    def Clear(self):
        self.segments = []
        self.cropped = []
        self.rect = [None, None]
        self.prev = None
        self.img.fill(QColor(255, 255, 255, 255).rgb())
        
        self.Update()


    def Redraw(self):
        self.img.fill(QColor(255, 255, 255, 255).rgb())

        for s in self.segments:
            self.DrawLine(s[0][0], s[0][1], s[1][0], s[1][1], self.segmentsColor, 2)
        for s in self.cropped:
            self.DrawLine(s[0][0], s[0][1], s[1][0], s[1][1], self.croppedColor, 3)
        if self.rect[1]:
            self.DrawRect(self.rect[0][0], self.rect[0][1], self.rect[1][0], self.rect[1][1], self.rectColor)
        
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
