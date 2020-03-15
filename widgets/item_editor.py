from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton

from pykotor.formats.gff import List, GFF, FieldType, Struct
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from ui import item_editor
from widgets.item_property_dialog import ItemPropertyDialog, ItemProperty
from widgets.model_renderer import ModelRenderer, Object
from widgets.tree_editor import AbstractTreeEditor


class ItemEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = item_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        self.item_properties = []

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
        dialog = ItemPropertyDialog(self, self.item_properties, self.installation)
        dialog.exec_()
        self.item_properties = dialog.get_item_properties()

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

    def load(self, uti):
        self.set_node_data("Basic", "Script Tag", uti.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", uti.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Base", uti.find_field_data("BaseItem", default=0))
        self.set_node_data("Basic", "Cost", uti.find_field_data("Cost", default=0))
        self.set_node_data("Basic", "Additional Cost", uti.find_field_data("AddCost", default=0))
        self.set_node_data("Basic", "Plot Item", uti.find_field_data("Plot", default=False))

        self.set_node_data("Advanced", "Upgrade Level", uti.find_field_data("", default=0))
        self.set_node_data("Advanced", "Charges", uti.find_field_data("Charges", default=0))
        self.set_node_data("Advanced", "Stack Size", uti.find_field_data("StackSize", default=0))
        self.set_node_data("Advanced", "Model Variation", uti.find_field_data("ModelVariation", default=0))
        self.set_node_data("Advanced", "Body Variation", uti.find_field_data("BodyVariation", default=0))
        self.set_node_data("Advanced", "Texture Variation", uti.find_field_data("TextureVar", default=0))

        self.set_localized_string_nodes("Name", uti.find_field_data("LocalizedName"))
        self.set_localized_string_nodes("Description", uti.find_field_data("DescIdentified"))

        for i in range(len(uti.find_field_data("PropertiesList", default=List([])).structs)):
            item_property = ItemProperty()
            item_property.type_value = uti.find_field_data("PropertiesList", i, "PropertyName", default=-1)
            item_property.subtype_value = uti.find_field_data("PropertiesList", i, "Subtype", default=-1)
            item_property.upgrade_value = uti.find_field_data("PropertiesList", i, "UpgradeType", default=-1)
            item_property.cost_value = uti.find_field_data("PropertiesList", i, "CostValue", default=-1)
            item_property.cost_table = uti.find_field_data("PropertiesList", i, "CostTable", default=-1)
            item_property.param1_value = uti.find_field_data("PropertiesList", i, "Param1Value", default=-1)
            item_property.param1_table = uti.find_field_data("PropertiesList", i, "Param1", default=-1)
            item_property.param2_value = uti.find_field_data("PropertiesList", i, "Param2Value", default=-1)
            item_property.param2_table = uti.find_field_data("PropertiesList", i, "Param2", default=-1)
            self.item_properties.append(item_property)

    def build(self):
        uti = GFF()

        uti.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        uti.root.add_field(FieldType.ResRef, "TemplateResRef", self.get_node_data("Basic", "Template"))
        uti.root.add_field(FieldType.Int32, "BaseItem", self.get_node_data("Basic", "Base"))
        uti.root.add_field(FieldType.UInt32, "Cost", self.get_node_data("Basic", "Cost"))
        uti.root.add_field(FieldType.UInt32, "AddCost", self.get_node_data("Basic", "Additional Cost"))
        uti.root.add_field(FieldType.UInt8, "Plot", self.get_node_data("Basic", "Plot Item"))

        uti.root.add_field(FieldType.LocalizedString, "LocalizedName", self.get_node_localized_string("Name"))
        uti.root.add_field(FieldType.LocalizedString, "DescIdentified", self.get_node_localized_string("Description"))

        uti.root.add_field(FieldType.UInt8, "UpgradeLevel", self.get_node_data("Advanced", "Upgrade Level"))
        uti.root.add_field(FieldType.UInt8, "Charges", self.get_node_data("Advanced", "Charges"))
        uti.root.add_field(FieldType.UInt16, "StackSize", self.get_node_data("Advanced", "Stack Size"))
        uti.root.add_field(FieldType.UInt8, "ModelVariation", self.get_node_data("Advanced", "Model Variation"))
        uti.root.add_field(FieldType.UInt8, "BodyVariation", self.get_node_data("Advanced", "Body Variation"))
        uti.root.add_field(FieldType.UInt8, "TextureVar", self.get_node_data("Advanced", "Texture Variation"))

        uti_property_list = List([])
        for property in self.item_properties:
            uti_property_struct = Struct(0, [])
            uti_property_struct.add_field(FieldType.UInt8, "ChanceAppear", 100)
            uti_property_struct.add_field(FieldType.UInt16, "PropertyName", property.type_value)
            uti_property_struct.add_field(FieldType.UInt16, "Subtype", property.subtype_value)
            uti_property_struct.add_field(FieldType.UInt8, "UpgradeType", property.upgrade_value)

            uti_property_struct.add_field(FieldType.UInt8, "CostTable", property.cost_table)
            uti_property_struct.add_field(FieldType.UInt16, "CostValue", property.cost_value)

            uti_property_struct.add_field(FieldType.UInt8, "Param1", property.param1_table)
            if property.param1_table == -1:
                uti_property_struct.add_field(FieldType.UInt8, "Param1Value", 0)
            else:
                uti_property_struct.add_field(FieldType.UInt8, "Param1Value", property.param1_value)

            if property.param2_table != -1:
                uti_property_struct.add_field(FieldType.UInt8, "Param2", property.param2_table)
                uti_property_struct.add_field(FieldType.UInt8, "Param2Value", property.param2_value)
            uti_property_list.structs.append(uti_property_struct)
        uti.root.add_field(FieldType.List, "PropertiesList", uti_property_list)

        return uti

