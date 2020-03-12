from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QDialog, QTreeWidgetItem, QSpinBox, QCheckBox, QLineEdit

from pykotor.globals import Equipment
from ui import inventory_dialog


class InventoryDialog(QDialog):
    def __init__(self, parent, inventory, container="human", installation=None, module=None):
        QDialog.__init__(self, parent)

        self.ui = inventory_dialog.Ui_Form()
        self.ui.setupUi(self)

        self.container = container

        self.model = QStandardItemModel()
        self.ui.inventory_table.setModel(self.model)
        self.ui.inventory_table.model().setHorizontalHeaderLabels(["ResRef", "Quantity", "Dropable"])

        self.set_inventory(inventory)
        self.installation = installation
        self.module = module

        self.ui.head_name.hide()
        self.ui.implant_name.hide()
        self.ui.gauntlet_name.hide()
        self.ui.belt_name.hide()
        self.ui.armor_name.hide()
        self.ui.leftarm_name.hide()
        self.ui.rightarm_name.hide()
        self.ui.lefthand_name.hide()
        self.ui.righthand_name.hide()
        self.ui.hide_name.hide()
        self.ui.creature1_name.hide()
        self.ui.creature2_name.hide()
        self.ui.creature3_name.hide()

        if self.container == "placeable":
            self.ui.equipment_tabs.hide()
            self.ui.inventory_table.hideColumn(2)

        # TODO: item tree
        self.ui.items_tree.hide()

        #if installation is not None:
        #    core_items = installation.chitin.resources_by_type("uti")
        #    for item in core_items:
        #        self.ui.items_tree.insertTopLevelItem(0, QTreeWidgetItem([item, ""]))

    def set_droid_labels(self):
        self.ui.implant_label.setText("Utility")
        self.ui.gauntlet_label.setText("Utility")
        self.ui.head_label.setText("Sensor")
        self.ui.armor_label.setText("Plating")
        self.ui.belt_label.setText("Shield")
        self.ui.leftarm_label.setText("Special Weapon")
        self.ui.rightarm_label.setText("Special Weapon")
        self.ui.lefthand_label.setText("Left Weapon")
        self.ui.righthand_label.setText("Right Weapon")

    def get_inventory(self):
        inventory = Inventory()

        if self.ui.head_edit.text() != "": inventory.equipment[Equipment.Head] = self.ui.head_edit.text()
        if self.ui.implant_edit.text() != "": inventory.equipment[Equipment.Implant] = self.ui.implant_edit.text()
        if self.ui.gauntlet_edit.text() != "": inventory.equipment[Equipment.Gauntlet] = self.ui.gauntlet_edit.text()
        if self.ui.belt_edit.text() != "": inventory.equipment[Equipment.Belt] = self.ui.belt_edit.text()
        if self.ui.armor_edit.text() != "": inventory.equipment[Equipment.Armor] = self.ui.armor_edit.text()
        if self.ui.leftarm_edit.text() != "": inventory.equipment[Equipment.LeftArm] = self.ui.leftarm_edit.text()
        if self.ui.rightarm_edit.text() != "": inventory.equipment[Equipment.RightArm] = self.ui.rightarm_edit.text()
        if self.ui.lefthand_edit.text() != "": inventory.equipment[Equipment.LeftHand] = self.ui.lefthand_edit.text()
        if self.ui.righthand_edit.text() != "": inventory.equipment[Equipment.RightHand] = self.ui.righthand_edit.text()
        if self.ui.hide_edit.text() != "": inventory.equipment[Equipment.Hide] = self.ui.hide_edit.text()
        if self.ui.creature1_edit.text() != "": inventory.equipment[Equipment.CreatureItem1] = self.ui.creature1_edit.text()
        if self.ui.creature2_edit.text() != "": inventory.equipment[Equipment.CreatureItem2] = self.ui.creature2_edit.text()
        if self.ui.creature3_edit.text() != "": inventory.equipment[Equipment.CreatureItem3] = self.ui.creature3_edit.text()

        for i in range(self.model.rowCount()):
            res_ref = self.model.item(i, 0).text()
            quantity = int(self.model.item(i, 1).text())
            dropable = True if self.model.item(i, 2).checkState() == 2 else False
            for j in range(quantity):
                inventory.items.append(InventoryItem(res_ref, dropable))

        return inventory

    def set_inventory(self, inventory):
        equipment = inventory.equipment
        if Equipment.Head in equipment: self.ui.head_edit.setText(inventory.equipment[Equipment.Head])
        if Equipment.Implant in equipment: self.ui.implant_edit.setText(inventory.equipment[Equipment.Implant])
        if Equipment.Gauntlet in equipment: self.ui.gauntlet_edit.setText(inventory.equipment[Equipment.Gauntlet])
        if Equipment.Belt in equipment: self.ui.belt_edit.setText(inventory.equipment[Equipment.Belt])
        if Equipment.Armor in equipment: self.ui.armor_edit.setText(inventory.equipment[Equipment.Armor])
        if Equipment.LeftArm in equipment: self.ui.leftarm_edit.setText(inventory.equipment[Equipment.LeftArm])
        if Equipment.RightArm in equipment: self.ui.rightarm_edit.setText(inventory.equipment[Equipment.RightArm])
        if Equipment.LeftHand in equipment: self.ui.lefthand_edit.setText(inventory.equipment[Equipment.LeftHand])
        if Equipment.RightHand in equipment: self.ui.righthand_edit.setText(inventory.equipment[Equipment.RightHand])
        if Equipment.Hide in equipment: self.ui.hide_edit.setText(inventory.equipment[Equipment.Hide])
        if Equipment.CreatureItem1 in equipment: self.ui.creature1_edit.setText(inventory.equipment[Equipment.CreatureItem1])
        if Equipment.CreatureItem2 in equipment: self.ui.creature2_edit.setText(inventory.equipment[Equipment.CreatureItem2])
        if Equipment.CreatureItem3 in equipment: self.ui.creature3_edit.setText(inventory.equipment[Equipment.CreatureItem3])

        for item in inventory.items:
            row_id = self.model.rowCount()
            self.model.insertRow(row_id)

            resref_item = QStandardItem()
            resref_item.setText(item.res_ref)
            self.model.setItem(row_id, 0, resref_item)

            quantity_item = QStandardItem()
            quantity_item.setText("1")
            self.model.setItem(row_id, 1, quantity_item)

            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)
            checkbox_item.setCheckState(2 if item.dropable else 0)
            self.model.setItem(row_id, 2, checkbox_item)


class Inventory:
    def __init__(self):
        self.equipment = {}
        self.items = []


class InventoryItem:
    def __init__(self, res_ref, dropable):
        self.res_ref = res_ref
        self.dropable = dropable

    def __str__(self):
        return self.res_ref
