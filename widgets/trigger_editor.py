from PyQt5.QtWidgets import QWidget

from ui import trigger_editor


class TriggerEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = trigger_editor.Ui_Form()
        self.ui.setupUi(self)

