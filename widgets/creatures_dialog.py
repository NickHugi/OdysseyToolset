from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QCheckBox, QSpinBox, QDoubleSpinBox

from ui import creatures_dialog


class CreaturesDialog(QDialog):
    def __init__(self, parent, creatures, installation=None):
        QDialog.__init__(self, parent)

        self.ui = creatures_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        #self.ui.add_button.clicked.connect(self.add_creature)
        self.ui.add_button.clicked.connect(lambda state, x=EncounteredCreature(): self.add_creature(x))
        self.ui.remove_button.clicked.connect(self.remove_creature)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ResRef", "Guaranteed Count", "Single Spawn", "Challenge Rating", "Appearance"])
        self.ui.table.setModel(self.model)

        self.set_creatures(creatures)

    def set_creatures(self, creatures):
        for creature in creatures:
            self.add_creature(creature)

    def get_creatures(self):
        creatures = []
        for i in range(self.model.rowCount()):
            creature = EncounteredCreature()
            creature.res_ref = self.model.item(i, 0).text()
            creature.guaranteed_count = self.ui.table.indexWidget(self.model.index(i, 1)).value()
            creature.single_spawn = self.ui.table.indexWidget(self.model.index(i, 2)).isChecked()
            creature.challenge_rating = self.ui.table.indexWidget(self.model.index(i, 3)).value()
            creature.appearance = self.ui.table.indexWidget(self.model.index(i, 4)).value()
            creatures.append(creature)
        return creatures

    def add_creature(self, creature):
        row = self.model.rowCount()
        self.model.insertRow(row)

        self.ui.table.setIndexWidget(self.model.index(row, 1), QSpinBox())
        self.ui.table.setIndexWidget(self.model.index(row, 4), QSpinBox())
        self.ui.table.setIndexWidget(self.model.index(row, 3), QDoubleSpinBox())
        self.ui.table.setIndexWidget(self.model.index(row, 2), QCheckBox())

        self.model.setItem(row, QStandardItem(creature.res_ref))
        self.ui.table.indexWidget(self.model.index(row, 1)).setValue(creature.guaranteed_count)
        self.ui.table.indexWidget(self.model.index(row, 2)).setChecked(creature.single_spawn)
        self.ui.table.indexWidget(self.model.index(row, 3)).setValue(creature.challenge_rating)
        self.ui.table.indexWidget(self.model.index(row, 4)).setMaximum(99999)
        self.ui.table.indexWidget(self.model.index(row, 4)).setValue(creature.appearance)

    def remove_creature(self):
        index = self.ui.table.selectedIndexes()[0]
        item = self.model.itemFromIndex(index)
        row = item.row()
        self.model.takeRow(row)


class EncounteredCreature:
    def __init__(self):
        self.res_ref = ""
        self.guaranteed_count = 0
        self.single_spawn = False
        self.appearance = 0
        self.challenge_rating = 0.0
