from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QLineEdit, QSpinBox, QCheckBox, QComboBox, QPushButton

from pykotor.formats.gff import List, GFF, FieldType, Struct
from ui import sound_editor
from widgets.playlist_dialog import PlaylistDialog
from widgets.tree_editor import AbstractTreeEditor


class SoundEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = sound_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        self.playlist = []

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
        dialog = PlaylistDialog(self, self.playlist, self.installation)
        dialog.exec_()
        self.playlist = dialog.get_playlist()

    def load(self, uts):
        self.set_node_data("Basic", "Script Tag", uts.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", uts.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Elevation", uts.find_field_data("Elevation", default=0))
        self.set_node_data("Basic", "Interval", uts.find_field_data("Interval", default=0))
        self.set_node_data("Basic", "Interval Variation", uts.find_field_data("IntervalVrtn", default=0))
        self.set_node_data("Basic", "Volume", uts.find_field_data("Volume", default=0))
        self.set_node_data("Basic", "Volume Variation", uts.find_field_data("VolumeVrtn", default=0))
        self.set_node_data("Basic", "Pitch Variation", uts.find_field_data("PitchVariation", default=0))
        self.set_node_data("Basic", "Min Distance", uts.find_field_data("MinDistance", default=0))
        self.set_node_data("Basic", "Max Distance", uts.find_field_data("MaxDistance", default=0))

        self.set_node_data("Advanced", "Priority", uts.find_field_data("Priority", default=0))
        self.set_node_data("Advanced", "X Variation", uts.find_field_data("RandomRangeX", default=0))
        self.set_node_data("Advanced", "Y Variation", uts.find_field_data("RandomRangeY", default=0))

        self.set_node_data("Flags", "Active", uts.find_field_data("Active", default=0))
        self.set_node_data("Flags", "Continuous", uts.find_field_data("Continuous", default=0))
        self.set_node_data("Flags", "Looping", uts.find_field_data("Looping", default=0))
        self.set_node_data("Flags", "Positional", uts.find_field_data("Positional", default=0))
        self.set_node_data("Flags", "Random Position", uts.find_field_data("RandomPosition", default=0))
        self.set_node_data("Flags", "Random Order", uts.find_field_data("Random", default=0))

        self.set_localized_string_nodes("Name", uts.find_field_data("LocName"))

        for i in range(len(uts.find_field_data("Sounds", default=List([])).structs)):
            sound = uts.find_field_data("Sounds", i, "Sound", default="")
            self.playlist.append(sound)

    def build(self):
        uts = GFF()

        uts.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        uts.root.add_field(FieldType.ResRef, "TemplateResRef", self.get_node_data("Basic", "Template"))
        uts.root.add_field(FieldType.Float, "Elevation", self.get_node_data("Basic", "Elevation"))
        uts.root.add_field(FieldType.UInt32, "Interval", self.get_node_data("Basic", "Interval"))
        uts.root.add_field(FieldType.UInt32, "IntervalVrtn", self.get_node_data("Basic", "Interval Variation"))
        uts.root.add_field(FieldType.UInt8, "Volume", self.get_node_data("Basic", "Volume"))
        uts.root.add_field(FieldType.Float, "VolumeVrtn", self.get_node_data("Basic", "Volume Variation"))
        uts.root.add_field(FieldType.Float, "PitchVariation", self.get_node_data("Basic", "Pitch Variation"))
        uts.root.add_field(FieldType.Float, "MinDistance", self.get_node_data("Basic", "Min Distance"))
        uts.root.add_field(FieldType.Float, "MaxDistance", self.get_node_data("Basic", "Max Distance"))

        uts.root.add_field(FieldType.LocalizedString, "LocName", self.get_node_localized_string("Name"))

        uts.root.add_field(FieldType.UInt8, "Priority", self.get_node_data("Advanced", "Priority"))
        uts.root.add_field(FieldType.Float, "RandomRangeX", self.get_node_data("Advanced", "X Variation"))
        uts.root.add_field(FieldType.Float, "RandomRangeY", self.get_node_data("Advanced", "Y Variation"))

        uts.root.add_field(FieldType.UInt8, "Active", self.get_node_data("Flags", "Active"))
        uts.root.add_field(FieldType.UInt8, "Continuous", self.get_node_data("Flags", "Continuous"))
        uts.root.add_field(FieldType.UInt8, "Looping", self.get_node_data("Flags", "Looping"))
        uts.root.add_field(FieldType.UInt8, "Positional", self.get_node_data("Flags", "Positional"))
        uts.root.add_field(FieldType.UInt8, "RandomPosition", self.get_node_data("Flags", "Random Position"))
        uts.root.add_field(FieldType.UInt8, "Random", self.get_node_data("Flags", "Random Order"))

        uts_sound_list = List([])
        for sound in self.playlist:
            uts_sound_struct = Struct(0, [])
            uts_sound_struct.add_field(FieldType.ResRef, "Sound", sound)
            uts_sound_list.structs.append(uts_sound_struct)
        uts.root.add_field(FieldType.List, "CreatureList", uts_sound_list)

        return uts
