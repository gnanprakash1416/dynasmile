from PyQt5.QtCore import QThread, pyqtSignal
def thread_checker(name='function'):
    print(f"function in thread: {QThread.currentThread().objectName()}")  # 查询当前线程

        