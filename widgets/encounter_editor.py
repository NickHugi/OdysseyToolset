from PyQt5.QtWidgets import QWidget

from ui import encounter_editor


class EncounterEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = encounter_editor.Ui_Form()
        self.ui.setupUi(self)

