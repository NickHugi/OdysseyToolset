from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialog, QCheckBox, QTableWidgetItem, QListWidgetItem

from installation import Installation
from ui import ability_dialog, item_property_dialog


class ItemPropertyDialog(QDialog):
    def __init__(self, parent, item_properties=[], installation=None):
        QDialog.__init__(self, parent)

        self.ui = item_property_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.properties = k2_properties if installation is None or installation.is_tsl() else k1_properties

        for i in range(len(self.properties)):
            self.ui.property_combo.addItem(self.properties[i]["name"])

        self.ui.upgrade_combo.addItems(["[None]"] + Installation.get_upgrades_list(installation))

        self.ui.property_combo.currentIndexChanged.connect(self.property_changed)
        self.ui.subtype_combo.currentIndexChanged.connect(self.subtype_changed)
        self.ui.add_button.clicked.connect(self.add_property)
        self.ui.remove_button.clicked.connect(self.remove_property)
        self.ui.property_list.currentItemChanged.connect(self.property_selected)

        self.ui.save_button.clicked.connect(self.update_selected_property)

        self.ui.frame.setDisabled(True)

        self.paramtable = paramtable
        self.iprp = {
            'iprp_attribcost':  {'name': "", 'options': ['>=1', '>=2', '>=3', '>=4', '>=5', '>=6', '>=7', '>=8', '>=9', '>=10', '>=11', '>=12', '>=13', '>=14', '>=15', '>=16', '>=17', '>=18', '>=19', '>=20', '>=21', '>=22', '>=23', '>=24', '>=25']},
            'iprp_abilities':   {'name': "", 'options': ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]},
            'iprp_meleecost':   {'name': "", 'options': ['Random', '1', '2', '3', '4', '5']},
            'iprp_pc':          {'name': "", 'options': ['Player', 'Kreia', 'Atton', 'Handmaiden', 'T3-M4', 'HK-47', 'Hanharr', 'Bao_Dur', 'Mira', 'G0-T0', 'Mandalore', 'Visas_Marr', 'Remote', 'Disciple']},
            'iprp_combatdam':   {'name': "", 'options': ['Bludgeoning', 'Piercing', 'Slashing']},
            'iprp_neg5cost':    {'name': "", 'options': ['Random', 'Penalty_-1', 'Penalty_-2', 'Penalty_-3', 'Penalty_-4', 'Penalty_-5']},
            'iprp_neg10cost':   {'name': "", 'options': ['Random', 'Penalty_-1', 'Penalty_-2', 'Penalty_-3', 'Penalty_-4', 'Penalty_-5', 'Penalty_-6', 'Penalty_-7', 'Penalty_-8', 'Penalty_-9', 'Penalty_-10']},
            'iprp_base1':       {'name': "", 'options': []},
            'iprp_weightinc':   {'name': "", 'options': ['50', '100', '150', '300', '500', '1000']},
            'iprp_chargecost':  {'name': "", 'options': ['Random', 'Single_Use', '5_Charges/Use', '4_Charges/Use', '3_Charges/Use', '2_Charges/Use', '1_Charge/Use', '0_Charges/Use', '1_Use/Day', '2_Uses/Day', '3_Uses/Day', '4_Uses/Day', '5_Uses/Day', 'Unlimited_Use', '1_1_Minute', '1_2_Minute', '1_3_Minute', '1_4_Minute', '1_5_Minute']},
            'iprp_protection':  {'name': "", 'options': ['Bonus+1', 'Bonus+2', 'Bonus+3', 'Bonus+4', 'Bonus+5']},
            'iprp_soakcost':    {'name': "", 'options': ['Random', 'Soak5', 'Soak10', 'Soak15', 'Soak20', 'Soak25', 'Soak30']},
            'iprp_damvulcost':  {'name': "", 'options': ['Random', '5%', '10%', '25%', '50%', '75%', '90%', '100%']},
            'iprp_resistcost':  {'name': "", 'options': ['Random', 'Resist_5/-', 'Resist_10/-', 'Resist_15/-', 'Resist_20/-', 'Resist_25/-', 'Resist_30/-']},
            'iprp_immunity':    {'name': "", 'options': ['Backstab', 'LvL/Ab_drain', 'MindSpells', 'Poison', 'Disease', 'Fear', 'Knockdown', 'Paralysis', 'Critical_Hits', 'Death_Magic']},
            'iprp_srcost':      {'name': "", 'options': ['Bonus_10', 'Bonus_12', 'Bonus_14', 'Bonus_16', 'Bonus_18', 'Bonus_20', 'Bonus_22', 'Bonus_24', 'Bonus_26', 'Bonus_28', 'Bonus_30', 'Bonus_32']},
            'iprp_saveelement': {'name': "", 'options': ['1.25', '0.4', '0.4', '0.4', '0.75', '0.5', '0.4', '0.4', '0.4', '0.5', '0.75', '0.75', '0.5', '0.4', '0.4', '0.75', '', '', '']},
            'iprp_savingthrow': {'name': "", 'options': ['All', 'Fortitude', 'Reflex', 'Will']},
            'iprp_acmodtype':   {'name': "", 'options': ['AC_Dodge', 'AC_Natural', 'AC_Armor', 'AC_Shield', 'AC_Deflection']},
            'iprp_onhitdur':    {'name': "", 'options': ['25%', '25%', '25%', '50%', '50%', '50%', '100%', '100%', '100%']},
            'iprp_ammocost':    {'name': "", 'options': ['Random', 'Basic', '1d6Fire', '1d6Cold', '1d6Light', '', '', '', '', '', '', '1', '2', '3', '', '']},
            'iprp_monsterhit':  {'name': "", 'options': ['AbilityDrain', 'Confusion', 'Fear', 'Poison', 'Slow', 'Stun', 'Instant_Kill', 'Sleep', 'Paralyze']},
            'iprp_amount':      {'name': "", 'options': ['1', '2', '3', '4', '5']},
            'iprp_bonuscost':   {'name': "", 'options': ['Random', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
            'iprp_ammotype':    {'name': "", 'options': ['Arrow', 'Bolt', 'Bullet']},
            'iprp_walk':        {'name': "", 'options': ['Default', 'ZombieWalk']},
            'iprp_monstcost':   {'name': "", 'options': ['Random', '1d2', '1d3', '1d4', '2d4', '3d4', '4d4', '5d4', '1d6', '2d6', '3d6', '4d6', '5d6', '6d6', '7d6', '8d6', '9d6', '10d6', '1d8', '2d8', '3d8', '4d8', '5d8', '6d8', '7d8', '8d8', '9d8', '10d8', '1d10', '2d10', '3d10', '4d10', '5d10', '6d10', '7d10', '8d10', '9d10', '10d10', '1d12', '2d12', '3d12', '4d12', '5d12', '6d12', '7d12', '8d12', '9d12', '10d12', '1d20', '2d20', '3d20', '4d20', '5d20', '6d20', '7d20', '8d20', '9d20', '10d20']},
            'poison':           {'name': "", 'options': ['POISON_ABILITY_SCORE_MILD', 'POISON_ABILITY_SCORE_AVERAGE', 'POISON_ABILITY_SCORE_VIRULENT', 'POISON_DAMAGE_MILD', 'POISON_DAMAGE_AVERAGE', 'POISON_DAMAGE_VIRULENT']},
            'iprp_onhitdc':     {'name': "", 'options': ['10', '14', '18', '22', '100']},
            'iprp_onhit':       {'name': "", 'options': ['Sleep', 'Stun', 'Paralyze', 'Confusion', 'Fear', 'Slow', 'AbilityDrain', 'ItemPoison', 'SlayRG', 'SlayAG', 'Instant_Death']},
            'skills':           {'name': "", 'options': ['Computer Use', 'Demolitions', 'Stealth', 'Awareness', 'Persuade', 'Repair', 'Security', 'Treat Injury']},
        }
        if installation is None or installation.is_tsl():
            self.iprp["iprp_aligngrp"] = {'name': "", 'options': ['All', 'Neutral', 'Light_Side', 'Dark_Side', 'Dark_100%', 'Light_100%']}
            self.iprp["iprp_damagetype"] = {'name': "", 'options': ['Bludgeoning', 'Piercing', 'Slashing', 'Universal', 'Unstoppable', 'Cold', 'Light_Side', 'Electrical', 'Fire', 'Dark_Side', 'Sonic', 'Ion', 'Energy']}
            self.iprp["iprp_damagecost"] = {'name': "", 'options': ['Random', '1', '2', '3', '4', '5', '1d4', '1d6', '1d8', '1d10', '2d6', '1d12', '2d8', '2d10', '1d3']}
            self.iprp["iprp_immuncost"] = {'name': "", 'options': ['Random', '5%', '10%', '25%', '50%', '75%', '90%', '100%', '15%', '20%', '30%']}
            self.costtable = k2_costtable
        else:
            self.iprp["iprp_aligngrp"] = {'name': "", 'options': ['All', 'Neutral', 'Light_Side', 'Dark_Side']}
            self.iprp["iprp_damagetype"] = {'name': "", 'options': ['Bludgeoning', 'Piercing', 'Slashing', 'Universal', 'Acid', 'Cold', 'Light_Side', 'Electrical', 'Fire', 'Dark_Side', 'Sonic', 'Ion', 'Energy']}
            self.iprp["iprp_damagecost"] = {'name': "", 'options': ['Random', '1', '2', '3', '4', '5', '1d4', '1d6', '1d8', '1d10', '2d6']}
            self.iprp["iprp_immuncost"] = {'name': "", 'options': ['Random', '5%', '10%', '25%', '50%', '75%', '90%', '100%']}
            self.costtable = k1_costtable
        self.iprp["classes"] = {'name': "", 'options': Installation.get_class_list()}
        self.iprp["traps"] = {'name': "", 'options': Installation.get_trap_type_list()}
        self.iprp["racialtypes"] = {'name': "", 'options': ["","","","","","Droid","Human"]}
        self.iprp["spells"] = {'name': "", 'options': [i for i in Installation.get_powers_list(installation)]}
        self.iprp["appearance"] = {'name': "", 'options': Installation.get_appearance_list(installation)}
        self.iprp["feat"] = {'name': "", 'options': Installation.get_feats_list(installation)}

        self.set_item_properties(item_properties)
        self.refresh_main_combos()
        self.refresh_parameter_combos()

    def property_changed(self, index):
        self.refresh_main_combos()

    def subtype_changed(self, subtype_index):
        self.refresh_parameter_combos()

    def refresh_main_combos(self):
        index = self.ui.property_combo.currentIndex()

        subtype = self.properties[index]["subtype"]
        cost_table = self.properties[index]["cost_table"]

        self.ui.subtype_combo.clear()
        if subtype == '':
            self.ui.subtype_combo.setEnabled(False)
        else:
            self.ui.subtype_combo.setEnabled(True)
            # self.ui.subtype_label.setText(self.iprp[subtype]["name"])
            self.ui.subtype_combo.addItems(self.iprp[subtype]["options"])

        self.ui.value_combo.clear()
        if cost_table == '' or cost_table == 'iprp_base1':
            self.ui.value_combo.setEnabled(False)
        else:
            self.ui.value_combo.setEnabled(True)
            # self.ui.value_label.setText(self.iprp[cost_table]["name"])
            self.ui.value_combo.addItems(self.iprp[cost_table]["options"])

    def refresh_parameter_combos(self):
        self.ui.parameter_a_combo.clear()
        self.ui.parameter_b_combo.clear()

        property_index = self.ui.property_combo.currentIndex()
        subtype_index = self.ui.subtype_combo.currentIndex()

        param_a = ""
        param_b = ""

        try:
            param_a = self.properties[property_index]["param1"][subtype_index].lower()
            param_b = self.properties[property_index]["param2"][subtype_index].lower()
        except:
            pass

        self.ui.parameter_a_combo.clear()
        if param_a == '':
            self.ui.parameter_a_combo.setEnabled(False)
        else:
            self.ui.parameter_a_combo.setEnabled(True)
            # self.ui.parameter_a_label.setText(self.iprp[param_a]["name"])
            self.ui.parameter_a_combo.addItems(self.iprp[param_a]["options"])

        self.ui.parameter_b_combo.clear()
        if param_b == '':
            self.ui.parameter_b_combo.setEnabled(False)
        else:
            self.ui.parameter_b_combo.setEnabled(True)
            # self.ui.parameter_b_label.setText(self.iprp[param_b]["name"])
            self.ui.parameter_b_combo.addItems(self.iprp[param_b]["options"])

    def add_property(self):
        item = QListWidgetItem("Attribute Bonus")
        item.property = ItemProperty()
        self.ui.property_list.addItem(item)

    def remove_property(self):
        if len(self.ui.property_list.selectedItems()) != 0:
            self.ui.property_list.takeItem(self.ui.property_list.currentRow())

        if self.ui.property_list.count() == 0:
            self.ui.frame.setDisabled(True)

    def property_selected(self, item):
        if item is not None:
            self.ui.frame.setDisabled(False)
            item_property = item.property

            self.ui.property_combo.setCurrentIndex(item_property.type_value)
            self.ui.subtype_combo.setCurrentIndex(item_property.subtype_value)
            self.ui.value_combo.setCurrentIndex(item_property.cost_value)
            self.ui.parameter_a_combo.setCurrentIndex(item_property.param1_value)
            self.ui.parameter_b_combo.setCurrentIndex(item_property.param2_value)
            self.ui.upgrade_combo.setCurrentIndex(item_property.upgrade_value+1)
        else:
            self.ui.frame.setDisabled(True)

    def update_selected_property(self):
        item = self.ui.property_list.item(self.ui.property_list.currentRow())
        property = item.property
        property.type_value = self.ui.property_combo.currentIndex()
        property.subtype_value = self.ui.subtype_combo.currentIndex()
        property.cost_value = self.ui.value_combo.currentIndex()
        property.param1_value = self.ui.parameter_a_combo.currentIndex()
        property.param2_value = self.ui.parameter_b_combo.currentIndex()
        property.upgrade_value = self.ui.upgrade_combo.currentIndex()-1
        item.setText(self.ui.property_combo.currentText())

        property.cost_table = -1
        property.param1_table = -1
        property.param2_table = -2

        try: property.cost_table = self.costtable[self.properties[property.type_value]["cost_table"].lower()]
        except: pass

        try: property.param1_table = self.paramtable[self.properties[property.type_value]['param1'][property.subtype_value].lower()]
        except: pass

        try: property.param1_table = self.paramtable[self.properties[property.type_value]['param2'][property.subtype_value].lower()]
        except: pass

    def get_item_properties(self):
        properties = []
        for i in range(self.ui.property_list.count()):
            properties.append(self.ui.property_list.item(i).property)
        return properties

    def set_item_properties(self, properties):
        for property in properties:
            item = QListWidgetItem("Attribute Bonus")
            item.property = property
            item.setText(self.properties[property.type_value]['name'])
            self.ui.property_list.addItem(item)


class ItemProperty:
    def __init__(self):
        self.type_value = 0
        self.subtype_value = 0
        self.cost_table = 0
        self.cost_value = -1
        self.param1_table = -1
        self.param1_value = -1
        self.param2_table = -1
        self.param2_value = -1
        self.upgrade_value = -1


k1_properties = [{'name': 'Attribute Bonus', 'subtype': 'iprp_abilities', 'cost_table': 'iprp_bonuscost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Defense Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Defense Bonus vs Alignment Group', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Defense Bonus vs Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_meleecost', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Defense Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Enhancement Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Enhancement Bonus vs Alignment Group', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Enhancement Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attack Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Bonus Feat', 'subtype': 'feat', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Activate Item', 'subtype': 'spells', 'cost_table': 'iprp_chargecost', 'param1': [], 'param2': []}, {'name': 'Damage Bonus', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_damagecost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Bonus vs Alignment Group', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_damagecost', 'param1': ['iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype'], 'param2': ['', '', '', '']}, {'name': 'Damage Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_damagecost', 'param1': [], 'param2': []}, {'name': 'Damage Immunity', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_immuncost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Damage Reduction', 'subtype': 'iprp_protection', 'cost_table': 'iprp_soakcost', 'param1': ['', '', '', '', ''], 'param2': ['', '', '', '', '']}, {'name': 'Damage Resistance', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_resistcost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Vulnerability', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_damvulcost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Decreased Attribute Score', 'subtype': 'iprp_abilities', 'cost_table': 'iprp_neg10cost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Decreased DB', 'subtype': 'iprp_acmodtype', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', '', ''], 'param2': ['', '', '', '', '']}, {'name': 'Decreased Skill Modifier', 'subtype': 'skills', 'cost_table': 'iprp_neg10cost', 'param1': ['', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '']}, {'name': 'Extra Melee Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_base1', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Extra Ranged Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_base1', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Immunity', 'subtype': 'iprp_immunity', 'cost_table': 'iprp_base1', 'param1': ['', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '']}, {'name': 'Improved Force Resistance', 'subtype': '', 'cost_table': 'iprp_srcost', 'param1': [], 'param2': []}, {'name': 'Improved Saving Throws', 'subtype': 'iprp_saveelement', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Improved Saving Throws: Specific', 'subtype': 'iprp_savingthrow', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Keen', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Light', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Mighty', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'No Damage', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'On Hit Properties', 'subtype': 'iprp_onhit', 'cost_table': 'iprp_onhitdc', 'param1': ['IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ABILITIES', 'POISON', 'racialtypes', 'IPRP_ALIGNGRP', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Reduced Saving Throws', 'subtype': 'iprp_saveelement', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Reduced Saving Throws: Specific', 'subtype': 'iprp_savingthrow', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Regeneration', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Skill Bonus', 'subtype': 'skills', 'cost_table': 'iprp_bonuscost', 'param1': ['', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '']}, {'name': 'Security Spike', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Attack Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attack Bonus vs Alignment Group', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Attack Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'To Hit Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Unlimited Ammunition', 'subtype': 'iprp_ammotype', 'cost_table': 'iprp_ammocost', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Alignment Limitation', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_base1', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Class Limitation', 'subtype': 'classes', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'User Limitation', 'subtype': 'racialtypes', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Trap', 'subtype': 'traps', 'cost_table': '', 'param1': [], 'param2': []}, {'name': 'Stealth Field Nullifier', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'On Monster Hit', 'subtype': 'iprp_monsterhit', 'cost_table': 'iprp_base1', 'param1': ['IPRP_ABILITIES', '', '', 'poison', '', '', '', '', ''], 'param2': ['IPRP_AMOUNT', '', '', '', '', '', '', '', '']}, {'name': 'Massive Criticals', 'subtype': '', 'cost_table': 'iprp_damagecost', 'param1': [], 'param2': []}, {'name': 'Freedom of Movement', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Monster Damage', 'subtype': '', 'cost_table': 'iprp_monstcost', 'param1': [], 'param2': []}, {'name': 'Special Walk', 'subtype': 'iprp_walk', 'cost_table': 'iprp_base1', 'param1': ['', ''], 'param2': ['', '']}, {'name': 'Computer Spike', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Regeneration Force Points', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Blaster Bolt Deflection: Increase', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Blaster Bolt Deflection: Decrease', 'subtype': '', 'cost_table': 'iprp_neg10cost', 'param1': [], 'param2': []}, {'name': 'Feat Required', 'subtype': 'feat', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Droid Repair Kit', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Disguise', 'subtype': 'appearance', 'cost_table': '', 'param1': [], 'param2': []}]
k2_properties = [{'name': 'Attribute Bonus', 'subtype': 'iprp_abilities', 'cost_table': 'iprp_bonuscost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Defense Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Defense Bonus vs. Alignment', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Defense Bonus vs. Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_meleecost', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Defense Bonus vs. Type', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Enhancement Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Enhancement Bonus vs. Alignment', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Enhancement Bonus vs. Type', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attack Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Bonus Feat', 'subtype': 'feat', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Activate Item', 'subtype': 'spells', 'cost_table': 'iprp_chargecost', 'param1': [], 'param2': []}, {'name': 'Damage Bonus', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_damagecost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Bonus vs. Alignment', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_damagecost', 'param1': ['iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype', 'iprp_damagetype'], 'param2': ['', '', '', '', '', '']}, {'name': 'Damage Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_damagecost', 'param1': [], 'param2': []}, {'name': 'Damage Immunity', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_immuncost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Damage Reduction', 'subtype': 'iprp_protection', 'cost_table': 'iprp_soakcost', 'param1': ['', '', '', '', ''], 'param2': ['', '', '', '', '']}, {'name': 'Damage Resistance', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_resistcost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Damage Vulnerability', 'subtype': 'iprp_damagetype', 'cost_table': 'iprp_damvulcost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Attribute Penalty', 'subtype': 'iprp_abilities', 'cost_table': 'iprp_neg10cost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Defense Penalty', 'subtype': 'iprp_acmodtype', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', '', ''], 'param2': ['', '', '', '', '']}, {'name': 'Decreased Skill Modifier', 'subtype': 'skills', 'cost_table': 'iprp_neg10cost', 'param1': ['', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '']}, {'name': 'Extra Melee Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_base1', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Extra Ranged Damage Type', 'subtype': 'iprp_combatdam', 'cost_table': 'iprp_base1', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Immunity', 'subtype': 'iprp_immunity', 'cost_table': 'iprp_base1', 'param1': ['', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '']}, {'name': 'Improved Force Resistance', 'subtype': '', 'cost_table': 'iprp_srcost', 'param1': [], 'param2': []}, {'name': 'Improved Saving Throws: Damage Type', 'subtype': 'iprp_saveelement', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Improved Saving Throws', 'subtype': 'iprp_savingthrow', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Keen', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Light', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Mighty', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'No Damage', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'On Hit', 'subtype': 'iprp_onhit', 'cost_table': 'iprp_onhitdc', 'param1': ['IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ONHITDUR', 'IPRP_ABILITIES', 'POISON', 'racialtypes', 'IPRP_ALIGNGRP', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Reduced Saving Throws: Damage Type', 'subtype': 'iprp_saveelement', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Reduced Saving Throws', 'subtype': 'iprp_savingthrow', 'cost_table': 'iprp_neg5cost', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'Regeneration', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Skill Bonus', 'subtype': 'skills', 'cost_table': 'iprp_bonuscost', 'param1': ['', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '']}, {'name': 'Security Spike', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Attack Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attack Bonus vs Alignment Group', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_meleecost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Attack Bonus vs Racial Group', 'subtype': 'racialtypes', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attack Penalty', 'subtype': '', 'cost_table': 'iprp_neg5cost', 'param1': [], 'param2': []}, {'name': 'Unlimited Ammunition', 'subtype': 'iprp_ammotype', 'cost_table': 'iprp_ammocost', 'param1': ['', '', ''], 'param2': ['', '', '']}, {'name': 'Alignment Limitation', 'subtype': 'iprp_aligngrp', 'cost_table': 'iprp_base1', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}, {'name': 'Class Limitation', 'subtype': 'classes', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'User Limitation', 'subtype': 'racialtypes', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Trap', 'subtype': 'traps', 'cost_table': '', 'param1': [], 'param2': []}, {'name': 'Stealth Field Nullifier', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'On Monster Hit', 'subtype': 'iprp_monsterhit', 'cost_table': 'iprp_base1', 'param1': ['IPRP_ABILITIES', '', '', 'poison', '', '', '', '', ''], 'param2': ['IPRP_AMOUNT', '', '', '', '', '', '', '', '']}, {'name': 'Massive Criticals', 'subtype': '', 'cost_table': 'iprp_damagecost', 'param1': [], 'param2': []}, {'name': 'Freedom of Movement', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Monster Damage', 'subtype': '', 'cost_table': 'iprp_monstcost', 'param1': [], 'param2': []}, {'name': 'Special Walk', 'subtype': 'iprp_walk', 'cost_table': 'iprp_base1', 'param1': ['', ''], 'param2': ['', '']}, {'name': 'Computer Spike', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Regenerate Force Points', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Blaster Bolt Deflection: Increase', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Blaster Bolt Deflection: Decrease', 'subtype': '', 'cost_table': 'iprp_neg10cost', 'param1': [], 'param2': []}, {'name': 'Feat Required', 'subtype': 'feat', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Droid Repair Kit', 'subtype': '', 'cost_table': 'iprp_bonuscost', 'param1': [], 'param2': []}, {'name': 'Disguise', 'subtype': 'appearance', 'cost_table': '', 'param1': [], 'param2': []}, {'name': 'Gender Restriction', 'subtype': 'gender', 'cost_table': 'iprp_base1', 'param1': ['', '', '', '', ''], 'param2': ['', '', '', '', '']}, {'name': 'Subrace Restriction', 'subtype': 'subrace', 'cost_table': 'iprp_base1', 'param1': ['', '', '', ''], 'param2': ['', '', '', '']}, {'name': 'PC Restriction', 'subtype': 'iprp_pc', 'cost_table': 'iprp_base1', 'param1': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''], 'param2': ['', '', '', '', '', '', '', '', '', '', '', '', '', '']}, {'name': 'Dampen Sound', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Door Cutting', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Door Sabering', 'subtype': '', 'cost_table': 'iprp_base1', 'param1': [], 'param2': []}, {'name': 'Sniper Shot Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Rapid Shot Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Max DEX Bonus', 'subtype': '', 'cost_table': 'iprp_meleecost', 'param1': [], 'param2': []}, {'name': 'Attribute Restriction', 'subtype': 'iprp_abilities', 'cost_table': 'iprp_attribcost', 'param1': ['', '', '', '', '', ''], 'param2': ['', '', '', '', '', '']}]
k1_costtable = {'iprp_base1': 0, 'iprp_bonuscost': 1, 'iprp_meleecost': 2, 'iprp_chargecost': 3, 'iprp_damagecost': 4, 'iprp_immuncost': 5, 'iprp_soakcost': 6, 'iprp_resistcost': 7, 'iprp_bladecost': 8, 'iprp_slotscost': 9, 'iprp_weightcost': 10, 'iprp_srcost': 11, 'iprp_staminacost': 12, 'iprp_spelllvcost': 13, 'iprp_ammocost': 14, 'iprp_redcost': 15, 'iprp_spellcost': 16, 'iprp_trapcost': 17, 'iprp_lightcost': 18, 'iprp_monstcost': 19, 'iprp_neg5cost': 20, 'iprp_neg10cost': 21, 'iprp_damvulcost': 22, 'iprp_spelllvlimm': 23, 'iprp_onhitcost': 24, 'iprp_onhitdc': 25}
k2_costtable = {'iprp_base1': 0, 'iprp_bonuscost': 1, 'iprp_meleecost': 2, 'iprp_chargecost': 3, 'iprp_damagecost': 4, 'iprp_immuncost': 5, 'iprp_soakcost': 6, 'iprp_resistcost': 7, 'iprp_bladecost': 8, 'iprp_slotscost': 9, 'iprp_weightcost': 10, 'iprp_srcost': 11, 'iprp_staminacost': 12, 'iprp_spelllvcost': 13, 'iprp_ammocost': 14, 'iprp_redcost': 15, 'iprp_spellcost': 16, 'iprp_trapcost': 17, 'iprp_lightcost': 18, 'iprp_monstcost': 19, 'iprp_neg5cost': 20, 'iprp_neg10cost': 21, 'iprp_damvulcost': 22, 'iprp_spelllvlimm': 23, 'iprp_onhitcost': 24, 'iprp_onhitdc': 25, 'iprp_attribcost': 26}
paramtable = {'iprp_damagetype': 0, 'iprp_onhitdur': 1, 'iprp_abilities': 2, 'iprp_aligngrp': 3, 'iprp_alignment': 4, 'racialtypes': 5, 'disease': 6, 'iprp_amount': 7, 'poison': 10, 'iprp_color': 9, 'iprp_weightinc': 11}

