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
        self.timeButton.clicked.connect(self.time_button_clicked)
        self.stepsButton.clicked.connect(self.steps_button_clicked)

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
            s = self.startInput.text().split()
            x1 = int(s[0])
            y1 = int(s[1])
        except:
            self.errorLabel.setText('Неверно введены координаты начала отрезка. \n'
                                    + 'Целочисленные X и Y должны разделяться одним пробелом')
            return

        try:
            s = self.endInput.text().split()
            x2 = int(s[0])
            y2 = int(s[1])
        except:
            self.errorLabel.setText('Неверно введены координаты конца отрезка. \n'
                                    + 'Целочисленные X и Y должны разделяться одним пробелом')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)
        
        draw_single_section(self.img, x1, y1, x2, y2, self.color, self.algChoice.currentText())
            
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
            length = float(self.lengthInput.text())
            if length < 1e-8:
                raise()
        except:
            self.errorLabel.setText('Неверно введена длина отрезков. \n'
                                    + 'Должно быть задано положительное действительное число')
            return

        try:
            angle = int(self.angleInput.text())
            if angle == 0:
                raise()
        except:
            self.errorLabel.setText('Неверно введен шаг изменения угла. \n'
                                    + 'Должно быть задано ненулевое целое число')
            return

        if scale != self.scale:
            self.scale = scale
            self.img = self.create_img(scale)
        
        draw_sections_series(self.img, self.img.width() / 2, self.img.height() / 2, 
                                length, angle * math.pi / 180, self.color, self.alg1Choice.currentText())
        if self.alg2Choice.currentText() != '-':
            draw_sections_series(self.img, self.img.width() / 2, self.img.height() / 2, 
                                length, angle * math.pi / 180, QColor(255, 255, 255), self.alg2Choice.currentText())
            
        self.redraw()
    

    def time_button_clicked(self):
        measure_time()
        

    def steps_button_clicked(self):
        try:
            l = int(self.lengthMInput.text())
            if l <= 0:
                raise()
        except:
            self.errorLabel.setText('Неверно введена длина отрезков. \n'
                                    + 'Должно быть задано положительное действительное число')

            return
        measure_steps(l)


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
