from PyQt5.QtWidgets import QWidget

from ui import merchant_editor


class MerchantEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = merchant_editor.Ui_Form()
        self.ui.setupUi(self)

