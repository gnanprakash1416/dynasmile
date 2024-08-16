import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsSceneHoverEvent, QMainWindow, QDialog, QFileDialog
from PyQt5.QtGui import QImage
# from PyQt5.Qt import QStandardPaths
from library.read_csv import Ui_Dialog
import cv2
import imutils
import csv


class CustomUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，self 就是一个 QMainWindow 对象
        self.ui = Ui_Dialog()  # 创建UI 对象
        self.ui.setupUi(self)  # 构造UIm

        self.ui.pushButton.clicked.connect(self.open_file)
        self.ui.buttonBox.accepted.connect(self.ok_api)
        # self.fileopener=QFileDialog.getOpenFileName(self,"choose csv","C:/","(*.csv)")
        # self.ui.horizontalLayout.addItem(self.fileopener)
        # self.csv_source=''

    def open_file(self):
        self.file = QFileDialog.getOpenFileName(
            self, "choose csv", "C:/", "(*.csv)")
        self.csv_source = str(self.file[0])
        self.ui.lineEdit.setText(self.csv_source)

    def ok_api(self):
        print("ok")
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建app，用 QApplication 类
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
