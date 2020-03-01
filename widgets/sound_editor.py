from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QLineEdit, QSpinBox, QCheckBox, QComboBox, QPushButton

from ui import sound_editor


class SoundEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = sound_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        search_flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive

        self.playlist_item = self.ui.tree.findItems("Playlist", search_flags)[0]

        self.script_tag_item = self.ui.tree.findItems("Script Tag", search_flags)[0]
        self.template_item = self.ui.tree.findItems("Template", search_flags)[0]
        self.elevation_item = self.ui.tree.findItems("Elevation", search_flags)[0]
        self.interval_item = self.ui.tree.findItems("Interval", search_flags)[0]
        self.interval_variation_item = self.ui.tree.findItems("Interval Variation", search_flags)[0]
        self.volume_item = self.ui.tree.findItems("Volume", search_flags)[0]
        self.volume_variation_item = self.ui.tree.findItems("Volume Variation", search_flags)[0]
        self.pitch_variation_item = self.ui.tree.findItems("Pitch Variation", search_flags)[0]
        self.min_distance_item = self.ui.tree.findItems("Min Distance", search_flags)[0]
        self.max_distance_item = self.ui.tree.findItems("Max Distance", search_flags)[0]

        self.priority_item = self.ui.tree.findItems("Priority", search_flags)[0]
        self.x_variation_item = self.ui.tree.findItems("X Variation", search_flags)[0]
        self.y_variation_item = self.ui.tree.findItems("Y Variation", search_flags)[0]

        self.active_item = self.ui.tree.findItems("Active", search_flags)[0]
        self.continuous_item = self.ui.tree.findItems("Continuous", search_flags)[0]
        self.looping_item = self.ui.tree.findItems("Looping", search_flags)[0]
        self.positional_item = self.ui.tree.findItems("Positional", search_flags)[0]
        self.random_position_item = self.ui.tree.findItems("Random Position", search_flags)[0]
        self.random_order_item = self.ui.tree.findItems("Random Order", search_flags)[0]

        self.tlk_reference_item = self.ui.tree.findItems("TLK Reference", search_flags)[0]
        self.tlk_text_item = self.ui.tree.findItems("TLK Text", search_flags)[0]
        self.english_item = self.ui.tree.findItems("English", search_flags)[0]
        self.french_item = self.ui.tree.findItems("French", search_flags)[0]
        self.german_item = self.ui.tree.findItems("German", search_flags)[0]
        self.italian_item = self.ui.tree.findItems("Italian", search_flags)[0]
        self.spanish_item = self.ui.tree.findItems("Spanish", search_flags)[0]
        self.polish_item = self.ui.tree.findItems("Polish", search_flags)[0]
        self.korean_item = self.ui.tree.findItems("Korean", search_flags)[0]

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_button(self.playlist_item, "...")

        self.ui.tree.itemWidget(self.playlist_item, 1).clicked.connect(self.open_inventory_dialog)

        self.init_line_edit(self.script_tag_item)
        self.init_line_edit(self.template_item)
        self.init_spin_box(self.elevation_item)
        self.init_spin_box(self.interval_item)
        self.init_spin_box(self.interval_variation_item)
        self.init_spin_box(self.volume_item)
        self.init_spin_box(self.volume_variation_item)
        self.init_spin_box(self.pitch_variation_item)
        self.init_spin_box(self.min_distance_item)
        self.init_spin_box(self.max_distance_item)

        self.init_combo_box(self.priority_item, ["Unmaskable Sound", "Music/Stingers", "Streams Music",
                                                 "One-Shot Streams", "Looping Area-wide Ambience",
                                                 "Looping Positional Ambience", "Looping Player",
                                                 "Looping Non-player", "Player Chat", "Non-player Chat",
                                                 "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
        self.init_spin_box(self.x_variation_item)
        self.init_spin_box(self.y_variation_item)

        self.init_check_box(self.active_item)
        self.init_check_box(self.continuous_item)
        self.init_check_box(self.looping_item)
        self.init_check_box(self.positional_item)
        self.init_check_box(self.random_position_item)
        self.init_check_box(self.random_order_item)

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

        if self.installation is None:
            self.ui.tree.findItems("Naming", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0].removeChild(
                self.tlk_text_item)

    def open_inventory_dialog(self):
        # TODO
        pass

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
