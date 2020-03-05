from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from ui import item_editor
from widgets.model_renderer import ModelRenderer, Object
from widgets.tree_editor import AbstractTreeEditor


class ItemEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = item_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        properties_button = QPushButton("...")
        properties_button.setFixedHeight(17)
        properties_button.clicked.connect(self.open_properties_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Properties", QtCore.Qt.MatchExactly)[0], 1, properties_button)

        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script Tag")
        self.init_spin_box("Basic", "Cost")
        self.init_spin_box("Basic", "Additional Cost")
        self.init_check_box("Basic", "Plot Item")

        self.init_localized_string_nodes("Name")
        self.init_localized_string_nodes("Description", multiline=True)

        self.init_spin_box("Advanced", "Upgrade Level")
        self.init_spin_box("Advanced", "Charges")
        self.init_spin_box("Advanced", "Stack Size")
        self.init_spin_box("Advanced", "Model Variation")
        self.init_spin_box("Advanced", "Body Variation")
        self.init_spin_box("Advanced", "Texture Variation")

        if self.installation is None:
            self.init_spin_box("Basic", "Base")
        else:
            self.init_combo_box("Basic", "Base", items=Installation.get_base_item_list(self.installation))
            self.get_node_widget("Basic", "Base").currentIndexChanged.connect(self.base_item_changed)

    def open_properties_dialog(self):
        # TODO
        print("open properties dialog")

    def base_item_changed(self, index):
        try:
            baseitems_data = TwoDA.from_data(self.installation.chitin.fetch_resource("baseitems", "2da"))
            model_name = baseitems_data.get_cell("defaultmodel", index).lower()
            mdl_data = self.installation.chitin.fetch_resource(model_name, "mdl")
            mdx_data = self.installation.chitin.fetch_resource(model_name, "mdx")
            model = MDL.from_data(mdl_data, mdx_data)
            self.model_renderer.model_buffer[model_name] = model
            self.model_renderer.objects.clear()
            self.model_renderer.objects.append(Object(model_name))
        except Exception as e:
            print("Failed to load door appearance model:", e)

    def load(self, utw):
        self.set_note_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_note_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_note_data("Basic", "Base", utw.find_field_data("BaseItem", default=0))
        self.set_note_data("Basic", "Cost", utw.find_field_data("Cost", default=0))
        self.set_note_data("Basic", "Additional Cost", utw.find_field_data("AddCost", default=0))
        self.set_note_data("Basic", "Plot Item", utw.find_field_data("Plot", default=False))

        self.set_note_data("Advanced", "Upgrade Level", utw.find_field_data("", default=0))
        self.set_note_data("Advanced", "Charges", utw.find_field_data("Charges", default=0))
        self.set_note_data("Advanced", "Stack Size", utw.find_field_data("StackSize", default=0))
        self.set_note_data("Advanced", "Model Variation", utw.find_field_data("ModelVariation", default=0))
        self.set_note_data("Advanced", "Body Variation", utw.find_field_data("BodyVariation", default=0))
        self.set_note_data("Advanced", "Texture Variation", utw.find_field_data("TextureVar", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocalizedName"))
        self.set_localized_string_nodes("Description", utw.find_field_data("Description"))

