from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QFontInfo, QFontMetrics
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider, QTreeWidgetItem, \
    QPlainTextEdit, QFrame, QSizePolicy, QLabel
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from ui import placeable_editor
from widgets.model_renderer import ModelRenderer, Object
from widgets.tree_editor import AbstractTreeEditor


class PlaceableEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = placeable_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        inventory_button = QPushButton("Inventory")
        inventory_button.setFixedHeight(17)
        inventory_button.clicked.connect(self.open_inventory_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Inventory", QtCore.Qt.MatchExactly)[0], 1, inventory_button)

        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Dialog")
        self.init_combo_box("Basic", "Body Bag", items=Installation.get_bodybag_list())

        self.init_spin_box("Name", "TLK Reference")
        self.get_node_widget("Name", "TLK Reference").valueChanged.connect(self.tlk_name_changed)
        self.init_line_edit("Name", "TLK Text")
        self.get_node_widget("Name", "TLK Text").setReadOnly(True)
        self.init_line_edit("Name", "English")
        self.init_line_edit("Name", "French")
        self.init_line_edit("Name", "German")
        self.init_line_edit("Name", "Italian")
        self.init_line_edit("Name", "Spanish")
        self.init_line_edit("Name", "Polish")
        self.init_line_edit("Name", "Korean")

        self.init_combo_box("Advanced", "State", items=["Default", "Opened", "Closed", "Dead", "Activated", "Deactivated"])
        self.init_combo_box("Advanced", "Faction", items=Installation.get_faction_list())

        self.init_spin_box("Other", "Fortitude")
        self.init_spin_box("Other", "Reflex")
        self.init_spin_box("Other", "Will")
        self.init_spin_box("Other", "Health")
        self.init_spin_box("Other", "Hardness")

        self.init_check_box("Flags", "Plot")
        self.init_check_box("Flags", "Interactable")
        self.init_check_box("Flags", "Interruptable")
        self.init_check_box("Flags", "Invincible")
        self.init_check_box("Flags", "Static")
        self.init_check_box("Flags", "Party Useable")
        self.init_check_box("Flags", "Has Inventory")

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Used")
        self.init_line_edit("Scripts", "Opened")
        self.init_line_edit("Scripts", "Closed")
        self.init_line_edit("Scripts", "UnLocked")
        self.init_line_edit("Scripts", "Locked")
        self.init_line_edit("Scripts", "After Talking")
        self.init_line_edit("Scripts", "Inventory Accessed")
        self.init_line_edit("Scripts", "Attacked Physically")
        self.init_line_edit("Scripts", "Attacked Ability")
        self.init_line_edit("Scripts", "Damaged")
        self.init_line_edit("Scripts", "Death")
        self.init_line_edit("Scripts", "Disarmed")
        self.init_line_edit("Scripts", "Triggered")
        self.init_line_edit("Scripts", "Custom")

        self.init_check_box("Trap", "Is Trap")
        self.init_check_box("Trap", "One-Shot")
        self.init_check_box("Trap", "Findable")
        self.init_check_box("Trap", "Disarmable")
        self.init_spin_box("Trap", "Detection DC")
        self.init_spin_box("Trap", "Disarm DC")
        self.init_combo_box("Trap", "Trap Type", items=Installation.get_trap_type_list())

        self.init_check_box("Lock", "Is Locked")
        self.init_check_box("Lock", "Lockable")
        self.init_check_box("Lock", "Requires Key")
        self.init_check_box("Lock", "Remove Key")
        self.init_line_edit("Lock", "Key Tag")
        self.init_spin_box("Lock", "Unlock DC")
        self.init_spin_box("Lock", "Lock DC")

        if self.installation is None:
            self.get_node("Name", "TLK Text").parent().removeChild(self.get_node("Name", "TLK Text"))
            self.init_spin_box("Basic", "Appearance")
        else:
            self.init_combo_box("Basic", "Appearance", items=Installation.get_placeable_list(self.installation))
            self.get_node_widget("Basic", "Appearance").currentIndexChanged.connect(self.appearance_changed)

    def open_inventory_dialog(self):
        # TODO
        print("open inventory dialog")

    def tlk_name_changed(self, index):
        if self.installation is not None:
            self.get_node_widget("Name", "TLK Text").setText("")
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.get_node_widget("Name", "TLK Text").setText(text)

    def appearance_changed(self, index):
        try:
            genericdoors_data = TwoDA.from_data(self.installation.chitin.fetch_resource("placeables", "2da"))
            model_name = genericdoors_data.get_cell("modelname", index).lower()
            mdl_data = self.installation.chitin.fetch_resource(model_name, "mdl")
            mdx_data = self.installation.chitin.fetch_resource(model_name, "mdx")
            model = MDL.from_data(mdl_data, mdx_data)
            self.model_renderer.model_buffer[model_name] = model
            self.model_renderer.objects.clear()
            self.model_renderer.objects.append(Object(model_name))
        except Exception as e:
            print("Failed to load door appearance model:", e)

