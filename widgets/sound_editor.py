from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QLineEdit, QSpinBox, QCheckBox, QComboBox, QPushButton

from ui import sound_editor
from widgets.tree_editor import AbstractTreeEditor


class SoundEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = sound_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        playlist_button = QPushButton("...")
        playlist_button.setFixedHeight(17)
        playlist_button.clicked.connect(self.open_playlist_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Playlist", QtCore.Qt.MatchExactly)[0], 1, playlist_button)

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_spin_box("Basic", "Elevation")
        self.init_spin_box("Basic", "Interval")
        self.init_spin_box("Basic", "Interval Variation")
        self.init_spin_box("Basic", "Volume")
        self.init_spin_box("Basic", "Volume Variation")
        self.init_spin_box("Basic", "Pitch Variation")
        self.init_spin_box("Basic", "Min Distance")
        self.init_spin_box("Basic", "Max Distance")

        self.init_combo_box("Advanced", "Priority", items=["Unmaskable Sound", "Music/Stingers", "Streams Music",
                                                           "One-Shot Streams", "Looping Area-wide Ambience",
                                                           "Looping Positional Ambience", "Looping Player",
                                                           "Looping Non-player", "Player Chat", "Non-player Chat",
                                                           "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                                           "", ""])
        self.init_spin_box("Advanced", "X Variation")
        self.init_spin_box("Advanced", "Y Variation")

        self.init_check_box("Flags", "Active")
        self.init_check_box("Flags", "Continuous")
        self.init_check_box("Flags", "Looping")
        self.init_check_box("Flags", "Positional")
        self.init_check_box("Flags", "Random Position")
        self.init_check_box("Flags", "Random Order")

        self.init_localized_string_nodes("Name")

    def open_playlist_dialog(self):
        # TODO
        pass

    def load(self, utw):
        self.set_node_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Elevation", utw.find_field_data("Elevation", default=0))
        self.set_node_data("Basic", "Interval", utw.find_field_data("Interval", default=0))
        self.set_node_data("Basic", "Interval Variation", utw.find_field_data("IntervalVrtn", default=0))
        self.set_node_data("Basic", "Volume", utw.find_field_data("Volume", default=0))
        self.set_node_data("Basic", "Volume Variation", utw.find_field_data("VolumeVrtn", default=0))
        self.set_node_data("Basic", "Pitch Variation", utw.find_field_data("PitchVariation", default=0))
        self.set_node_data("Basic", "Min Distance", utw.find_field_data("MinDistance", default=0))
        self.set_node_data("Basic", "Max Distance", utw.find_field_data("MaxDistance", default=0))

        self.set_node_data("Advanced", "Priority", utw.find_field_data("Priority", default=0))
        self.set_node_data("Advanced", "X Variation", utw.find_field_data("RandomRangeX", default=0))
        self.set_node_data("Advanced", "Y Variation", utw.find_field_data("RandomRangeY", default=0))

        self.set_node_data("Flags", "Active", utw.find_field_data("Active", default=0))
        self.set_node_data("Flags", "Continuous", utw.find_field_data("Continuous", default=0))
        self.set_node_data("Flags", "Looping", utw.find_field_data("Looping", default=0))
        self.set_node_data("Flags", "Positional", utw.find_field_data("Positional", default=0))
        self.set_node_data("Flags", "Random Position", utw.find_field_data("RandomPosition", default=0))
        self.set_node_data("Flags", "Random Order", utw.find_field_data("Random", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocName"))
