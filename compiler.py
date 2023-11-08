import sys
# import os
# import time
# from multiprocessing import Process
# from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, \
    QLabel, QWidget
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt, QObject, QThread


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(362, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 336, 192))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 270, 331, 200))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 470, 141, 31))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Twitch"))
        self.pushButton.setText(_translate("MainWindow", "Закрыть"))


class Thread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(str)

    def __init__(self, status, parent=None):
        super(Thread, self).__init__(parent)
        self.status = status
        self.i = 0

    def run(self):
        while True:
            self.updateSignal.emit(f'{self.status}{self.i}')
            self.i += 1
            self.msleep(1000)


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self, status):
        super().__init__()
        self.setupUi(self)

        self.status = status
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(170, 470, 141, 31))

        self.btnThread = QtWidgets.QPushButton("btnThread", self.centralwidget)
        self.btnThread.setGeometry(QtCore.QRect(170, 370, 141, 31))
        self.btnThread.setObjectName("btnThread")


        self.statusUpgrader(status)
        self.start_thread()
    def statusUpgrader(self, status):
        self.label.setText(str(status))
        self.progress.setValue(int(status))

    def exit(self):
        raise SystemExit(1)

    def start_thread(self):
        self.btnThread.setEnabled(False)

        self.thread = Thread(self.status)
        self.thread.updateSignal.connect(self.statusUpgrader)
        self.thread.start()



status = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(status)
    w.show()
    sys.exit(app.exec())