from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox

from ui import trigger_editor


class TriggerEditor(QWidget):
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

        self.init_line_edit(self.script_tag_item)
        self.init_line_edit(self.template_item)

        self.init_spin_box(self.tlk_reference_item)
        self.init_line_edit(self.tlk_text_item)
        self.ui.tree.itemWidget(self.tlk_text_item, 1).setReadOnly(True)
        self.tlk_text_item.setDisabled(True)
        self.ui.tree.itemWidget(self.tlk_reference_item, 1).valueChanged.connect(self.tlk_reference_changed)
        self.init_line_edit(self.english_item)
        self.init_line_edit(self.french_item)
        self.init_line_edit(self.german_item)
        self.init_line_edit(self.italian_item)
        self.init_line_edit(self.spanish_item)
        self.init_line_edit(self.polish_item)
        self.init_line_edit(self.korean_item)

        self.init_combo_box(self.type_item, ["Generic", "Area Transition", "Trap"])
        self.init_combo_box(self.faction_item, ["Friendly 1", "Hostile 2", "Friendly 2", "Neutral", "Insane", "Tuskan",
                                                "GLB XOR", "Surrender 1", "Surrender 2", "Predator", "Prey", "Trap",
                                                "Endar Spire", "Rancor", "Gizka 1", "Gizka 2", "Czerka",
                                                "Zone Controller", "Sacrafice", "One On One", "Party Puppet"])

        self.init_check_box(self.is_trap_item)
        self.init_combo_box(self.trap_type_item)
        self.init_check_box(self.one_shot_type)
        self.init_check_box(self.disarmable_type)
        self.init_check_box(self.findable_type)
        self.init_spin_box(self.detection_dc_type)
        self.init_spin_box(self.disarm_dc_type)

        self.init_line_edit(self.routine_item)
        self.init_line_edit(self.entered_item)
        self.init_line_edit(self.exited_item)
        self.init_line_edit(self.clicked_item)
        self.init_line_edit(self.triggered_item)
        self.init_line_edit(self.disarmed_item)
        self.init_line_edit(self.custom_item)

        if self.installation is None:
            self.ui.tree.findItems("Naming", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0].removeChild(
                self.tlk_text_item)

    def tlk_reference_changed(self, index):
        self.ui.tree.itemWidget(self.tlk_text_item, 1).setText("")
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
