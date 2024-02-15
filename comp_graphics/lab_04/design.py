# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(900, 150, 441, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.Circle = QtWidgets.QWidget()
        self.Circle.setObjectName("Circle")
        self.singleBox = QtWidgets.QGroupBox(self.Circle)
        self.singleBox.setGeometry(QtCore.QRect(10, 10, 411, 161))
        self.singleBox.setObjectName("singleBox")
        self.algLabel = QtWidgets.QLabel(self.singleBox)
        self.algLabel.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.algLabel.setObjectName("algLabel")
        self.algChoice = QtWidgets.QComboBox(self.singleBox)
        self.algChoice.setGeometry(QtCore.QRect(190, 30, 201, 22))
        self.algChoice.setObjectName("algChoice")
        self.centerLabel = QtWidgets.QLabel(self.singleBox)
        self.centerLabel.setGeometry(QtCore.QRect(20, 60, 121, 16))
        self.centerLabel.setObjectName("centerLabel")
        self.centerInput = QtWidgets.QLineEdit(self.singleBox)
        self.centerInput.setGeometry(QtCore.QRect(190, 60, 61, 22))
        self.centerInput.setObjectName("centerInput")
        self.radiusLabel = QtWidgets.QLabel(self.singleBox)
        self.radiusLabel.setGeometry(QtCore.QRect(20, 90, 121, 16))
        self.radiusLabel.setObjectName("radiusLabel")
        self.radiusInput = QtWidgets.QLineEdit(self.singleBox)
        self.radiusInput.setGeometry(QtCore.QRect(190, 90, 61, 22))
        self.radiusInput.setObjectName("radiusInput")
        self.singleDrawButton = QtWidgets.QPushButton(self.singleBox)
        self.singleDrawButton.setGeometry(QtCore.QRect(20, 120, 121, 28))
        self.singleDrawButton.setObjectName("singleDrawButton")
        self.seriesBox = QtWidgets.QGroupBox(self.Circle)
        self.seriesBox.setGeometry(QtCore.QRect(10, 180, 411, 221))
        self.seriesBox.setObjectName("seriesBox")
        self.alg1Label = QtWidgets.QLabel(self.seriesBox)
        self.alg1Label.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.alg1Label.setObjectName("alg1Label")
        self.alg1Choice = QtWidgets.QComboBox(self.seriesBox)
        self.alg1Choice.setGeometry(QtCore.QRect(190, 30, 201, 22))
        self.alg1Choice.setObjectName("alg1Choice")
        self.startLabel = QtWidgets.QLabel(self.seriesBox)
        self.startLabel.setGeometry(QtCore.QRect(20, 90, 151, 16))
        self.startLabel.setObjectName("startLabel")
        self.startInput = QtWidgets.QLineEdit(self.seriesBox)
        self.startInput.setGeometry(QtCore.QRect(190, 90, 61, 22))
        self.startInput.setObjectName("startInput")
        self.endLabel = QtWidgets.QLabel(self.seriesBox)
        self.endLabel.setGeometry(QtCore.QRect(20, 120, 151, 16))
        self.endLabel.setObjectName("endLabel")
        self.endInput = QtWidgets.QLineEdit(self.seriesBox)
        self.endInput.setGeometry(QtCore.QRect(190, 120, 61, 22))
        self.endInput.setObjectName("endInput")
        self.seriesDrawButton = QtWidgets.QPushButton(self.seriesBox)
        self.seriesDrawButton.setGeometry(QtCore.QRect(20, 180, 121, 28))
        self.seriesDrawButton.setObjectName("seriesDrawButton")
        self.alg2Label = QtWidgets.QLabel(self.seriesBox)
        self.alg2Label.setGeometry(QtCore.QRect(20, 60, 121, 16))
        self.alg2Label.setObjectName("alg2Label")
        self.alg2Choice = QtWidgets.QComboBox(self.seriesBox)
        self.alg2Choice.setGeometry(QtCore.QRect(190, 60, 201, 22))
        self.alg2Choice.setObjectName("alg2Choice")
        self.stepLabel = QtWidgets.QLabel(self.seriesBox)
        self.stepLabel.setGeometry(QtCore.QRect(20, 150, 121, 16))
        self.stepLabel.setObjectName("stepLabel")
        self.stepInput = QtWidgets.QLineEdit(self.seriesBox)
        self.stepInput.setGeometry(QtCore.QRect(190, 150, 61, 22))
        self.stepInput.setObjectName("stepInput")
        self.timeButton_2 = QtWidgets.QPushButton(self.Circle)
        self.timeButton_2.setGeometry(QtCore.QRect(20, 410, 351, 28))
        self.timeButton_2.setObjectName("timeButton_2")
        self.tabWidget.addTab(self.Circle, "")
        self.Ellipse = QtWidgets.QWidget()
        self.Ellipse.setObjectName("Ellipse")
        self.seriesBox_1 = QtWidgets.QGroupBox(self.Ellipse)
        self.seriesBox_1.setGeometry(QtCore.QRect(10, 180, 411, 221))
        self.seriesBox_1.setObjectName("seriesBox_1")
        self.alg1Label_1 = QtWidgets.QLabel(self.seriesBox_1)
        self.alg1Label_1.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.alg1Label_1.setObjectName("alg1Label_1")
        self.alg1Choice_1 = QtWidgets.QComboBox(self.seriesBox_1)
        self.alg1Choice_1.setGeometry(QtCore.QRect(190, 30, 201, 22))
        self.alg1Choice_1.setObjectName("alg1Choice_1")
        self.startLabel_1 = QtWidgets.QLabel(self.seriesBox_1)
        self.startLabel_1.setGeometry(QtCore.QRect(20, 90, 121, 16))
        self.startLabel_1.setObjectName("startLabel_1")
        self.startInput_1 = QtWidgets.QLineEdit(self.seriesBox_1)
        self.startInput_1.setGeometry(QtCore.QRect(190, 90, 61, 22))
        self.startInput_1.setObjectName("startInput_1")
        self.endLabel_1 = QtWidgets.QLabel(self.seriesBox_1)
        self.endLabel_1.setGeometry(QtCore.QRect(20, 120, 121, 16))
        self.endLabel_1.setObjectName("endLabel_1")
        self.endInput_1 = QtWidgets.QLineEdit(self.seriesBox_1)
        self.endInput_1.setGeometry(QtCore.QRect(190, 120, 61, 22))
        self.endInput_1.setObjectName("endInput_1")
        self.seriesDrawButton_1 = QtWidgets.QPushButton(self.seriesBox_1)
        self.seriesDrawButton_1.setGeometry(QtCore.QRect(20, 180, 121, 28))
        self.seriesDrawButton_1.setObjectName("seriesDrawButton_1")
        self.alg2Label_1 = QtWidgets.QLabel(self.seriesBox_1)
        self.alg2Label_1.setGeometry(QtCore.QRect(20, 60, 121, 16))
        self.alg2Label_1.setObjectName("alg2Label_1")
        self.alg2Choice_1 = QtWidgets.QComboBox(self.seriesBox_1)
        self.alg2Choice_1.setGeometry(QtCore.QRect(190, 60, 201, 22))
        self.alg2Choice_1.setObjectName("alg2Choice_1")
        self.qtyLabel = QtWidgets.QLabel(self.seriesBox_1)
        self.qtyLabel.setGeometry(QtCore.QRect(20, 150, 121, 16))
        self.qtyLabel.setObjectName("qtyLabel")
        self.qtyInput = QtWidgets.QLineEdit(self.seriesBox_1)
        self.qtyInput.setGeometry(QtCore.QRect(190, 150, 61, 22))
        self.qtyInput.setObjectName("qtyInput")
        self.singleBox_1 = QtWidgets.QGroupBox(self.Ellipse)
        self.singleBox_1.setGeometry(QtCore.QRect(10, 10, 411, 161))
        self.singleBox_1.setObjectName("singleBox_1")
        self.algLabel_1 = QtWidgets.QLabel(self.singleBox_1)
        self.algLabel_1.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.algLabel_1.setObjectName("algLabel_1")
        self.algChoice_1 = QtWidgets.QComboBox(self.singleBox_1)
        self.algChoice_1.setGeometry(QtCore.QRect(190, 30, 201, 22))
        self.algChoice_1.setObjectName("algChoice_1")
        self.centerLabel_1 = QtWidgets.QLabel(self.singleBox_1)
        self.centerLabel_1.setGeometry(QtCore.QRect(20, 60, 121, 16))
        self.centerLabel_1.setObjectName("centerLabel_1")
        self.centerInput_1 = QtWidgets.QLineEdit(self.singleBox_1)
        self.centerInput_1.setGeometry(QtCore.QRect(190, 60, 61, 22))
        self.centerInput_1.setObjectName("centerInput_1")
        self.radiusLabel_1 = QtWidgets.QLabel(self.singleBox_1)
        self.radiusLabel_1.setGeometry(QtCore.QRect(20, 90, 121, 16))
        self.radiusLabel_1.setObjectName("radiusLabel_1")
        self.radiusInput_1 = QtWidgets.QLineEdit(self.singleBox_1)
        self.radiusInput_1.setGeometry(QtCore.QRect(190, 90, 61, 22))
        self.radiusInput_1.setObjectName("radiusInput_1")
        self.singleDrawButton_1 = QtWidgets.QPushButton(self.singleBox_1)
        self.singleDrawButton_1.setGeometry(QtCore.QRect(20, 120, 121, 28))
        self.singleDrawButton_1.setObjectName("singleDrawButton_1")
        self.timeButton_1 = QtWidgets.QPushButton(self.Ellipse)
        self.timeButton_1.setGeometry(QtCore.QRect(20, 410, 351, 28))
        self.timeButton_1.setObjectName("timeButton_1")
        self.tabWidget.addTab(self.Ellipse, "")
        self.canvas = QtWidgets.QLabel(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(20, 20, 861, 861))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.canvas.setPalette(palette)
        self.canvas.setText("")
        self.canvas.setObjectName("canvas")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(900, 20, 441, 111))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        self.groupBox.setPalette(palette)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.clearButton = QtWidgets.QPushButton(self.groupBox)
        self.clearButton.setGeometry(QtCore.QRect(10, 70, 121, 28))
        self.clearButton.setObjectName("clearButton")
        self.colorButton = QtWidgets.QPushButton(self.groupBox)
        self.colorButton.setGeometry(QtCore.QRect(140, 10, 26, 25))
        self.colorButton.setText("")
        self.colorButton.setObjectName("colorButton")
        self.scaleInput = QtWidgets.QLineEdit(self.groupBox)
        self.scaleInput.setGeometry(QtCore.QRect(140, 40, 61, 22))
        self.scaleInput.setObjectName("scaleInput")
        self.colorLabel = QtWidgets.QLabel(self.groupBox)
        self.colorLabel.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.colorLabel.setObjectName("colorLabel")
        self.scaleLabel = QtWidgets.QLabel(self.groupBox)
        self.scaleLabel.setGeometry(QtCore.QRect(10, 40, 121, 16))
        self.scaleLabel.setObjectName("scaleLabel")
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(920, 660, 401, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.errorLabel.setPalette(palette)
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.singleBox.setTitle(_translate("MainWindow", "Одиночная окружность"))
        self.algLabel.setText(_translate("MainWindow", "Алгоритм"))
        self.centerLabel.setText(_translate("MainWindow", "Центр"))
        self.radiusLabel.setText(_translate("MainWindow", "Радиус"))
        self.singleDrawButton.setText(_translate("MainWindow", "Построить"))
        self.seriesBox.setTitle(_translate("MainWindow", "Спектр концентрических окружностей"))
        self.alg1Label.setText(_translate("MainWindow", "Алгоритм 1"))
        self.startLabel.setText(_translate("MainWindow", "Начальный радиус"))
        self.endLabel.setText(_translate("MainWindow", "Конечный радиус"))
        self.seriesDrawButton.setText(_translate("MainWindow", "Построить"))
        self.alg2Label.setText(_translate("MainWindow", "Алгоритм 2"))
        self.stepLabel.setText(_translate("MainWindow", "Шаг"))
        self.timeButton_2.setText(_translate("MainWindow", "Сравнение временных характеристик"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Circle), _translate("MainWindow", "Окружность"))
        self.seriesBox_1.setTitle(_translate("MainWindow", "Спектр концентрических эллипсов"))
        self.alg1Label_1.setText(_translate("MainWindow", "Алгоритм 1"))
        self.startLabel_1.setText(_translate("MainWindow", "Начальные полуоси"))
        self.endLabel_1.setText(_translate("MainWindow", "Конечные полуоси"))
        self.seriesDrawButton_1.setText(_translate("MainWindow", "Построить"))
        self.alg2Label_1.setText(_translate("MainWindow", "Алгоритм 2"))
        self.qtyLabel.setText(_translate("MainWindow", "Кол-во эллипсов"))
        self.singleBox_1.setTitle(_translate("MainWindow", "Одиночный эллипс"))
        self.algLabel_1.setText(_translate("MainWindow", "Алгоритм"))
        self.centerLabel_1.setText(_translate("MainWindow", "Центр"))
        self.radiusLabel_1.setText(_translate("MainWindow", "Полуоси"))
        self.singleDrawButton_1.setText(_translate("MainWindow", "Построить"))
        self.timeButton_1.setText(_translate("MainWindow", "Сравнение временных характеристик"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ellipse), _translate("MainWindow", "Эллипс"))
        self.clearButton.setText(_translate("MainWindow", "Очистить"))
        self.colorLabel.setText(_translate("MainWindow", "Цвет"))
        self.scaleLabel.setText(_translate("MainWindow", "Масштаб"))
