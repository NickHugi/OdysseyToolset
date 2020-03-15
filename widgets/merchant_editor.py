from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton

from pykotor.formats.gff import GFF, FieldType, List, Struct
from ui import merchant_editor
from widgets.inventory_dialog import InventoryDialog, Inventory, InventoryItem
from widgets.tree_editor import AbstractTreeEditor


class MerchantEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = merchant_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        self.inventory = Inventory()

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        creatures_button = QPushButton("...")
        creatures_button.setFixedHeight(17)
        creatures_button.clicked.connect(self.open_inventory_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Inventory", QtCore.Qt.MatchExactly)[0], 1, creatures_button)

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script")
        self.init_combo_box("Basic", "Type", items=["Buy Only", "Sell Only", "Buy and Sell"])
        self.init_spin_box("Basic", "Mark Up")
        self.init_spin_box("Basic", "Mark Down")

        self.init_localized_string_nodes("Name", False)

    def open_inventory_dialog(self):
        dialog = InventoryDialog(self, self.inventory, "placeable", self.installation)
        dialog.exec_()
        self.inventory = dialog.get_inventory()

    def load(self, utm):
        self.set_node_data("Basic", "Script Tag", utm.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utm.find_field_data("ResRef", default=""))
        self.set_node_data("Basic", "Script", utm.find_field_data("OnOpenStore", default=""))
        self.set_node_data("Basic", "Type", utm.find_field_data("BuySellFlag", default=0) - 1)
        self.set_node_data("Basic", "Mark Up", utm.find_field_data("MarkUp", default=0))
        self.set_node_data("Basic", "Mark Down", utm.find_field_data("MarkDown", default=0))

        self.set_localized_string_nodes("Name", utm.find_field_data("LocName"))

        for i in range(len(utm.find_field_data("ItemList", default=List([])).structs)):
            item_resref = utm.find_field_data("ItemList", i, "InventoryRes", default="")
            item_dropable = utm.find_field_data("ItemList", i, "Dropable", default="")
            if item_resref != "": self.inventory.items.append(InventoryItem(item_resref, item_dropable))
    
    def build(self):
        utm = GFF()

        utm.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        utm.root.add_field(FieldType.ResRef, "ResRef", self.get_node_data("Basic", "Template"))
        utm.root.add_field(FieldType.ResRef, "Script", self.get_node_data("OnOpenStore", "Script"))
        utm.root.add_field(FieldType.UInt8, "Type", self.get_node_data("BuySellFlag", "Script"))
        utm.root.add_field(FieldType.UInt8, "Mark Up", self.get_node_data("MarkUp", "Script"))
        utm.root.add_field(FieldType.UInt8, "Mark Down", self.get_node_data("MarkDown", "Script"))

        utm.root.add_field(FieldType.LocalizedString, "LocName", self.get_node_localized_string("Name"))

        utc_item_list = List([])
        for slot, item in enumerate(self.inventory.items):
            item_struct = Struct(slot, [])
            item_struct.add_field(FieldType.ResRef, "InventoryRes", item.res_ref)
            item_struct.add_field(FieldType.UInt16, "Repos_PosX", slot)
            item_struct.add_field(FieldType.UInt16, "Repos_PosY", 0)
            if item.dropable: item_struct.add_field(FieldType.UInt8, "Dropable", 1)
            utc_item_list.structs.append(item_struct)
        utm.root.add_field(FieldType.List, "ItemList", utc_item_list)

        return utm
    