from PyQt5.QtWidgets import QWidget

from ui import creature_editor


class CreatureEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = creature_editor.Ui_Form()
        self.ui.setupUi(self)

