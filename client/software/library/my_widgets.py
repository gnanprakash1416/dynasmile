from PyQt5 import QtCore, QtGui, QtWidgets


class RightClickLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__(parent=None)

    # if pyqt5,this line should be pyqtsignal
    mysignal = QtCore.pyqtSignal(str)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.RightButton:
            self.mysignal.emit('click')
            print(a0)
        return super().mousePressEvent(a0)
