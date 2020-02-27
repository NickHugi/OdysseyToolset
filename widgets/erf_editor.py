from PyQt5.QtWidgets import QMainWindow

from ui import erf_editor


class ERFEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = erf_editor.Ui_MainWindow()
        self.ui.setupUi(self)
