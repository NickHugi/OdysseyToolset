from PyQt5.QtWidgets import QWidget

from ui import sound_editor


class SoundEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = sound_editor.Ui_Form()
        self.ui.setupUi(self)

