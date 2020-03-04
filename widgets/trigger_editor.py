from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox

from installation import Installation
from ui import trigger_editor
from widgets.tree_editor import AbstractTreeEditor


class TriggerEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = trigger_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        search_flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive

        self.script_tag_item = self.ui.tree.findItems("Script Tag", search_flags)[0]
        self.template_item = self.ui.tree.findItems("Template", search_flags)[0]
        self.faction_item = self.ui.tree.findItems("Faction", search_flags)[0]
        self.type_item = self.ui.tree.findItems("Type", search_flags)[0]

        self.tlk_reference_item = self.ui.tree.findItems("TLK Reference", search_flags)[0]
        self.tlk_text_item = self.ui.tree.findItems("TLK Text", search_flags)[0]
        self.english_item = self.ui.tree.findItems("English", search_flags)[0]
        self.french_item = self.ui.tree.findItems("French", search_flags)[0]
        self.german_item = self.ui.tree.findItems("German", search_flags)[0]
        self.italian_item = self.ui.tree.findItems("Italian", search_flags)[0]
        self.spanish_item = self.ui.tree.findItems("Spanish", search_flags)[0]
        self.polish_item = self.ui.tree.findItems("Polish", search_flags)[0]
        self.korean_item = self.ui.tree.findItems("Korean", search_flags)[0]

        self.routine_item = self.ui.tree.findItems("Routine", search_flags)[0]
        self.entered_item = self.ui.tree.findItems("Entered", search_flags)[0]
        self.clicked_item = self.ui.tree.findItems("Clicked", search_flags)[0]
        self.disarmed_item = self.ui.tree.findItems("Disarmed", search_flags)[0]
        self.triggered_item = self.ui.tree.findItems("Triggered", search_flags)[0]
        self.exited_item = self.ui.tree.findItems("Exited", search_flags)[0]
        self.custom_item = self.ui.tree.findItems("Custom", search_flags)[0]

        self.is_trap_item = self.ui.tree.findItems("Is Trap", search_flags)[0]
        self.trap_type_item = self.ui.tree.findItems("Trap Type", search_flags)[0]
        self.one_shot_type = self.ui.tree.findItems("One-Shot", search_flags)[0]
        self.findable_type = self.ui.tree.findItems("Findable", search_flags)[0]
        self.disarmable_type = self.ui.tree.findItems("Disarmable", search_flags)[0]
        self.disarm_dc_type = self.ui.tree.findItems("Detection DC", search_flags)[0]
        self.detection_dc_type = self.ui.tree.findItems("Disarm DC", search_flags)[0]

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_combo_box("Basic", "Faction", ["Friendly 1", "Hostile 2", "Friendly 2", "Neutral", "Insane", "Tuskan",
                                                "GLB XOR", "Surrender 1", "Surrender 2", "Predator", "Prey", "Trap",
                                                "Endar Spire", "Rancor", "Gizka 1", "Gizka 2", "Czerka",
                                                "Zone Controller", "Sacrifice", "One On One", "Party Puppet"])
        self.init_combo_box("Basic", "Type", ["Generic", "Area Transition", "Trap"])
        self.init_combo_box("Basic", "Cursor", ["None", "Transition", "Use", "Examine", "Talk", "Walk", "XWalk",
                                                "Attack", "Magic", "NoUse", "Trap"])

        self.init_localized_string_nodes("Name")

        self.init_line_edit("Scripting", "Routine")
        self.init_line_edit("Scripting", "Entered")
        self.init_line_edit("Scripting", "Exit")
        self.init_line_edit("Scripting", "Clicked")
        self.init_line_edit("Scripting", "Disarmed")
        self.init_line_edit("Scripting", "Triggered")
        self.init_line_edit("Scripting", "Custom")

        self.init_check_box("Trap", "Is Trap")
        self.init_combo_box("Trap", "Trap Type", Installation.get_trap_type_list())
        self.init_check_box("Trap", "One-Shot")
        self.init_check_box("Trap", "Findable")
        self.init_check_box("Trap", "Disarmable")
        self.init_spin_box("Trap", "Detection DC")
        self.init_spin_box("Trap", "Disarm DC")
