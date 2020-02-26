from PyQt5.QtWidgets import QMainWindow
from ui.toolset_ui import Ui_MainWindow


class Toolset(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        
