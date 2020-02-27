from PyQt5.QtWidgets import QMainWindow

from ui import tlk_editor


class TLKEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = tlk_editor.Ui_MainWindow()
        self.ui.setupUi(self)
