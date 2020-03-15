from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialog, QCheckBox, QTableWidgetItem

from ui import ability_dialog


class AbilityDialog(QDialog):
    def __init__(self, parent, bools, abilities):
        QDialog.__init__(self, parent)

        self.ui = ability_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.model = QStandardItemModel()
        self.ui.table.setModel(self.model)
        self.build_table(bools, abilities)

    def build_table(self, bools, abilities):
        for id, name in enumerate(abilities):
            if name != "":
                item = QStandardItem(name)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.ability_id = id
                self.model.appendRow([item])
                self.model.setVerticalHeaderItem(self.model.rowCount()-1, QStandardItem(str(id)))

                if id in bools and bools[id] is True:
                    item.setCheckState(QtCore.Qt.Checked)

    def get_bools(self):
        bools = {}
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            ability_id = item.ability_id
            checked = bool(item.checkState())
            bools[ability_id] = checked
        return bools

