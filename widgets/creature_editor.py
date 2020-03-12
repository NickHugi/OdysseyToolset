import math

import pyrr
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton, QSlider, QFileDialog

from pykotor.formats.gff import GFF, FieldType, Struct, List
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from ui import creature_editor
from widgets.ability_dialog import AbilityDialog
from widgets.inventory_dialog import InventoryDialog, Inventory, InventoryItem
from widgets.model_renderer import Object, ModelRenderer
from widgets.tree_editor import AbstractTreeEditor


class CreatureEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = creature_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        self.inventory = Inventory()
        self.powers = {}
        self.feats = {}

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        feats_button = QPushButton("...")
        feats_button.setFixedHeight(17)
        feats_button.clicked.connect(self.open_feats_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Feats", QtCore.Qt.MatchExactly)[0], 1, feats_button)

        powers_button = QPushButton("...")
        powers_button.setFixedHeight(17)
        powers_button.clicked.connect(self.open_powers_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Powers", QtCore.Qt.MatchExactly)[0], 1, powers_button)

        inventory_button = QPushButton("...")
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
        self.init_line_edit("Scripts", "Attacked Physical")
        self.init_line_edit("Scripts", "Attacked Ability")
        self.init_line_edit("Scripts", "Damaged")
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

        self.init_localized_string_nodes("Name")

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

        self.init_double_spin_box("Other", "Challenge Rating")
        self.init_spin_box("Other", "Natural AC")
        self.init_spin_box("Other", "Fortitude")
        self.init_spin_box("Other", "Reflex")
        self.init_spin_box("Other", "Will")
        self.init_spin_box("Other", "Health")
        self.init_spin_box("Other", "Force")

        if self.installation is None:
            self.init_spin_box("Basic", "Appearance")
            self.init_spin_box("Advanced", "Soundset")
        else:
            self.init_combo_box("Basic", "Appearance", items=Installation.get_appearance_list(self.installation))
            self.get_node_widget("Basic", "Appearance").currentIndexChanged.connect(self.appearance_changed)
            self.init_combo_box("Advanced", "Soundset", items=Installation.get_soundset_list(self.installation))

    def open_feats_dialog(self):
        dialog = AbilityDialog(self, self.feats, Installation.get_feats_list(self.installation))
        dialog.exec_()
        self.feats = dialog.get_bools()

    def open_powers_dialog(self):
        dialog = AbilityDialog(self, self.powers, Installation.get_powers_list(self.installation))
        dialog.exec_()
        self.powers = dialog.get_bools()

    def open_inventory_dialog(self):
        dialog = InventoryDialog(self, self.inventory, self.installation)
        dialog.exec_()
        self.inventory = dialog.get_inventory()

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

    def load(self, utc):
        self.set_node_data("Skills", "Computer Use", utc.find_field_data("SkillList", 0, "Rank", default=0))
        self.set_node_data("Skills", "Demolitions", utc.find_field_data("SkillList", 1, "Rank", default=0))
        self.set_node_data("Skills", "Stealth", utc.find_field_data("SkillList", 2, "Rank", default=0))
        self.set_node_data("Skills", "Awareness", utc.find_field_data("SkillList", 3, "Rank", default=0))
        self.set_node_data("Skills", "Persuade", utc.find_field_data("SkillList", 4, "Rank", default=0))
        self.set_node_data("Skills", "Repair", utc.find_field_data("SkillList", 5, "Rank", default=0))
        self.set_node_data("Skills", "Security", utc.find_field_data("SkillList", 6, "Rank", default=0))
        self.set_node_data("Skills", "Treat Injury", utc.find_field_data("SkillList", 7, "Rank", default=0))

        self.set_node_data("Basic", "Script Tag", utc.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utc.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Appearance", utc.find_field_data("Appearance_Type", default=0))
        self.set_node_data("Basic", "Body Bag", utc.find_field_data("BodyBag", default=0))
        self.set_node_data("Basic", "Dialog", utc.find_field_data("Conversation", default=0))
        self.set_node_data("Basic", "Alignment", utc.find_field_data("GoodEvil", default=0))
        self.set_node_data("Basic", "Class", utc.find_field_data("ClassList", 0, "Class", default=0))
        self.set_node_data("Basic", "Level", utc.find_field_data("ClassList", 0, "ClassLevel", default=0))
        self.set_node_data("Basic", "Alignment", utc.find_field_data("ClassList", 0, "Class", default=0))

        self.set_node_data("Advanced", "Faction", utc.find_field_data("FactionID", default=4))
        self.set_node_data("Advanced", "Gender", utc.find_field_data("Gender", default=0))
        self.set_node_data("Advanced", "Perception", utc.find_field_data("PerceptionRange", default=8) - 8)  # starts at index 8
        self.set_node_data("Advanced", "Phenotype", utc.find_field_data("Phenotype", default=0))
        self.set_node_data("Advanced", "Race", utc.find_field_data("Race", default=6) - 5)  # starts at index 5
        self.set_node_data("Advanced", "Subrace", utc.find_field_data("SubraceIndex", default=0))
        self.set_node_data("Advanced", "Soundset", utc.find_field_data("SoundSetFile", default=0))
        self.set_node_data("Advanced", "Speed", utc.find_field_data("WalkRate", default=0))

        self.set_node_data("Attributes", "Strength", utc.find_field_data("Str", default=0))
        self.set_node_data("Attributes", "Dexterity", utc.find_field_data("Dex", default=0))
        self.set_node_data("Attributes", "Constitution", utc.find_field_data("Con", default=0))
        self.set_node_data("Attributes", "Intelligence", utc.find_field_data("Int", default=0))
        self.set_node_data("Attributes", "Charisma", utc.find_field_data("Cha", default=0))
        self.set_node_data("Attributes", "Wisdom", utc.find_field_data("Wis", default=0))

        self.set_node_data("Scripts", "Attacked Physical", utc.find_field_data("ScriptAttacked", default=0))
        self.set_node_data("Scripts", "Damaged", utc.find_field_data("ScriptDamaged", default=0))
        self.set_node_data("Scripts", "Death", utc.find_field_data("ScriptDeath", default=0))
        self.set_node_data("Scripts", "Before Talking", utc.find_field_data("ScriptDialogue", default=0))
        self.set_node_data("Scripts", "Inventory Changed", utc.find_field_data("ScriptDisturbed", default=0))
        self.set_node_data("Scripts", "After Talking", utc.find_field_data("ScriptEndDialogu", default=0))
        self.set_node_data("Scripts", "Round Ended", utc.find_field_data("ScriptEndRound", default=0))
        self.set_node_data("Scripts", "Routine", utc.find_field_data("ScriptHeartbeat", default=0))
        self.set_node_data("Scripts", "Blocked", utc.find_field_data("ScriptOnBlocked", default=0))
        self.set_node_data("Scripts", "Detected", utc.find_field_data("ScriptOnNotice", default=0))
        self.set_node_data("Scripts", "Spawned", utc.find_field_data("ScriptSpawn", default=0))
        self.set_node_data("Scripts", "Attacked Ability", utc.find_field_data("ScriptSpellAt", default=0))
        self.set_node_data("Scripts", "Routine", utc.find_field_data("ScriptUserDefine", default=0))

        self.set_node_data("Flags", "Disarmable", utc.find_field_data("Disarmable", default=0))
        self.set_node_data("Flags", "Interruptable", utc.find_field_data("Interruptable", default=0))
        self.set_node_data("Flags", "Is PC", utc.find_field_data("IsPC", default=0))
        self.set_node_data("Flags", "Invincible", utc.find_field_data("Min1HP", default=0))
        self.set_node_data("Flags", "Doesn't Die", utc.find_field_data("NoPermDeath", default=0))
        self.set_node_data("Flags", "Doesn't Face PC", utc.find_field_data("NotReorienting", default=0))
        self.set_node_data("Flags", "Interactable", utc.find_field_data("PartyInteract", default=0))
        self.set_node_data("Flags", "Plot", utc.find_field_data("Plot", default=0))

        self.set_node_data("Other", "Challenge Rating", utc.find_field_data("ChallengeRating", default=0))
        self.set_node_data("Other", "Health", utc.find_field_data("MaxHitPoints", default=0))
        self.set_node_data("Other", "Force", utc.find_field_data("ForcePoints", default=0))
        self.set_node_data("Other", "Fortitude", utc.find_field_data("fortbonus", default=0))
        self.set_node_data("Other", "Reflex", utc.find_field_data("refbonus", default=0))
        self.set_node_data("Other", "Will", utc.find_field_data("willbonus", default=0))
        self.set_node_data("Other", "Natural AC", utc.find_field_data("NaturalAC", default=0))

        for i in range(len(utc.find_field_data("FeatList", default=List([])).structs)):
            feat_id = utc.find_field_data("FeatList", i, "Feat", default=-1)
            if feat_id != -1: self.feats[feat_id] = True

        for i in range(len(utc.find_field_data("ClassList", 0, "KnownList0", default=List([])).structs)):
            power_id = utc.find_field_data("ClassList", 0, "KnownList0", i, "Spell", default=-1)
            if power_id != -1: self.powers[power_id] = True

        for i in range(len(utc.find_field_data("Equip_ItemList", default=List([])).structs)):
            struct_id = utc.find_field_data("Equip_ItemList", i, default=Struct(-1, [])).id
            equipment_id = int(math.log2(struct_id))
            equipment_resref = utc.find_field_data("Equip_ItemList", i, "EquippedRes", default="")
            if equipment_id != -1: self.inventory.equipment[equipment_id] = equipment_resref

        for i in range(len(utc.find_field_data("ItemList", default=List([])).structs)):
            item_resref = utc.find_field_data("ItemList", i, "InventoryRes", default="")
            item_dropable = utc.find_field_data("ItemList", i, "Dropable", default="")
            if item_resref != "": self.inventory.items.append(InventoryItem(item_resref, item_dropable))

        self.set_localized_string_nodes("Name", utc.find_field_data("FirstName"))

    def save(self, path):
        utc = GFF()

        utc.root.add_field(FieldType.String, "Tag", self.get_node_data("Basic", "Script Tag"))
        utc.root.add_field(FieldType.ResRef, "TemplateResRef", self.get_node_data("Basic", "Template"))
        utc.root.add_field(FieldType.UInt16, "Appearance_Type", self.get_node_data("Basic", "Appearance"))
        utc.root.add_field(FieldType.UInt8, "BodyBag", self.get_node_data("Basic", "Body Bag"))
        utc.root.add_field(FieldType.ResRef, "Conversation", self.get_node_data("Basic", "Dialog"))
        utc.root.add_field(FieldType.UInt8, "GoodEvil", self.get_node_data("Basic", "Alignment"))

        utc_class_struct = Struct(2, [])
        utc_class_struct.add_field(FieldType.Int32, "Class", self.get_node_data("Basic", "Class"))
        utc_class_struct.add_field(FieldType.Int16, "ClassLevel", self.get_node_data("Basic", "Level"))
        utc.root.add_field(FieldType.List, "ClassList", List([utc_class_struct]))

        utc_power_list = List([])
        for power_id, unlocked in self.powers.items():
            if unlocked:
                power_struct = Struct(3, [])
                power_struct.add_field(FieldType.UInt16, "Spell", power_id)
                power_struct.add_field(FieldType.UInt8, "SpellFlags", 1)
                power_struct.add_field(FieldType.UInt8, "SpellMetaMagic", 0)
                utc_power_list.structs.append(power_struct)
        utc_class_struct.add_field(FieldType.List, "KnownList0", utc_power_list)

        utc_feat_list = List([])
        for feat_id, unlocked in self.feats.items():
            if unlocked:
                feat_struct = Struct(1, [])
                feat_struct.add_field(FieldType.UInt16, "Feat", feat_id)
                utc_feat_list.structs.append(feat_struct)
        utc.root.add_field(FieldType.List, "FeatList", utc_feat_list)

        utc_item_list = List([])
        for slot, item in enumerate(self.inventory.items):
            item_struct = Struct(slot, [])
            item_struct.add_field(FieldType.ResRef, "InventoryRes", item.res_ref)
            item_struct.add_field(FieldType.UInt16, "Repos_PosX", slot)
            item_struct.add_field(FieldType.UInt16, "Repos_PosY", 0)
            if item.dropable: item_struct.add_field(FieldType.UInt8, "Dropable", 1)
            utc_item_list.structs.append(item_struct)
        utc.root.add_field(FieldType.List, "ItemList", utc_item_list)

        utc_equipment_list = List([])
        for i, res_ref in self.inventory.equipment.items():
            slot = int(math.pow(2, i))
            item_struct = Struct(slot, [])
            item_struct.add_field(FieldType.ResRef, "EquippedRes", res_ref)
            utc_equipment_list.structs.append(item_struct)
        utc.root.add_field(FieldType.List, "Equip_ItemList", utc_equipment_list)

        utc.root.add_field(FieldType.LocalizedString, "FirstName", self.get_node_localized_string("Name"))
        utc.to_path(path)
