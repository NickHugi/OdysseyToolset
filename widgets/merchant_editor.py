from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton

from ui import merchant_editor
from widgets.tree_editor import AbstractTreeEditor


class MerchantEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = merchant_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

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
        # TODO
        pass

    def load(self, utw):
        self.set_node_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utw.find_field_data("ResRef", default=""))
        self.set_node_data("Basic", "Script", utw.find_field_data("OnOpenStore", default=""))
        self.set_node_data("Basic", "Type", utw.find_field_data("BuySellFlag", default=0) - 1)
        self.set_node_data("Basic", "Mark Up", utw.find_field_data("MarkUp", default=0))
        self.set_node_data("Basic", "Mark Down", utw.find_field_data("MarkDown", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocName"))
