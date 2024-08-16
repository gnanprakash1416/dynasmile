import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsSceneHoverEvent, QMainWindow, QDialog, QFileDialog
from PyQt5.QtGui import QImage
# from PyQt5.Qt import QStandardPaths
from library.write_csv import Ui_Dialog_save_to_csv
import cv2
import imutils
import csv


class CustomUI(QDialog):
    mysignal = QtCore.pyqtSignal(str)

    identity_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，self 就是一个 QMainWindow 对象
        self.ui = Ui_Dialog_save_to_csv()  # 创建UI 对象
        self.ui.setupUi(self)  # 构造UIm

        '''By default you can not use the save image function.
        '''
        test_mode = False
        self.ui.pushButton_2.setVisible(False)
        self.ui.lineEdit_2.setVisible(False)

        self.ui.checkBox_AI.setVisible(False)
        self.ui.checkBox_tester1.setVisible(False)
        self.ui.checkBox_tester2.setVisible(False)

        if test_mode == True:
            self.ui.checkBox_AI.setVisible(True)
            self.ui.checkBox_tester1.setVisible(True)
            self.ui.checkBox_AI.setVisible(True)
            self.ui.checkBox_AI.click()

            self.ui.checkBox_AI.stateChanged.connect(self.AI_selection)
            self.ui.checkBox_tester1.stateChanged.connect(
                self.tester1_selection)
            self.ui.checkBox_tester2.stateChanged.connect(
                self.tester2_selection)

            self.identity_signal.emit("AI")

        self.ui.pushButton.clicked.connect(self.open_file)
        # self.fileopener=QFileDialog.getOpenFileName(self,"choose csv","C:/","(*.csv)")
        # self.ui.horizontalLayout.addItem(self.fileopener)
        self.ui.buttonBox.accepted.connect(self.ok_api)
        self.ui.checkBox.stateChanged.connect(self.save_with_image)

    def open_file(self):
        # self.file=QFileDialog.getOpenFileName(self,"choose csv","C:/","(*.csv)")
        self.file = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # self.csv_source=str(self.file[0])
        self.csv_source = str(self.file)  # the source folder
        # self.ui.lineEdit.setText(str(self.file[0]))
        self.ui.lineEdit.setText(str(self.file))

    def ok_api(self):
        print("ok")
        if self.ui.checkBox_AI.isChecked() == False and self.ui.checkBox_tester1.isChecked() == False and self.ui.checkBox_tester2.isChecked() == False:
            # if no chekcbox is clicked, you have to click the AI to ensure everything goes all right.
            self.ui.checkBox_AI.click()
        pass

    def save_with_image(self):
        if self.ui.checkBox.isChecked():
            self.mysignal.emit('true')
            # self.ui.pushButton_2.setVisible(True)
            # self.ui.lineEdit_2.setVisible(True)
        else:
            self.mysignal.emit('false')
            # self.ui.pushButton_2.setVisible(False)
            # self.ui.lineEdit_2.setVisible(False)

    def AI_selection(self):
        if self.ui.checkBox_AI.isChecked():
            self.ui.checkBox_tester1.setCheckState(0)
            self.ui.checkBox_tester2.setCheckState(0)
            self.identity_signal.emit("AI")

    def tester1_selection(self):
        if self.ui.checkBox_tester1.isChecked():
            self.ui.checkBox_AI.setCheckState(0)
            self.ui.checkBox_tester2.setCheckState(0)
            self.identity_signal.emit("tester1")

    def tester2_selection(self):
        if self.ui.checkBox_tester2.isChecked():
            self.ui.checkBox_AI.setCheckState(0)
            self.ui.checkBox_tester1.setCheckState(0)
            self.identity_signal.emit("tester2")


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建app，用 QApplication 类
    cutomUI = CustomUI()
    cutomUI.show()
    sys.exit(app.exec_())
