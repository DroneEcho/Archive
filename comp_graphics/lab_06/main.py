import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QColorDialog, QApplication
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
        self.mode = 0
        self.points = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.Redraw) 

    
    def canvasClick(self, event):
        if self.mode == 1:
            self.mode = 0
            QApplication.restoreOverrideCursor()
            self.Fill(event.x(), event.y())
            return
        if self.mode == 2:
            self.mode = 0
            QApplication.restoreOverrideCursor()
            self.MeasureTime(event.x(), event.y())
            return
        
        if event.buttons() == QtCore.Qt.RightButton:
            if len(self.points) > 2:
                self.DrawLine(self.points[-1][0], self.points[-1][1], 
                                self.points[0][0], self.points[0][1])
                self.points = []
            return 

        x = event.x()
        y = event.y()
        
        if len(self.points) > 0:
            modifiers = QtWidgets.QApplication.keyboardModifiers()

            if modifiers == QtCore.Qt.ShiftModifier:
                dx = x - self.points[-1][0]
                dy = y - self.points[-1][1]

                if dx > dy:
                    if dx > -dy:
                        y = self.points[-1][1]
                    else:
                        x = self.points[-1][0]
                else:
                    if dx < -dy:
                        y = self.points[-1][1]
                    else:
                        x = self.points[-1][0]

            self.DrawLine(self.points[-1][0], self.points[-1][1], x, y)
        
        self.points.append((x, y))

        
    def FillButtonClicked(self):
        self.mode = 1
        QApplication.setOverrideCursor(Qt.PointingHandCursor)


    def TimeButtonClicked(self):
        self.mode = 2
        QApplication.setOverrideCursor(Qt.PointingHandCursor)


    def Fill(self, x, y):
        if self.thread and self.thread.is_alive():
            return

        if self.delayButton.isChecked():
            self.thread = Thread(target = FillFigure, \
                args = (self.img, x, y, self.color.rgb(), True, self.timer.stop))
            self.timer.start(1)
            self.thread.start()
        else:
            FillFigure(self.img, x, y, self.color.rgb())
            self.Redraw()


    def MeasureTime(self, x, y):
        n = 3
        t = 0
        for i in range(n):
            img = QImage(self.img)
            tm = time.time_ns()
            FillFigure(img, x, y, self.color.rgb())
            tm = (time.time_ns() - tm) / 10 ** 6
            t += tm

        self.timeLabel.setText("{:.1f} мс (среднее из {:d})".format(t / n, n))
        self.img = img
        self.Redraw()


    def ClearButtonClicked(self):
        if not (self.thread and self.thread.is_alive()):
            self.Clear()


    def ColorButtonClicked(self):
        self.color = QColorDialog.getColor()
        self.SyncColorButton()


    def SyncColorButton(self):
        self.colorButton.setStyleSheet("QWidget { background-color: %s}" % self.color.name())


    def Clear(self):
        self.timeLabel.setText("")
        self.points = []
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
