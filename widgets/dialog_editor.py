from PyQt5.QtWidgets import QWidget

from ui import dialog_editor


class DialogEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = dialog_editor.Ui_Form()
        self.ui.setupUi(self)

