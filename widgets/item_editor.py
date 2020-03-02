from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton

from installation import Installation
from ui import item_editor
from widgets.model_renderer import ModelRenderer
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

        properties_button = QPushButton("Properties")
        properties_button.setFixedHeight(17)
        properties_button.clicked.connect(self.open_properties_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Properties", QtCore.Qt.MatchExactly)[0], 1, properties_button)

        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script Tag")
        self.init_spin_box("Basic", "Cost")
        self.init_spin_box("Basic", "Additional Cost")
        self.init_check_box("Basic", "Plot Item")

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

        self.init_spin_box("Description", "TLK Reference")
        self.get_node_widget("Description", "TLK Reference").valueChanged.connect(self.tlk_description_changed)
        self.init_multiline_edit("Description", "TLK Text")
        self.get_node_widget("Description", "TLK Text").setReadOnly(True)
        self.init_multiline_edit("Description", "English")
        self.init_multiline_edit("Description", "French")
        self.init_multiline_edit("Description", "German")
        self.init_multiline_edit("Description", "Italian")
        self.init_multiline_edit("Description", "Spanish")
        self.init_multiline_edit("Description", "Polish")
        self.init_multiline_edit("Description", "Korean")

        self.init_spin_box("Advanced", "Palette ID")
        self.init_spin_box("Advanced", "Upgrade Level")
        self.init_spin_box("Advanced", "Charges")
        self.init_spin_box("Advanced", "Stack Size")
        self.init_spin_box("Advanced", "Model Variation")
        self.init_spin_box("Advanced", "Body Variation")
        self.init_spin_box("Advanced", "Texture Variation")

        if self.installation is None:
            self.get_node("Name", "TLK Text").parent().removeChild(self.get_node("Name", "TLK Text"))
            self.get_node("Description", "TLK Text").parent().removeChild(self.get_node("Description", "TLK Text"))
            self.init_spin_box("Basic", "Base")
        else:
            self.init_combo_box("Basic", "Base", items=Installation.get_base_item_list(self.installation))
            self.get_node_widget("Basic", "Base").currentIndexChanged.connect(self.base_item_changed)

    def open_properties_dialog(self):
        # TODO
        print("open properties dialog")

    def tlk_name_changed(self, index):
        if self.installation is not None:
            self.get_node_widget("Name", "TLK Text").setText("")
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.get_node_widget("Name", "TLK Text").setText(text)

    def tlk_description_changed(self, index):
        if self.installation is not None:
            self.get_node_widget("Description", "TLK Text").setPlainText("")
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.get_node_widget("Description", "TLK Text").setPlainText(text)

    def base_item_changed(self, index):
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

