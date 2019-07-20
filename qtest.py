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
    QPushButton, QApplication, QVBoxLayout, QLabel)
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


class ToolBox(QWidget):
    def __init__(self, parent):
        super(ToolBox, self).__init__(parent)
        self.parent = parent
        print('ToolBox: my parent is',self.parent)
        self.initUI()

    def initUI(self):
        btn = [QPushButton('B', self) for i in range(6)]
        for Btn in btn:
            Btn.resize(30, 30)
        self.resize(60, 90)
        k = 0
        for i in range(6):
            btn[i].move((i%2)*30, k*30)
            k += 1 if i % 2 == 1 else 0


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

        toolbox = ToolBox(self)
        scaleframe = ScaleFrame(self)

        layout.addWidget(toolbox)
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
        self.setWindowTitle('Icon')
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