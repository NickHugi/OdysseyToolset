from PyQt5.QtWidgets import QWidget

from ui import waypoint_editor


class WaypointEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = waypoint_editor.Ui_Form()
        self.ui.setupUi(self)

