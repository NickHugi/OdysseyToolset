import pyrr
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton, QSlider
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from ui import creature_editor
from widgets.model_renderer import Object, ModelRenderer
from widgets.tree_editor import AbstractTreeEditor


class CreatureEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = creature_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        feats_button = QPushButton("Feats")
        feats_button.setFixedHeight(17)
        feats_button.clicked.connect(self.open_feats_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Feats", QtCore.Qt.MatchExactly)[0], 1, feats_button)

        powers_button = QPushButton("Powers")
        powers_button.setFixedHeight(17)
        powers_button.clicked.connect(self.open_powers_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Powers", QtCore.Qt.MatchExactly)[0], 1, powers_button)

        inventory_button = QPushButton("Inventory")
        inventory_button.setFixedHeight(17)
        inventory_button.clicked.connect(self.open_inventory_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Inventory", QtCore.Qt.MatchExactly)[0], 1, inventory_button)

        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Dialog")
        self.init_slider("Basic", "Alignment")
        self.init_combo_box("Basic", "Class", Installation.get_class_list())
        self.init_combo_box("Basic", "Body Bag", Installation.get_bodybag_list())
        self.init_spin_box("Basic", "Level", 0, Installation.get_max_level())

        self.init_combo_box("Advanced", "Faction", Installation.get_faction_list())
        self.init_combo_box("Advanced", "Gender", Installation.get_gender_list())
        self.init_combo_box("Advanced", "Race", Installation.get_race_list())
        self.init_combo_box("Advanced", "Subrace", Installation.get_subrace_list())
        self.init_combo_box("Advanced", "Speed", Installation.get_speed_list())
        self.init_combo_box("Advanced", "Perception", Installation.get_perception_list())
        self.init_combo_box("Advanced", "Phenotype", Installation.get_phenotype_list())

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Detected")
        self.init_line_edit("Scripts", "Attacked Physically")
        self.init_line_edit("Scripts", "Attacked Ability")
        self.init_line_edit("Scripts", "Inventory Changed")
        self.init_line_edit("Scripts", "Round Ended")
        self.init_line_edit("Scripts", "After Talking")
        self.init_line_edit("Scripts", "Before Talking")
        self.init_line_edit("Scripts", "Spawned")
        self.init_line_edit("Scripts", "Death")
        self.init_line_edit("Scripts", "Blocked")
        self.init_line_edit("Scripts", "Custom")

        self.init_check_box("Flags", "Invincible")
        self.init_check_box("Flags", "Is PC")
        self.init_check_box("Flags", "Disarmable")
        self.init_check_box("Flags", "Doesn't Die")
        self.init_check_box("Flags", "Plot")
        self.init_check_box("Flags", "Doesn't Face PC")
        self.init_check_box("Flags", "Interruptable")
        self.init_check_box("Flags", "Interactable")

        self.init_spin_box("Name", "TLK Reference")
        self.get_node_widget("Name", "TLK Reference").valueChanged.connect(self.tlk_name_changed)
        self.init_line_edit("Name", "TLK Text")
        self.get_node_widget("Name", "TLK Text").setReadOnly(True)
        self.init_line_edit("Name", "English")
        self.init_line_edit("Name", "French")
        self.init_line_edit("Name", "German")
        self.init_line_edit("Name", "Italian")
        self.init_line_edit("Name", "Spanish")
        self.init_line_edit("Name", "Polish")
        self.init_line_edit("Name", "Korean")

        self.init_spin_box("Attributes", "Strength")
        self.init_spin_box("Attributes", "Dexterity")
        self.init_spin_box("Attributes", "Constitution")
        self.init_spin_box("Attributes", "Intelligence")
        self.init_spin_box("Attributes", "Wisdom")
        self.init_spin_box("Attributes", "Charisma")

        self.init_spin_box("Skills", "Computer Use")
        self.init_spin_box("Skills", "Demolitions")
        self.init_spin_box("Skills", "Stealth")
        self.init_spin_box("Skills", "Awareness")
        self.init_spin_box("Skills", "Persuade")
        self.init_spin_box("Skills", "Repair")
        self.init_spin_box("Skills", "Security")
        self.init_spin_box("Skills", "Treat Injury")

        self.init_spin_box("Other", "Challenge Rating")
        self.init_spin_box("Other", "Natural AC")
        self.init_spin_box("Other", "Fortitude")
        self.init_spin_box("Other", "Reflex")
        self.init_spin_box("Other", "Will")
        self.init_spin_box("Other", "Health")
        self.init_spin_box("Other", "Force")

        if self.installation is None:
            self.get_node("Name", "TLK Text").parent().removeChild(self.get_node("Name", "TLK Text"))
            self.init_spin_box("Basic", "Appearance")
            self.init_spin_box("Advanced", "Soundset")
        else:
            self.init_combo_box("Basic", "Appearance", items=Installation.get_appearance_list(self.installation))
            self.get_node_widget("Basic", "Appearance").currentIndexChanged.connect(self.appearance_changed)
            self.init_combo_box("Advanced", "Soundset", items=Installation.get_soundset_list(self.installation))

    def open_feats_dialog(self):
        # TODO
        print("open feat dialog")

    def open_powers_dialog(self):
        # TODO
        print("open powers dialog")

    def open_inventory_dialog(self):
        # TODO
        print("open inventory dialog")

    def tlk_name_changed(self, index):
        if self.installation is not None:
            self.get_node_widget("Name", "TLK Text").setText("")
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.get_node_widget("Name", "TLK Text").setText(text)

    def appearance_changed(self, index):
        try:
            models = self.installation.get_appearance_model(index)

            self.model_renderer.objects.clear()

            self.model_renderer.model_buffer["body"] = models[0]
            self.model_renderer.objects.append(Object("body"))
            if len(models) == 2:
                head_position = models[0].find_node("headhook").get_absolute_position()
                head_position_pyrr = pyrr.vector3.create(head_position.x, head_position.y, head_position.z)

                self.model_renderer.model_buffer["head"] = models[1]
                head_object = Object("head", head_position_pyrr)
                self.model_renderer.objects.append(head_object)
        except Exception as e:
            print("Failed to load creature appearance model:", e)
