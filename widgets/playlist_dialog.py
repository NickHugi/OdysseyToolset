from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QCheckBox, QSpinBox, QDoubleSpinBox

from ui import creatures_dialog


class PlaylistDialog(QDialog):
    def __init__(self, parent, playlist, installation=None):
        QDialog.__init__(self, parent)

        self.ui = creatures_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.add_button.clicked.connect(self.add_creature)
        self.ui.remove_button.clicked.connect(self.remove_creature)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Sound"])
        self.ui.table.setModel(self.model)

        self.set_playlist(playlist)

    def set_playlist(self, playlist):
        for sound in playlist:
            self.add_creature(sound)

    def get_playlist(self):
        playlist = []
        for i in range(self.model.rowCount()):
            playlist.append(self.model.item(i, 0).text())
        return playlist

    def add_creature(self, sound=""):
        row = self.model.rowCount()
        self.model.insertRow(row)
        self.model.setItem(row, QStandardItem(sound))

    def remove_creature(self):
        index = self.ui.table.selectedIndexes()[0]
        item = self.model.itemFromIndex(index)
        row = item.row()
        self.model.takeRow(row)

