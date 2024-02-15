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
        
        self.colorButton.clicked.connect(self.ColorButtonClicked)
        self.fillButton.clicked.connect(self.FillButtonClicked)
        self.clearButton.clicked.connect(self.ClearButtonClicked)
        self.timeButton.clicked.connect(self.TimeButtonClicked)

        self.canvas.mousePressEvent = self.canvasClick

        self.color = QColor(0, 0, 0)
        self.SyncColorButton()
        self.img = self.CreateImage()
        self.Redraw()
        self.thread = None

        self.points = [[]]

    
    def canvasClick(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            if len(self.points[-1]) > 2:
                self.DrawLine(self.points[-1][-1][0], self.points[-1][-1][1], 
                                self.points[-1][0][0], self.points[-1][0][1])
                self.points.append([])
            return 

        x = event.x()
        y = event.y()
        
        if len(self.points[-1]) > 0:
            modifiers = QtWidgets.QApplication.keyboardModifiers()

            if modifiers == QtCore.Qt.ShiftModifier:
                dx = x - self.points[-1][-1][0]
                dy = y - self.points[-1][-1][1]

                if dx > dy:
                    if dx > -dy:
                        y = self.points[-1][-1][1]
                    else:
                        x = self.points[-1][-1][0]
                else:
                    if dx < -dy:
                        y = self.points[-1][-1][1]
                    else:
                        x = self.points[-1][-1][0]

            self.DrawLine(self.points[-1][-1][0], self.points[-1][-1][1], x, y)
        
        self.points[-1].append((x, y))

        
    def FillButtonClicked(self):
        if self.thread and self.thread.is_alive():
            return

        edges = self.PointsToEdges(self.points)
        if len(edges) < 3:
            return

        self.img = self.CreateImage()

        if self.delayButton.isChecked():
            self.thread = Thread(target = FillFigure, \
                args = (self.img, edges, self.color, QColor.fromRgb(255, 255, 255), \
                True, self.Redraw))
            self.thread.start()
        else:
            FillFigure(self.img, edges, self.color, QColor.fromRgb(255, 255, 255))
            self.Redraw()


    def PointsToEdges(self, points):
        edges = []
        for figure in points:
            if len(figure) > 2:
                for i in range(len(figure) - 1):
                    edges.append((figure[i], figure[i + 1]))
                edges.append((figure[-1], figure[0]))

        return edges


    def TimeButtonClicked(self):
        edges = self.PointsToEdges(self.points)

        n = 3
        t = 0
        for i in range(n):
            tm = time.time_ns()
            FillFigure(self.img, edges, self.color, QColor.fromRgb(255, 255, 255))
            tm = (time.time_ns() - tm) / 10 ** 6
            t += tm

        self.timeLabel.setText("{:.1f} мс (среднее из {:d})".format(t / n, n))
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
