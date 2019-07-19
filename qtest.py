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
    QPushButton, QApplication, QVBoxLayout)
from PyQt5.QtGui import (QIcon, QFont)


class ScaleFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.initFrame()

    def initFrame(self):
        qbtn = QPushButton('Jalla', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 150)
        self.setObjectName('MainWidget')
        self.setStyleSheet("""
            #MainWidget {
                background-color: #00ff00;
            }
            .QLabel {
                color: #fff;
            }
        """)

class ToolBox(QWidget):
    def __init__(self):
        super().__init__()
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
    def __init__(self):
        super().__init__()
        self.initFrame()

    def initFrame(self):

        layout = QVBoxLayout()


        qbtn = QPushButton('Queit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())


        toolbox = ToolBox()

        scaleframe = ScaleFrame()
        #scaleframe.setFrameShadow(QFrame.Sunken)
        #scaleframe.resize(200,200)
        #scaleframe.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        #scaleframe.move(50, 50)

        layout.addWidget(toolbox)
        layout.addWidget(qbtn)
        layout.addWidget(scaleframe)
        self.setLayout(layout)

        #testcolor = QPalette().color(QPalette.Window)
        #self.setStyleSheet('QPlainTextEdit[readOnly="true"] { background-color: %s;} QFrame {border: 0px}' % testcolor.name() )
        #self.setPalette(QPalette(self.colorForLanguage('green')))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        centralframe = CentralFrame()
        self.setCentralWidget(centralframe)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setMenuRole(QAction.NoRole)
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

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
    mainwindow = MainWindow()
    sys.exit(app.exec_())