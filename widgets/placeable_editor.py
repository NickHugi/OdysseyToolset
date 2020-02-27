from PyQt5.QtWidgets import QWidget

from ui import placeable_editor


class PlaceableEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = placeable_editor.Ui_Form()
        self.ui.setupUi(self)

