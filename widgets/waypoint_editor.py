from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton, QFileDialog
from pykotor.globals import Gender, Language, resource_types

from pykotor.formats.gff import GFF, FieldType
from ui import waypoint_editor
from widgets.editor_widget import EditorWidget
from widgets.tree_editor import AbstractTreeEditor


class WaypointEditor(AbstractTreeEditor, EditorWidget):
    def __init__(self, parent, utw=GFF(), file_path="", res_ref="untitled"):
        EditorWidget.__init__(self, parent, waypoint_editor, "waypoint")
        self.load(utw)
        self.setup(file_path, res_ref, resource_types['utw'])
        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_check_box("Basic", "Map Note")
        self.init_check_box("Basic", "Note Active")

        self.init_localized_string_nodes("Name", False)
        self.init_localized_string_nodes("Map Note", False)
        self.init_localized_string_nodes("Description", True)

    def load(self, utw):
        self.set_node_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Map Note", utw.find_field_data("HasMapNote", default=False))
        self.set_node_data("Basic", "Note Active", utw.find_field_data("MapNoteEnabled", default=False))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocalizedName"))
        self.set_localized_string_nodes("Map Note", utw.find_field_data("MapNote"))
        self.set_localized_string_nodes("Description", utw.find_field_data("Description"))

    def build(self):
        utw = GFF()
        utw.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        utw.root.add_field(FieldType.ResRef, "TemplateResRef", self.get_node_data("Basic", "Template"))
        utw.root.add_field(FieldType.Int8, "HasMapNote", self.get_node_data("Basic", "Map Note"))
        utw.root.add_field(FieldType.Int8, "MapNoteEnabled", self.get_node_data("Basic", "Note Active"))
        utw.root.add_field(FieldType.LocalizedString, "LocalizedName", self.get_node_localized_string("Name"))
        utw.root.add_field(FieldType.LocalizedString, "Description", self.get_node_localized_string("Description"))
        utw.root.add_field(FieldType.LocalizedString, "MapNote", self.get_node_localized_string("Map Note"))
        return utw
