from PyQt5.QtWidgets import QWidget

from ui import item_editor


class ItemEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = item_editor.Ui_Form()
        self.ui.setupUi(self)

