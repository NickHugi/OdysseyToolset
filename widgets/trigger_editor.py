from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox

from installation import Installation
from pykotor.formats.gff import GFF, FieldType
from pykotor.globals import resource_types
from ui import trigger_editor
from widgets.editor_widget import EditorWidget
from widgets.tree_editor import AbstractTreeEditor


class TriggerEditor(AbstractTreeEditor, EditorWidget):
    def __init__(self, parent, utw=GFF(), file_path="", res_ref="untitled"):
        EditorWidget.__init__(self, parent, trigger_editor, "trigger")
        self.load(utw)
        self.setup(file_path, res_ref, resource_types['utt'])
        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_combo_box("Basic", "Faction", Installation.get_faction_list())
        self.init_combo_box("Basic", "Type", ["Generic", "Area Transition", "Trap"])
        self.init_combo_box("Basic", "Cursor", ["None", "Transition", "Use", "Examine", "Talk", "Walk", "XWalk",
                                                "Attack", "Magic", "NoUse", "Trap"])

        self.init_localized_string_nodes("Name")

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Entered")
        self.init_line_edit("Scripts", "Exited")
        self.init_line_edit("Scripts", "Clicked")
        self.init_line_edit("Scripts", "Disarmed")
        self.init_line_edit("Scripts", "Triggered")
        self.init_line_edit("Scripts", "Custom")

        self.init_check_box("Trap", "Is Trap")
        self.init_combo_box("Trap", "Trap Type", Installation.get_trap_type_list())
        self.init_check_box("Trap", "One-Shot")
        self.init_check_box("Trap", "Detectable")
        self.init_check_box("Trap", "Disarmable")
        self.init_spin_box("Trap", "Detection DC")
        self.init_spin_box("Trap", "Disarm DC")

    def load(self, utt):
        self.set_node_data("Basic", "Script Tag", utt.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utt.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Faction", utt.find_field_data("Faction", default=0))
        self.set_node_data("Basic", "Type", utt.find_field_data("Type", default=0))
        self.set_node_data("Basic", "Cursor", utt.find_field_data("Cursor", default=0))

        self.set_localized_string_nodes("Name", utt.find_field_data("LocalizedName"))

        self.set_node_data("Scripts", "Routine", utt.find_field_data("ScriptHeartbeat", default=""))
        self.set_node_data("Scripts", "Entered", utt.find_field_data("ScriptOnEnter", default=""))
        self.set_node_data("Scripts", "Exited", utt.find_field_data("ScriptOnExit", default=""))
        self.set_node_data("Scripts", "Clicked", utt.find_field_data("OnClick", default=""))
        self.set_node_data("Scripts", "Disarmed", utt.find_field_data("OnDisarm", default=""))
        self.set_node_data("Scripts", "Triggered", utt.find_field_data("OnTrapTriggered", default=0))
        self.set_node_data("Scripts", "Custom", utt.find_field_data("ScriptUserDefine", default=""))

        self.set_node_data("Trap", "Is Trap", utt.find_field_data("TrapFlag", default=False))
        self.set_node_data("Trap", "Trap Type", utt.find_field_data("TrapType", default=0))
        self.set_node_data("Trap", "One-Shot", utt.find_field_data("TrapOneShot", default=False))
        self.set_node_data("Trap", "Detectable", utt.find_field_data("TrapDetectable", default=False))
        self.set_node_data("Trap", "Disarmable", utt.find_field_data("TrapDisarmable", default=False))
        self.set_node_data("Trap", "Detection DC", utt.find_field_data("TrapDetectDC", default=0))
        self.set_node_data("Trap", "Disarm DC", utt.find_field_data("DisarmDC", default=0))

    def build(self):
        utt = GFF()

        utt.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        utt.root.add_field(FieldType.ResRef, "TemplateResRef", self.get_node_data("Basic", "Template"))
        utt.root.add_field(FieldType.UInt32, "Faction",  self.get_node_data("Basic", "Faction"))
        utt.root.add_field(FieldType.Int32, "Type",  self.get_node_data("Basic", "Type"))
        utt.root.add_field(FieldType.UInt8, "Cursor",  self.get_node_data("Basic", "Cursor"))
        
        utt.root.add_field(FieldType.ResRef, "ScriptHeartbeat",  self.get_node_data("Scripts", "Routine"))
        utt.root.add_field(FieldType.ResRef, "ScriptOnEnter",  self.get_node_data("Scripts", "Entered"))
        utt.root.add_field(FieldType.ResRef, "ScriptOnExit",  self.get_node_data("Scripts", "Exited"))
        utt.root.add_field(FieldType.ResRef, "OnClick",  self.get_node_data("Scripts", "Clicked"))
        utt.root.add_field(FieldType.ResRef, "OnDisarm",  self.get_node_data("Scripts", "Disarmed"))
        utt.root.add_field(FieldType.ResRef, "OnTrapTriggered",  self.get_node_data("Scripts", "Triggered"))
        utt.root.add_field(FieldType.ResRef, "ScriptUserDefine",  self.get_node_data("Scripts", "Custom"))
        
        utt.root.add_field(FieldType.UInt8, "TrapFlag",  self.get_node_data("Trap", "Is Trap"))
        utt.root.add_field(FieldType.UInt8, "TrapType",  self.get_node_data("Trap", "Trap Type"))
        utt.root.add_field(FieldType.UInt8, "TrapOneShot",  self.get_node_data("Trap", "One-Shot"))
        utt.root.add_field(FieldType.UInt8, "TrapDetectable",  self.get_node_data("Trap", "Detectable"))
        utt.root.add_field(FieldType.UInt8, "TrapDisarmable",  self.get_node_data("Trap", "Disarmable"))
        utt.root.add_field(FieldType.UInt8, "TrapDetectDC",  self.get_node_data("Trap", "Detection DC"))
        utt.root.add_field(FieldType.UInt8, "DisarmDC",  self.get_node_data("Trap", "Disarm DC"))

        return utt

