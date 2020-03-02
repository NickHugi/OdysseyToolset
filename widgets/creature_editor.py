from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton, QSlider

from installation import Installation
from ui import creature_editor


class CreatureEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = creature_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        search_flags = QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive

        self.script_tag_item = self.ui.tree.findItems("Script Tag", search_flags)[0]
        self.template_item = self.ui.tree.findItems("Template", search_flags)[0]
        self.dialog_item = self.ui.tree.findItems("Dialog", search_flags)[0]
        self.alignment_item = self.ui.tree.findItems("Alignment", search_flags)[0]

        self.appearance_item = self.ui.tree.findItems("Appearance", search_flags)[0]
        self.body_bag_item = self.ui.tree.findItems("Body Bag", search_flags)[0]
        self.class_item = self.ui.tree.findItems("Class", search_flags)[0]
        self.level_item = self.ui.tree.findItems("Level", search_flags)[0]

        self.race_item = self.ui.tree.findItems("Race", search_flags)[0]
        self.subrace_item = self.ui.tree.findItems("Subrace", search_flags)[0]
        self.phenotype_item = self.ui.tree.findItems("Phenotype", search_flags)[0]
        self.perception_item = self.ui.tree.findItems("Perception", search_flags)[0]
        self.soundset_item = self.ui.tree.findItems("Soundset", search_flags)[0]
        self.faction_item = self.ui.tree.findItems("Faction", search_flags)[0]
        self.gender_item = self.ui.tree.findItems("Gender", search_flags)[0]
        self.speed_item = self.ui.tree.findItems("Speed", search_flags)[0]
        self.portrait_item = self.ui.tree.findItems("Portrait", search_flags)[0]

        self.tlk_name_reference_item = self.ui.tree.findItems("TLK Reference", search_flags)[0]
        self.tlk_name_text_item = self.ui.tree.findItems("TLK Text", search_flags)[0]
        self.name_english_item = self.ui.tree.findItems("English", search_flags)[0]
        self.name_french_item = self.ui.tree.findItems("French", search_flags)[0]
        self.name_german_item = self.ui.tree.findItems("German", search_flags)[0]
        self.name_italian_item = self.ui.tree.findItems("Italian", search_flags)[0]
        self.name_spanish_item = self.ui.tree.findItems("Spanish", search_flags)[0]
        self.name_polish_item = self.ui.tree.findItems("Polish", search_flags)[0]
        self.name_korean_item = self.ui.tree.findItems("Korean", search_flags)[0]

        self.strength_item = self.ui.tree.findItems("Strength", search_flags)[0]
        self.dexterity_item = self.ui.tree.findItems("Dexterity", search_flags)[0]
        self.constitution_item = self.ui.tree.findItems("Constitution", search_flags)[0]
        self.intelligence_item = self.ui.tree.findItems("Intelligence", search_flags)[0]
        self.wisdom_item = self.ui.tree.findItems("Wisdom", search_flags)[0]
        self.charisma_item = self.ui.tree.findItems("Charisma", search_flags)[0]

        self.computer_use_item = self.ui.tree.findItems("Computer Use", search_flags)[0]
        self.demolitions_item = self.ui.tree.findItems("Demolitions", search_flags)[0]
        self.stealth_item = self.ui.tree.findItems("Stealth", search_flags)[0]
        self.awareness_item = self.ui.tree.findItems("Awareness", search_flags)[0]
        self.persuade_item = self.ui.tree.findItems("Persuade", search_flags)[0]
        self.repair_item = self.ui.tree.findItems("Repair", search_flags)[0]
        self.security_item = self.ui.tree.findItems("Security", search_flags)[0]
        self.treat_injury_item = self.ui.tree.findItems("Treat Injury", search_flags)[0]

        self.challenge_rating_item = self.ui.tree.findItems("Challenge Rating", search_flags)[0]
        self.natural_ac_item = self.ui.tree.findItems("Natural AC", search_flags)[0]
        self.fortitude_item = self.ui.tree.findItems("Fortitude", search_flags)[0]
        self.reflex_item = self.ui.tree.findItems("Reflex", search_flags)[0]
        self.will_item = self.ui.tree.findItems("Will", search_flags)[0]
        self.health_item = self.ui.tree.findItems("Health", search_flags)[0]
        self.force_item = self.ui.tree.findItems("Force", search_flags)[0]

        self.invincible_item = self.ui.tree.findItems("Invincible", search_flags)[0]
        self.is_pc_item = self.ui.tree.findItems("Is PC", search_flags)[0]
        self.disarmable_item = self.ui.tree.findItems("Disarmable", search_flags)[0]
        self.doesnt_die_item = self.ui.tree.findItems("Doesn't Die", search_flags)[0]
        self.plot_item = self.ui.tree.findItems("Plot", search_flags)[0]
        self.doesnt_face_pc_item = self.ui.tree.findItems("Doesn't Face PC", search_flags)[0]
        self.interruptable_item = self.ui.tree.findItems("Interruptable", search_flags)[0]
        self.interactable_item = self.ui.tree.findItems("Interactable", search_flags)[0]

        self.routine_item = self.ui.tree.findItems("Routine", search_flags)[0]
        self.detected_item = self.ui.tree.findItems("Detected", search_flags)[0]
        self.attacked_physical_item = self.ui.tree.findItems("Attacked Physical", search_flags)[0]
        self.attacked_ability_item = self.ui.tree.findItems("Attacked Ability", search_flags)[0]
        self.damaged_item = self.ui.tree.findItems("Damaged", search_flags)[0]
        self.inventory_changed_item = self.ui.tree.findItems("Inventory Changed", search_flags)[0]
        self.round_ended_item = self.ui.tree.findItems("Round Ended", search_flags)[0]
        self.after_talking_item = self.ui.tree.findItems("After Talking", search_flags)[0]
        self.before_talking_item = self.ui.tree.findItems("Before Talking", search_flags)[0]
        self.spawned_item = self.ui.tree.findItems("Spawned", search_flags)[0]
        self.death_item = self.ui.tree.findItems("Death", search_flags)[0]
        self.blocked_item = self.ui.tree.findItems("Blocked", search_flags)[0]
        self.custom_item = self.ui.tree.findItems("Custom", search_flags)[0]

        self.feats_item = self.ui.tree.findItems("Feats", search_flags)[0]
        self.powers_item = self.ui.tree.findItems("Powers", search_flags)[0]
        self.inventory_item = self.ui.tree.findItems("Inventory", search_flags)[0]

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_button(self.feats_item, "...")
        self.ui.tree.itemWidget(self.feats_item, 1).clicked.connect(self.open_feats_dialog)
        self.init_button(self.powers_item, "...")
        self.ui.tree.itemWidget(self.powers_item, 1).clicked.connect(self.open_powers_dialog)
        self.init_button(self.inventory_item, "...")
        self.ui.tree.itemWidget(self.inventory_item, 1).clicked.connect(self.open_inventory_dialog)

        self.init_combo_box(self.faction_item, Installation.get_faction_list())
        self.init_combo_box(self.gender_item, Installation.get_gender_list())
        self.init_combo_box(self.race_item, Installation.get_race_list())
        self.init_combo_box(self.subrace_item, Installation.get_subrace_list())
        self.init_combo_box(self.speed_item, Installation.get_speed_list())
        self.init_combo_box(self.perception_item, Installation.get_perception_list())
        self.init_combo_box(self.phenotype_item, Installation.get_phenotype_list())
        self.init_combo_box(self.class_item, Installation.get_class_list())
        self.init_combo_box(self.body_bag_item, Installation.get_bodybag_list())
        self.init_spin_box(self.level_item, 0, Installation.get_max_level())

        self.init_line_edit(self.routine_item)
        self.init_line_edit(self.detected_item)
        self.init_line_edit(self.attacked_physical_item)
        self.init_line_edit(self.attacked_ability_item)
        self.init_line_edit(self.inventory_changed_item)
        self.init_line_edit(self.round_ended_item)
        self.init_line_edit(self.after_talking_item)
        self.init_line_edit(self.before_talking_item)
        self.init_line_edit(self.spawned_item)
        self.init_line_edit(self.death_item)
        self.init_line_edit(self.blocked_item)
        self.init_line_edit(self.custom_item)

        self.init_check_box(self.invincible_item)
        self.init_check_box(self.is_pc_item)
        self.init_check_box(self.disarmable_item)
        self.init_check_box(self.doesnt_die_item)
        self.init_check_box(self.plot_item)
        self.init_check_box(self.doesnt_face_pc_item)
        self.init_check_box(self.interruptable_item)
        self.init_check_box(self.interactable_item)

        self.init_line_edit(self.script_tag_item)
        self.init_line_edit(self.dialog_item)
        self.init_line_edit(self.template_item)
        self.init_slider(self.alignment_item)

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

        self.init_spin_box(self.strength_item)
        self.init_spin_box(self.dexterity_item)
        self.init_spin_box(self.constitution_item)
        self.init_spin_box(self.intelligence_item)
        self.init_spin_box(self.wisdom_item)
        self.init_spin_box(self.charisma_item)

        self.init_spin_box(self.computer_use_item)
        self.init_spin_box(self.demolitions_item)
        self.init_spin_box(self.stealth_item)
        self.init_spin_box(self.awareness_item)
        self.init_spin_box(self.persuade_item)
        self.init_spin_box(self.repair_item)
        self.init_spin_box(self.security_item)
        self.init_spin_box(self.treat_injury_item)

        self.init_spin_box(self.challenge_rating_item)
        self.init_spin_box(self.natural_ac_item)
        self.init_spin_box(self.fortitude_item)
        self.init_spin_box(self.reflex_item)
        self.init_spin_box(self.will_item)
        self.init_spin_box(self.health_item)
        self.init_spin_box(self.force_item)

        if self.installation is None:
            self.ui.tree.findItems("Name", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0].removeChild(self.tlk_name_text_item)
            self.init_spin_box(self.appearance_item)
            self.init_spin_box(self.soundset_item)
        else:
            self.init_combo_box(self.appearance_item, Installation.get_appearance_list(self.installation))
            self.init_combo_box(self.soundset_item, Installation.get_soundset_list(self.installation))

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
            self.ui.tree.itemWidget(self.tlk_name_text_item, 1).setText("")
            if index < self.installation.get_tlk_entry_count():
                text = self.installation.get_tlk_entry_text(index)
                self.ui.tree.itemWidget(self.tlk_name_text_item, 1).setText(text)

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

    def init_slider(self, item, min=0, max=100):
        slider = QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setFixedHeight(23)
        self.ui.tree.setItemWidget(item, 1, slider)
        return slider
