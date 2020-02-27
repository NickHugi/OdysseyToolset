from PyQt5.QtWidgets import QWidget

from ui import door_editor


class DoorEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = door_editor.Ui_Form()
        self.ui.setupUi(self)

