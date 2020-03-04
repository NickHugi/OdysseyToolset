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

    def init_button(self, item, text):
        button = QPushButton()
        button.setText(text)
        button.setFixedHeight(17)
        self.ui.tree.setItemWidget(item, 1, button)
        return button

    def init_line_edit(self, item):
        line_edit = QLineEdit()
        line_edit.setFixedHeight(23)
        line_edit.setStyleSheet("background: rgb(0,0,0,0%)")
        self.ui.tree.setItemWidget(item, 1, line_edit)
        return line_edit

    def init_spin_box(self, item, min=0, max=999999):
        spin_box = QSpinBox()
        spin_box.setMaximum(max)
        spin_box.setMinimum(min)
        spin_box.setFixedHeight(23)
        spin_box.setStyleSheet("background: rgb(0,0,0,0%); border-width: 0px; border-style: none;")
        self.ui.tree.setItemWidget(item, 1, spin_box)
        return spin_box

    def init_check_box(self, item, checked=False):
        check_box = QCheckBox()
        check_box.setFixedHeight(23)
        check_box.setStyleSheet("QCheckBox::indicator { width: 23; height: 23;}")
        self.ui.tree.setItemWidget(item, 1, check_box)
        return check_box

    def init_combo_box(self, item, items=[]):
        combo_box = QComboBox()
        combo_box.setFixedHeight(23)
        combo_box.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        combo_box.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        combo_box.addItems(items)
        self.ui.tree.setItemWidget(item, 1, combo_box)
        return combo_box
