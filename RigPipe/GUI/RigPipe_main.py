import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtWidgets as qtw


from RigPipe.GUI.RigPipeUI import Ui_MainWindow
# Subclass QMainWindow to customize your application's main window
class RigPipeWindow(qtw.QWidget,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)




if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = RigPipeWindow()
    window.show

    sys.exit(app.exec_())

