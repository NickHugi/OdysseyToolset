from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QPushButton, QPlainTextEdit, QTreeWidget, QLineEdit, QSpinBox, \
    QCheckBox, QComboBox

from installation import Installation
from pykotor.formats.gff import List, GFF, FieldType, Struct
from pykotor.globals import resource_types
from ui import encounter_editor
from widgets.creatures_dialog import CreaturesDialog, EncounteredCreature
from widgets.editor_widget import EditorWidget
from widgets.tree_editor import AbstractTreeEditor


class EncounterEditor(AbstractTreeEditor, EditorWidget):
    def __init__(self, parent, utw=GFF(), file_path="", res_ref="untitled"):
        self.creatures = []

        EditorWidget.__init__(self, parent, encounter_editor, "encounter")
        self.load(utw)
        self.setup(file_path, res_ref, resource_types['ute'])
        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        creatures_button = QPushButton("...")
        creatures_button.setFixedHeight(17)
        creatures_button.clicked.connect(self.open_creatures_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Creatures", QtCore.Qt.MatchExactly)[0], 1, creatures_button)

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_combo_box("Basic", "Faction", Installation.get_faction_list())
        self.init_combo_box("Basic", "Difficulty", ["Very Easy", "Easy", "Normal", "Hard", "Impossible"])
        self.init_spin_box("Basic", "Min Creatures")
        self.init_spin_box("Basic", "Max Creatures")
        self.init_spin_box("Basic", "Interval")
        self.init_spin_box("Basic", "Waves")

        self.init_check_box("Flags", "Active")
        self.init_check_box("Flags", "Player-Activated")
        self.init_check_box("Flags", "Will Reset")
        self.init_check_box("Flags", "One-Time")

        self.init_localized_string_nodes("Name")

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Entered")
        self.init_line_edit("Scripts", "Exited")
        self.init_line_edit("Scripts", "All Dead")
        self.init_line_edit("Scripts", "Custom")

    def open_creatures_dialog(self):
        dialog = CreaturesDialog(self, self.creatures, self.installation)
        dialog.exec_()
        self.creatures = dialog.get_creatures()

    def load(self, ute):
        self.set_node_data("Basic", "Script Tag", ute.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", ute.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Faction", ute.find_field_data("Faction", default=0))
        self.set_node_data("Basic", "Difficulty", ute.find_field_data("DifficultyIndex", default=0))
        self.set_node_data("Basic", "Min Creatures", ute.find_field_data("RecCreatures", default=0))
        self.set_node_data("Basic", "Max Creatures", ute.find_field_data("MaxCreatures", default=0))
        self.set_node_data("Basic", "Interval", ute.find_field_data("ResetTime", default=0))
        self.set_node_data("Basic", "Waves", ute.find_field_data("Respawns", default=0))

        self.set_node_data("Flags", "Active", ute.find_field_data("Active", default=False))
        self.set_node_data("Flags", "Player-Activated", ute.find_field_data("PlayerOnly", default=False))
        self.set_node_data("Flags", "Will Reset", ute.find_field_data("Reset", default=False))
        self.set_node_data("Flags", "One-Time", ute.find_field_data("SpawnOption", default=False))

        self.set_localized_string_nodes("Name", ute.find_field_data("LocalizedName"))

        self.set_node_data("Scripts", "Routine", ute.find_field_data("ScriptHeartbeat", default=""))
        self.set_node_data("Scripts", "Entered", ute.find_field_data("ScriptOnEnter", default=""))
        self.set_node_data("Scripts", "Exited", ute.find_field_data("ScriptOnExit", default=""))
        self.set_node_data("Scripts", "All Dead", ute.find_field_data("OnExhausted", default=""))
        self.set_node_data("Scripts", "Custom", ute.find_field_data("ScriptUserDefine", default=""))

        for i in range(len(ute.find_field_data("CreatureList", default=List([])).structs)):
            creature = EncounteredCreature()
            creature.appearance = ute.find_field_data("CreatureList", i, "Appearance", default=0)
            creature.challenge_rating = ute.find_field_data("CreatureList", i, "CR", default=1)
            creature.guaranteed_count = ute.find_field_data("CreatureList", i, "GuaranteedCount", default=0)
            creature.res_ref = ute.find_field_data("CreatureList", i, "ResRef", default="")
            creature.single_spawn = bool(ute.find_field_data("CreatureList", i, "SingleSpawn", default=0))
            self.creatures.append(creature)

    def build(self):
        ute = GFF()

        ute.root.add_field(FieldType.String, "Tag",             self.get_node_data("Basic", "Script Tag"))
        ute.root.add_field(FieldType.ResRef, "TemplateResRef",  self.get_node_data("Basic", "Template"))
        ute.root.add_field(FieldType.UInt32, "Faction",  self.get_node_data("Basic", "Faction"))
        ute.root.add_field(FieldType.Int32, "DifficultyIndex",  self.get_node_data("Basic", "Difficulty"))
        ute.root.add_field(FieldType.Int32, "RecCreatures",  self.get_node_data("Basic", "Min Creatures"))
        ute.root.add_field(FieldType.Int32, "MaxCreatures",  self.get_node_data("Basic", "Max Creatures"))
        ute.root.add_field(FieldType.Int32, "ResetTime",  self.get_node_data("Basic", "Interval"))
        ute.root.add_field(FieldType.Int32, "Respawns",  self.get_node_data("Basic", "Waves"))

        ute.root.add_field(FieldType.LocalizedString, "LocalizedName", self.get_node_localized_string("Name"))

        ute.root.add_field(FieldType.UInt8, "Active",  self.get_node_data("Flags", "Active"))
        ute.root.add_field(FieldType.UInt8, "PlayerOnly",  self.get_node_data("Flags", "Player-Activated"))
        ute.root.add_field(FieldType.UInt8, "Reset",  self.get_node_data("Flags", "Will Reset"))
        ute.root.add_field(FieldType.UInt8, "SpawnOption",  self.get_node_data("Flags", "One-Time"))

        ute.root.add_field(FieldType.ResRef, "OnHeartbeat", self.get_node_data("Scripts", "Routine"))
        ute.root.add_field(FieldType.ResRef, "OnEntered", self.get_node_data("Scripts", "Entered"))
        ute.root.add_field(FieldType.ResRef, "OnExit", self.get_node_data("Scripts", "Exited"))
        ute.root.add_field(FieldType.ResRef, "OnExhausted", self.get_node_data("Scripts", "All Dead"))
        ute.root.add_field(FieldType.ResRef, "OnUserDefined", self.get_node_data("Scripts", "Custom"))

        ute_creature_list = List([])
        for creature in self.creatures:
            ute_creature_struct = Struct(0, [])
            ute_creature_struct.add_field(FieldType.Int32, "Appearance", creature.appearance)
            ute_creature_struct.add_field(FieldType.Float, "CR", creature.challenge_rating)
            ute_creature_struct.add_field(FieldType.Int32, "GuaranteedCount", creature.guaranteed_count)
            ute_creature_struct.add_field(FieldType.ResRef, "ResRef", creature.res_ref)
            ute_creature_struct.add_field(FieldType.UInt8, "SingleSpawn", creature.single_spawn)
            ute_creature_list.structs.append(ute_creature_struct)
        ute.root.add_field(FieldType.List, "CreatureList", ute_creature_list)

        return ute
