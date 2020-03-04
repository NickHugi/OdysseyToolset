from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton
from pykotor.globals import Gender, Language

from pykotor.formats.gff import GFF
from ui import waypoint_editor
from widgets.tree_editor import AbstractTreeEditor


class WaypointEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = waypoint_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        search_flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
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
        self.set_note_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_note_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_note_data("Basic", "Map Note", utw.find_field_data("HasMapNote", default=False))
        self.set_note_data("Basic", "Note Active", utw.find_field_data("MapNoteEnabled", default=False))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocalizedName"))
        self.set_localized_string_nodes("Name", utw.find_field_data("LocalizedName"))

