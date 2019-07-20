#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""


Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
import os
from PyQt5.QtWidgets import (QFrame, QDesktopWidget, QMainWindow, QAction, QWidget, qApp, QGridLayout,
    QPushButton, QApplication, QVBoxLayout, QLabel, QLineEdit)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect
from PyQt5.QtGui import (QIcon, QFont, QPainter, QBrush, QColor)

from scale import Scale

class ScaleFrame(QFrame):
    def __init__(self, parent):
        super(ScaleFrame, self).__init__(parent)
        self.parent = parent
        print('ScaleFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        self.timer = QBasicTimer()
        self.myscale = Scale(10202)

        self.lbl_weight = QLabel(self)
        self.lbl_weight.setObjectName('lbl_weight')
        self.lbl_weight.setText("0.000")
        self.lbl_weight.resize(500, 100)
        self.lbl_weight.move(200, 50)

        lbl_unit = QLabel(self)
        lbl_unit.setObjectName('lbl_unit')
        lbl_unit.setText("kg")
        lbl_unit.resize(100, 120)
        lbl_unit.move(500, 40)

        #self.lbl_status = QLabel(self)
        #self.lbl_status.setText("MAYBE ON")
        #self.lbl_status.resize(100, 100)
        #self.lbl_status.move(700, 10)


        #qbtn = QPushButton('Jalla', self)
        #qbtn.clicked.connect(QApplication.instance().quit)
        #qbtn.resize(qbtn.sizeHint())
        #qbtn.move(150, 150)

        self.setObjectName('ScaleFrame')
        self.setStyleSheet("""
            #ScaleFrame {
                background-color: #cfcfcf;
            }
            .QLabel#lbl_weight {
                font-size:100pt;
                color: #ff0000;
            }
            .QLabel#lbl_unit {
                font-size:100pt;
                color: #000000;
            }
            .QLabel {
                font-size:22pt;
                color: #000000;
            }
        """)
        self.start_timer()

    def start_timer(self):
        self.timer.start(100, self)

    def timerEvent(self, event):
        '''handles timer event'''
        if event.timerId() == self.timer.timerId():
            time_last_received, weight = self.myscale.return_last_weight()
            self.window().statusbar.showMessage(F"Last received: {time_last_received}")
            self.lbl_weight.setText(F"{weight:.3f}")
        else:
            super(Board, self).timerEvent(event)


class LabelFrame(QWidget):
    def __init__(self, parent):
        super(LabelFrame, self).__init__(parent)
        self.parent = parent
        print('LabelFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        layout = QGridLayout()

        lbl_language = QLabel('Language')
        input_language = QLineEdit()

        lbl_product = QLabel('Product')
        input_product = QLineEdit()

        lbl_grade = QLabel('Grade')
        input_grade = QLineEdit()

        lbl_processing = QLabel('Processing')
        input_processing = QLineEdit()

        lbl_batch = QLabel('Processing')
        input_batch = QLineEdit()

        lbl_harvest_date = QLabel('Harvest date')
        input_harvest_date = QLineEdit()

        lbl_customer = QLabel('Customer')
        input_customer = QLineEdit()

        layout.setSpacing(10)
        layout.addWidget(lbl_language, 1, 0)
        layout.addWidget(input_language, 1, 1)
        layout.addWidget(lbl_product, 2, 0)
        layout.addWidget(input_product, 2, 1)
        layout.addWidget(lbl_grade, 3, 0)
        layout.addWidget(input_grade, 3, 1)
        layout.addWidget(lbl_processing, 4, 0)
        layout.addWidget(input_processing, 4, 1)
        layout.addWidget(lbl_batch, 5, 0)
        layout.addWidget(input_batch, 5, 1)
        layout.addWidget(lbl_harvest_date, 6, 0)
        layout.addWidget(input_harvest_date, 6, 1)
        layout.addWidget(lbl_customer, 7, 0)
        layout.addWidget(input_customer, 7, 1)
        self.setLayout(layout) 


class CentralFrame(QFrame):
    def __init__(self, parent):
        super(CentralFrame, self).__init__(parent)
        self.parent = parent
        print('CentralFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        layout = QVBoxLayout()


        printbtn = QPushButton('Print Label', self)
        printbtn.clicked.connect(QApplication.instance().quit)
        printbtn.resize(printbtn.sizeHint())

        labelframe = LabelFrame(self)
        scaleframe = ScaleFrame(self)

        layout.addWidget(labelframe)
        layout.addWidget(scaleframe)
        layout.addWidget(printbtn)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent
        print('MainWindow: my parent is',self.parent)
        self.initUI()

    def initUI(self):


        centralframe = CentralFrame(self)
        self.setCentralWidget(centralframe)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setMenuRole(QAction.NoRole)
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon.png')
        self.setWindowIcon(QIcon(path))
        self.setGeometry(800, 600, 800, 600)
        self.center()
        self.setWindowTitle('Seafood Packing Software')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parent = QMainWindow()
    mainwindow = MainWindow(parent)
    sys.exit(app.exec_())