import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import *
import design
from drawing import *
from measurements import *


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        algs = [i.title for i in AlgName]

        self.algChoice.addItems(algs)
        self.alg1Choice.addItems(algs)
        self.alg2Choice.addItems(['-'] + algs)
        
        self.colorButton.clicked.connect(self.color_button_clicked)
        self.clearButton.clicked.connect(self.clear_button_clicked)
        self.singleDrawButton.clicked.connect(self.single_button_clicked)
        self.seriesDrawButton.clicked.connect(self.series_button_clicked)
        self.timeButton_2.clicked.connect(self.time_button_clicked)

        self.algChoice_1.addItems(algs)
        self.alg1Choice_1.addItems(algs)
        self.alg2Choice_1.addItems(['-'] + algs)
        
        self.singleDrawButton_1.clicked.connect(self.single_button_clicked_1)
        self.seriesDrawButton_1.clicked.connect(self.series_button_clicked_1)
        self.timeButton_1.clicked.connect(self.time_button_clicked_1)

        self.color = QColor(0, 0, 0)
        self.sync_color_button()
        self.img = None
        self.scale = 0


    def single_button_clicked(self):
        self.errorLabel.setText('')

        try:
            scale = float(self.scaleInput.text())
            if scale < 1e-8:
                raise()
        except:
            self.errorLabel.setText('Неверно введен масштаб. \n'
                                    + 'Должно быть задано положительное действительное число')
            return
        
        try:
            s = self.centerInput.text().split()
            xc = int(s[0])
            yc = int(s[1])
        except:
            self.errorLabel.setText('Неверно введены координаты центра. \n'
                                    + 'Целочисленные X и Y должны разделяться одним пробелом')
            return

        try:
            s = self.radiusInput.text()
            r = int(s)
        except:
            self.errorLabel.setText('Неверно введен радиус. \n'
                                    + 'Должно быть задано натуральное число')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)
        
        draw_single_circle(self.img, xc, yc, r, self.color, self.algChoice.currentText())
            
        self.redraw()


    def single_button_clicked_1(self):
        self.errorLabel.setText('')

        try:
            scale = float(self.scaleInput.text())
            if scale < 1e-8:
                raise()
        except:
            self.errorLabel.setText('Неверно введен масштаб. \n'
                                    + 'Должно быть задано положительное действительное число')
            return
        
        try:
            s = self.centerInput_1.text().split()
            xc = int(s[0])
            yc = int(s[1])
        except:
            self.errorLabel.setText('Неверно введены координаты центра. \n'
                                    + 'Целочисленные X и Y должны разделяться одним пробелом')
            return

        try:
            s = self.radiusInput_1.text().split()
            a = int(s[0])
            b = int(s[1])
        except:
            self.errorLabel.setText('Неверно введены полуоси. \n'
                                    + 'Должны быть заданы два натуральных числа')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)
        
        draw_single_ellipse(self.img, xc, yc, a, b, self.color, self.algChoice_1.currentText())
            
        self.redraw()


    def series_button_clicked(self):
        self.errorLabel.setText('')

        try:
            scale = float(self.scaleInput.text())
            if scale < 1e-8:
                raise()
        except:
            self.errorLabel.setText('Неверно введен масштаб. \n'
                                    + 'Должно быть задано положительное действительное число')
            return
        
        try:
            r1 = int(self.startInput.text())
            if r1 < 1:
                raise()
        except:
            self.errorLabel.setText('Неверно введен начальный радиус. \n'
                                    + 'Должно быть задано натуральное число')
            return

        try:
            r2 = int(self.endInput.text())
            if r2 < 1:
                raise()
        except:
            self.errorLabel.setText('Неверно введен конечный радиус. \n'
                                    + 'Должно быть задано натуральное число')
            return

        try:
            step = int(self.stepInput.text())
            if step < 1:
                raise()
        except:
            self.errorLabel.setText('Неверно введен шаг изменения радиуса. \n'
                                    + 'Должно быть задано натуральное число')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)
        
        draw_spector(self.img, self.img.width() // 2, self.img.height() // 2, 
            r1, r2, step, self.color, self.alg1Choice.currentText())

        if self.alg2Choice.currentText() != '-':
            draw_spector(self.img, self.img.width() // 2, self.img.height() // 2, 
                r1, r2, step, QColor(255, 255, 255), self.alg2Choice.currentText())
            
        self.redraw()


    def series_button_clicked_1(self):
        self.errorLabel.setText('')

        try:
            scale = float(self.scaleInput.text())
            if scale < 1e-8:
                raise()
        except:
            self.errorLabel.setText('Неверно введен масштаб. \n'
                                    + 'Должно быть задано положительное действительное число')
            return
        
        try:
            s = self.startInput_1.text().split()
            a1, b1 = int(s[0]), int(s[1])
            if a1 < 1 or b1 < 1:
                raise()
        except:
            self.errorLabel.setText('Неверно введены начальные полуоси. \n'
                                    + 'Должны быть заданы два натуральных числа')
            return

        try:
            s = self.endInput_1.text().split()
            a2, b2 = int(s[0]), int(s[1])
            if a2 < 1 or b2 < 1:
                raise()
        except:
            self.errorLabel.setText('Неверно введены конечные полуоси. \n'
                                    + 'Должны быть заданы два натуральных числа')
            return

        try:
            qty = int(self.qtyInput.text())
            if qty < 2:
                raise()
        except:
            self.errorLabel.setText('Неверно введено количество эллипсов. \n'
                                    + 'Должно быть задано натуральное число > 1')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)

        draw_spector_ellipse(self.img, self.img.width() // 2, self.img.height() // 2,
            a1, b1, a2, b2, qty, self.color, self.alg1Choice_1.currentText())

        if self.alg2Choice_1.currentText() != '-':
            draw_spector_ellipse(self.img, self.img.width() // 2, self.img.height() // 2,
                a1, b1, a2, b2, qty, QColor(255, 255, 255), self.alg2Choice_1.currentText())
            
        self.redraw()
    

    def time_button_clicked(self):
        measure_time()


    def time_button_clicked_1(self):
        measure_time_ellipse()


    def clear_button_clicked(self):
        self.clear()


    def color_button_clicked(self):
        self.color = QColorDialog.getColor()
        self.sync_color_button()


    def sync_color_button(self):
        self.colorButton.setStyleSheet("QWidget { background-color: %s}" % self.color.name())


    def clear(self):
        if self.img:
            self.img.fill(QColor(255, 255, 255, 255).rgb())
            self.redraw()


    def redraw(self):
        pix = QPixmap.fromImage(self.img)
        pix = pix.scaled(self.canvas.width(), self.canvas.height())
        self.canvas.clear()
        self.canvas.setPixmap(pix)


    def create_img(self, scale):
        img = QImage(round(self.canvas.width() / scale),
                     round(self.canvas.height() / scale),
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
