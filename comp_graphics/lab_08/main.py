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
        
        self.fillButton.clicked.connect(self.FillButtonClicked)
        self.clearButton.clicked.connect(self.ClearButtonClicked)

        self.canvas.mousePressEvent = self.canvasClick

        self.segments = []
        self.cropped = []
        self.cutter = []
        self.prev = None
        self.mode = 0

        self.segmentsColor = QColor(0, 0, 0)
        self.cutterColor = QColor(70, 50, 200)
        self.croppedColor = QColor(250, 50, 70)

        self.img = self.CreateImage()
        self.Redraw()

    
    def canvasClick(self, event):
        if event.buttons() == QtCore.Qt.RightButton and self.mode == 1:
            if len(self.cutter) > 2:
                self.cutter.append(self.cutter[0])
                self.Redraw()

                self.mode = 0
                cutter = self.PointsToEdges(self.cutter)

                try:
                    self.cropped = Crop(self.segments, cutter)
                except:
                    self.errorLabel.setText('Отсекатель не является выпуклым многоугольником')

                self.Redraw()
            return

        x = event.x()
        y = event.y()

        if self.mode == 0:
            self.cutter = []
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
            if len(self.cutter) > 0:
                modifiers = QtWidgets.QApplication.keyboardModifiers()

                if modifiers == QtCore.Qt.ShiftModifier:
                    dx = x - self.cutter[-1][0]
                    dy = y - self.cutter[-1][1]

                    if dx > dy:
                        if dx > -dy:
                            y = self.cutter[-1][1]
                        else:
                            x = self.cutter[-1][0]
                    else:
                        if dx < -dy:
                            y = self.cutter[-1][1]
                        else:
                            x = self.cutter[-1][0]

            self.cutter.append([x, y])
            self.Redraw()


    def PointsToEdges(self, points):
        edges = []
        
        if len(points) > 2:
            for i in range(len(points) - 1):
                edges.append([points[i], points[i + 1]])

        return edges

        
    def FillButtonClicked(self):
        self.errorLabel.setText('')
        self.cutter = []
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
        for i in range(len(self.cutter) - 1):
            self.DrawLine(self.cutter[i][0], self.cutter[i][1], 
                            self.cutter[i + 1][0], self.cutter[i + 1][1], self.cutterColor, 2)
        
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
