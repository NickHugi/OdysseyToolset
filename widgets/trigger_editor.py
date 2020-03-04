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
        self.init_line_edit("Scripting", "Exited")
        self.init_line_edit("Scripting", "Clicked")
        self.init_line_edit("Scripting", "Disarmed")
        self.init_line_edit("Scripting", "Triggered")
        self.init_line_edit("Scripting", "Custom")

        self.init_check_box("Trap", "Is Trap")
        self.init_combo_box("Trap", "Trap Type", Installation.get_trap_type_list())
        self.init_check_box("Trap", "One-Shot")
        self.init_check_box("Trap", "Detectable")
        self.init_check_box("Trap", "Disarmable")
        self.init_spin_box("Trap", "Detection DC")
        self.init_spin_box("Trap", "Disarm DC")

    def load(self, utw):
        self.set_note_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_note_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_note_data("Basic", "Faction", utw.find_field_data("Faction", default=0))
        self.set_note_data("Basic", "Type", utw.find_field_data("Type", default=0))
        self.set_note_data("Basic", "Cursor", utw.find_field_data("Cursor", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocalizedName"))

        self.set_note_data("Scripting", "Routine", utw.find_field_data("ScriptHeartbeat", default=""))
        self.set_note_data("Scripting", "Entered", utw.find_field_data("ScriptOnEnter", default=""))
        self.set_note_data("Scripting", "Exited", utw.find_field_data("ScriptOnExit", default=""))
        self.set_note_data("Scripting", "Clicked", utw.find_field_data("OnClick", default=""))
        self.set_note_data("Scripting", "Disarmed", utw.find_field_data("OnDisarm", default=""))
        self.set_note_data("Scripting", "Triggered", utw.find_field_data("OnTrapTriggered", default=0))
        self.set_note_data("Scripting", "Custom", utw.find_field_data("ScriptUserDefine", default=""))

        self.set_note_data("Trap", "Is Trap", utw.find_field_data("TrapFlag", default=False))
        self.set_note_data("Trap", "Trap Type", utw.find_field_data("TrapType", default=0))
        self.set_note_data("Trap", "One-Shot", utw.find_field_data("TrapOneShot", default=False))
        self.set_note_data("Trap", "Detectable", utw.find_field_data("TrapDetectable", default=False))
        self.set_note_data("Trap", "Disarmable", utw.find_field_data("TrapDisarmable", default=False))
        self.set_note_data("Trap", "Detection DC", utw.find_field_data("TrapDetectDC", default=0))
        self.set_note_data("Trap", "Disarm DC", utw.find_field_data("DisarmDC", default=0))



