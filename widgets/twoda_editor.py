from PyQt5.QtWidgets import QMainWindow

from ui import twoda_editor


class TwoDAEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = twoda_editor.Ui_MainWindow()
        self.ui.setupUi(self)
