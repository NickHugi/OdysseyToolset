from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton

from ui import waypoint_editor


class WaypointEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = waypoint_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        search_flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive

        self.script_tag_item = self.ui.tree.findItems("Script Tag", search_flags)[0]
        self.template_item = self.ui.tree.findItems("Template", search_flags)[0]
        self.map_note_item = self.ui.tree.findItems("Map Note", search_flags)[0]
        self.note_active_item = self.ui.tree.findItems("Note Active", search_flags)[0]

        self.tlk_name_reference_item = self.ui.tree.findItems("TLK Reference", search_flags)[0]
        self.tlk_name_text_item = self.ui.tree.findItems("TLK Text", search_flags)[0]
        self.name_english_item = self.ui.tree.findItems("English", search_flags)[0]
        self.name_french_item = self.ui.tree.findItems("French", search_flags)[0]
        self.name_german_item = self.ui.tree.findItems("German", search_flags)[0]
        self.name_italian_item = self.ui.tree.findItems("Italian", search_flags)[0]
        self.name_spanish_item = self.ui.tree.findItems("Spanish", search_flags)[0]
        self.name_polish_item = self.ui.tree.findItems("Polish", search_flags)[0]
        self.name_korean_item = self.ui.tree.findItems("Korean", search_flags)[0]

        self.tlk_note_reference_item = self.ui.tree.findItems("TLK Reference", search_flags)[1]
        self.tlk_note_text_item = self.ui.tree.findItems("TLK Text", search_flags)[1]
        self.note_english_item = self.ui.tree.findItems("English", search_flags)[1]
        self.note_french_item = self.ui.tree.findItems("French", search_flags)[1]
        self.note_german_item = self.ui.tree.findItems("German", search_flags)[1]
        self.note_italian_item = self.ui.tree.findItems("Italian", search_flags)[1]
        self.note_spanish_item = self.ui.tree.findItems("Spanish", search_flags)[1]
        self.note_polish_item = self.ui.tree.findItems("Polish", search_flags)[1]
        self.note_korean_item = self.ui.tree.findItems("Korean", search_flags)[1]

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_line_edit(self.script_tag_item)
        self.init_line_edit(self.template_item)
        self.init_check_box(self.map_note_item)
        self.init_check_box(self.note_active_item)

        self.init_spin_box(self.tlk_name_reference_item)
        self.init_line_edit(self.tlk_name_text_item)
        self.ui.tree.itemWidget(self.tlk_name_text_item, 1).setReadOnly(True)
        self.tlk_name_text_item.setDisabled(True)
        self.ui.tree.itemWidget(self.tlk_name_reference_item, 1).valueChanged.connect(self.tlk_name_changed)
        self.init_line_edit(self.name_english_item)
        self.init_line_edit(self.name_french_item)
        self.init_line_edit(self.name_german_item)
        self.init_line_edit(self.name_italian_item)
        self.init_line_edit(self.name_spanish_item)
        self.init_line_edit(self.name_polish_item)
        self.init_line_edit(self.name_korean_item)

        self.init_spin_box(self.tlk_note_reference_item)
        self.init_line_edit(self.tlk_note_text_item)
        self.ui.tree.itemWidget(self.tlk_note_text_item, 1).setReadOnly(True)
        self.tlk_note_text_item.setDisabled(True)
        self.ui.tree.itemWidget(self.tlk_note_reference_item, 1).valueChanged.connect(self.tlk_note_changed)
        self.init_line_edit(self.note_english_item)
        self.init_line_edit(self.note_french_item)
        self.init_line_edit(self.note_german_item)
        self.init_line_edit(self.note_italian_item)
        self.init_line_edit(self.note_spanish_item)
        self.init_line_edit(self.note_polish_item)
        self.init_line_edit(self.note_korean_item)

        if self.installation is None:
            self.ui.tree.findItems("Name", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0].removeChild(self.tlk_name_text_item)
            self.ui.tree.findItems("Map Note", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[1].removeChild(self.tlk_note_text_item)

    def tlk_name_changed(self, index):
        self.ui.tree.itemWidget(self.tlk_name_text_item, 1).setText("")
        if self.installation is not None:
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.ui.tree.itemWidget(self.tlk_text_item, 1).setText(text)

    def tlk_note_changed(self, index):
        self.ui.tree.itemWidget(self.tlk_note_text_item, 1).setText("")
        if self.installation is not None:
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.ui.tree.itemWidget(self.tlk_text_item, 1).setText(text)

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
