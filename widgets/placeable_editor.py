from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QFontInfo, QFontMetrics
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider, QTreeWidgetItem, \
    QPlainTextEdit, QFrame, QSizePolicy, QLabel

from pykotor.formats.gff import List, GFF, FieldType, Struct
from pykotor.formats.mdl import MDL

from installation import Installation
from pykotor.formats.twoda import TwoDA
from pykotor.globals import resource_types
from ui import placeable_editor
from widgets.editor_widget import EditorWidget
from widgets.inventory_dialog import InventoryDialog, Inventory, InventoryItem
from widgets.model_renderer import ModelRenderer, Object
from widgets.tree_editor import AbstractTreeEditor


class PlaceableEditor(AbstractTreeEditor, EditorWidget):
    def __init__(self, parent, utw=GFF(), file_path="", res_ref="untitled"):
        self.inventory = Inventory()

        EditorWidget.__init__(self, parent, placeable_editor, "placeable")
        self.load(utw)
        self.setup(file_path, res_ref, resource_types['uti'])
        self.init_tree()

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        inventory_button = QPushButton("...")
        inventory_button.setFixedHeight(17)
        inventory_button.clicked.connect(self.open_inventory_dialog)
        self.ui.tree.setItemWidget(self.ui.tree.findItems("Inventory", QtCore.Qt.MatchExactly)[0], 1, inventory_button)

        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Dialog")
        self.init_combo_box("Basic", "Body Bag", items=Installation.get_bodybag_list())

        self.init_localized_string_nodes("Name")

        self.init_combo_box("Advanced", "State", items=["Default", "Opened", "Closed", "Dead", "Activated", "Deactivated"])
        self.init_combo_box("Advanced", "Faction", items=Installation.get_faction_list())

        self.init_spin_box("Other", "Fortitude")
        self.init_spin_box("Other", "Reflex")
        self.init_spin_box("Other", "Will")
        self.init_spin_box("Other", "Health")
        self.init_spin_box("Other", "Hardness")

        self.init_check_box("Flags", "Plot")
        self.init_check_box("Flags", "Interactable")
        self.init_check_box("Flags", "Interruptable")
        self.init_check_box("Flags", "Invincible")
        self.init_check_box("Flags", "Static")
        self.init_check_box("Flags", "Party Useable")
        self.init_check_box("Flags", "Has Inventory")

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Used")
        self.init_line_edit("Scripts", "Opened")
        self.init_line_edit("Scripts", "Closed")
        self.init_line_edit("Scripts", "Unlocked")
        self.init_line_edit("Scripts", "Locked")
        self.init_line_edit("Scripts", "After Talking")
        self.init_line_edit("Scripts", "Inventory Accessed")
        self.init_line_edit("Scripts", "Attacked Physically")
        self.init_line_edit("Scripts", "Attacked Ability")
        self.init_line_edit("Scripts", "Damaged")
        self.init_line_edit("Scripts", "Death")
        self.init_line_edit("Scripts", "Disarmed")
        self.init_line_edit("Scripts", "Triggered")
        self.init_line_edit("Scripts", "Custom")

        self.init_check_box("Trap", "Is Trap")
        self.init_check_box("Trap", "One-Shot")
        self.init_check_box("Trap", "Detectable")
        self.init_check_box("Trap", "Disarmable")
        self.init_spin_box("Trap", "Detection DC")
        self.init_spin_box("Trap", "Disarm DC")
        self.init_combo_box("Trap", "Trap Type", items=Installation.get_trap_type_list())

        self.init_check_box("Lock", "Is Locked")
        self.init_check_box("Lock", "Lockable")
        self.init_check_box("Lock", "Requires Key")
        self.init_check_box("Lock", "Remove Key")
        self.init_line_edit("Lock", "Key Tag")
        self.init_spin_box("Lock", "Unlock DC")
        self.init_spin_box("Lock", "Lock DC")

        if self.installation is None:
            self.init_spin_box("Basic", "Appearance")
        else:
            self.init_combo_box("Basic", "Appearance", items=Installation.get_placeable_list(self.installation))
            self.get_node_widget("Basic", "Appearance").currentIndexChanged.connect(self.appearance_changed)

    def open_inventory_dialog(self):
        dialog = InventoryDialog(self, self.inventory, "placeable", self.installation)
        dialog.exec_()
        self.inventory = dialog.get_inventory()

    def appearance_changed(self, index):
        try:
            placeables_data = TwoDA.from_data(self.installation.chitin.fetch_resource("placeables", "2da"))
            model_name = placeables_data.get_cell("modelname", index).lower()
            mdl_data = self.installation.chitin.fetch_resource(model_name, "mdl")
            mdx_data = self.installation.chitin.fetch_resource(model_name, "mdx")
            model = MDL.from_data(mdl_data, mdx_data)
            self.model_renderer.model_buffer[model_name] = model
            self.model_renderer.objects.clear()
            self.model_renderer.objects.append(Object(model_name))
        except Exception as e:
            print("Failed to load door appearance model:", e)

    def load(self, utp):
        self.set_node_data("Basic", "Template", utp.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Script Tag", utp.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Dialog", utp.find_field_data("Conversation", default=""))
        self.set_node_data("Basic", "Body Bag", utp.find_field_data("BodyBag", default=0))
        self.set_node_data("Basic", "Appearance", utp.find_field_data("Appearance", default=0))

        self.set_localized_string_nodes("Name", utp.find_field_data("LocName"))

        self.set_node_data("Advanced", "State", utp.find_field_data("AnimationState", default=0))
        self.set_node_data("Advanced", "Faction", utp.find_field_data("Faction", default=0))

        self.set_node_data("Other", "Fortitude", utp.find_field_data("Fort", default=0))
        self.set_node_data("Other", "Reflex", utp.find_field_data("Ref", default=0))
        self.set_node_data("Other", "Will", utp.find_field_data("Will", default=0))
        self.set_node_data("Other", "Hardness", utp.find_field_data("Hardness", default=0))
        self.set_node_data("Other", "Health", utp.find_field_data("HP", default=0))

        self.set_node_data("Flags", "Plot", utp.find_field_data("Plot", default=0))
        self.set_node_data("Flags", "Interactable", utp.find_field_data("Useable", default=0))
        self.set_node_data("Flags", "Interruptable", utp.find_field_data("Interruptable", default=0))
        self.set_node_data("Flags", "Invincible", utp.find_field_data("Min1HP", default=0))
        self.set_node_data("Flags", "Static", utp.find_field_data("Static", default=0))
        self.set_node_data("Flags", "Party Useable", utp.find_field_data("PartyInteract", default=0))
        self.set_node_data("Flags", "Has Inventory", utp.find_field_data("HasInventory", default=0))

        self.set_node_data("Scripts", "Routine", utp.find_field_data("OnHeartbeat", default=""))
        self.set_node_data("Scripts", "Used", utp.find_field_data("OnUsed", default=""))
        self.set_node_data("Scripts", "Opened", utp.find_field_data("OnOpen", default=""))
        self.set_node_data("Scripts", "Closed", utp.find_field_data("OnClosed", default=""))
        self.set_node_data("Scripts", "Unlocked", utp.find_field_data("OnUnlock", default=""))
        self.set_node_data("Scripts", "Locked", utp.find_field_data("OnLock", default=""))
        self.set_node_data("Scripts", "After Talking", utp.find_field_data("OnEndDialogue", default=""))
        self.set_node_data("Scripts", "Inventory Accessed", utp.find_field_data("OnInvDisturbed", default=""))
        self.set_node_data("Scripts", "Attacked Physically", utp.find_field_data("OnMeleeAttacked", default=""))
        self.set_node_data("Scripts", "Attacked Ability", utp.find_field_data("OnSpellCastAt", default=""))
        self.set_node_data("Scripts", "Damaged", utp.find_field_data("OnDamaged", default=""))
        self.set_node_data("Scripts", "Death", utp.find_field_data("OnDeath", default=""))
        self.set_node_data("Scripts", "Disarmed", utp.find_field_data("OnDisarm", default=""))
        self.set_node_data("Scripts", "Triggered", utp.find_field_data("OnTrapTriggered", default=""))
        self.set_node_data("Scripts", "Custom", utp.find_field_data("OnUserDefined", default=""))

        self.set_node_data("Trap", "Is Trap", utp.find_field_data("TrapFlag", default=""))
        self.set_node_data("Trap", "One-Shot", utp.find_field_data("TrapOneShot", default=""))
        self.set_node_data("Trap", "Detectable", utp.find_field_data("TrapDetectable", default=""))
        self.set_node_data("Trap", "Disarmable", utp.find_field_data("TrapDisarmable", default=""))
        self.set_node_data("Trap", "Detection DC", utp.find_field_data("TrapDetectDC", default=""))
        self.set_node_data("Trap", "Disarm DC", utp.find_field_data("DisarmDC", default=""))
        self.set_node_data("Trap", "Trap Type", utp.find_field_data("TrapType", default=""))

        self.set_node_data("Lock", "Is Locked", utp.find_field_data("Locked", default=""))
        self.set_node_data("Lock", "Lockable", utp.find_field_data("Lockable", default=""))
        self.set_node_data("Lock", "Requires Key", utp.find_field_data("KeyRequired", default=""))
        self.set_node_data("Lock", "Remove Key", utp.find_field_data("AutoRemoveKey", default=""))
        self.set_node_data("Lock", "Key Tag", utp.find_field_data("KeyName", default=""))
        self.set_node_data("Lock", "Unlock DC", utp.find_field_data("OpenLockDC", default=""))
        self.set_node_data("Lock", "Lock DC", utp.find_field_data("CloseLockDC", default=""))

        for i in range(len(utp.find_field_data("ItemList", default=List([])).structs)):
            item_resref = utp.find_field_data("ItemList", i, "InventoryRes", default="")
            if item_resref != "": self.inventory.items.append(InventoryItem(item_resref, True))

        utp = self.build()

    def build(self):
        utp = GFF()

        utp.root.add_field(FieldType.String, "Tag",             self.get_node_data("Basic", "Script Tag"))
        utp.root.add_field(FieldType.ResRef, "TemplateResRef",  self.get_node_data("Basic", "Template"))
        utp.root.add_field(FieldType.UInt16, "Appearance",      self.get_node_data("Basic", "Appearance"))
        utp.root.add_field(FieldType.UInt8, "BodyBag",          self.get_node_data("Basic", "Body Bag"))
        utp.root.add_field(FieldType.ResRef, "Conversation",    self.get_node_data("Basic", "Dialog"))

        utp.root.add_field(FieldType.LocalizedString, "FirstName", self.get_node_localized_string("Name"))

        utp.root.add_field(FieldType.UInt8, "AnimationState",   self.get_node_data("Advanced", "State"))
        utp.root.add_field(FieldType.UInt32, "Faction",         self.get_node_data("Advanced", "Faction"))

        utp.root.add_field(FieldType.UInt8, "Fort",             self.get_node_data("Other", "Fortitude"))
        utp.root.add_field(FieldType.UInt8, "Ref",              self.get_node_data("Other", "Reflex"))
        utp.root.add_field(FieldType.UInt8, "Will",             self.get_node_data("Other", "Will"))
        utp.root.add_field(FieldType.UInt8, "Hardness",         self.get_node_data("Other", "Hardness"))
        utp.root.add_field(FieldType.Int16, "HP",               self.get_node_data("Other", "Health"))

        utp.root.add_field(FieldType.UInt8, "Plot",             self.get_node_data("Flags", "Plot"))
        utp.root.add_field(FieldType.UInt8, "Usable",           self.get_node_data("Flags", "Interactable"))
        utp.root.add_field(FieldType.UInt8, "Interruptable",    self.get_node_data("Flags", "Interruptable"))
        utp.root.add_field(FieldType.UInt8, "Min1HP",           self.get_node_data("Flags", "Invincible"))
        utp.root.add_field(FieldType.UInt8, "Static",           self.get_node_data("Flags", "Static"))
        utp.root.add_field(FieldType.UInt8, "PartyInteract",    self.get_node_data("Flags", "Party Useable"))
        utp.root.add_field(FieldType.UInt8, "HasInventory",     self.get_node_data("Flags", "Has Inventory"))

        utp.root.add_field(FieldType.ResRef, "OnHeartbeat",     self.get_node_data("Scripts", "Routine"))
        utp.root.add_field(FieldType.ResRef, "OnUsed",          self.get_node_data("Scripts", "Used"))
        utp.root.add_field(FieldType.ResRef, "OnOpen",          self.get_node_data("Scripts", "Opened"))
        utp.root.add_field(FieldType.ResRef, "OnClosed",        self.get_node_data("Scripts", "Closed"))
        utp.root.add_field(FieldType.ResRef, "OnUnlock",        self.get_node_data("Scripts", "Unlocked"))
        utp.root.add_field(FieldType.ResRef, "OnLock",          self.get_node_data("Scripts", "Locked"))
        utp.root.add_field(FieldType.ResRef, "OnEndDialogue",   self.get_node_data("Scripts", "After Talking"))
        utp.root.add_field(FieldType.ResRef, "OnInvDisturbed",  self.get_node_data("Scripts", "Inventory Accessed"))
        utp.root.add_field(FieldType.ResRef, "OnMeleeAttacked", self.get_node_data("Scripts", "Attacked Physically"))
        utp.root.add_field(FieldType.ResRef, "OnSpellCastAt",   self.get_node_data("Scripts", "Attacked Ability"))
        utp.root.add_field(FieldType.ResRef, "OnDamaged",       self.get_node_data("Scripts", "Damaged"))
        utp.root.add_field(FieldType.ResRef, "OnDeath",         self.get_node_data("Scripts", "Death"))
        utp.root.add_field(FieldType.ResRef, "OnDisarm",        self.get_node_data("Scripts", "Disarmed"))
        utp.root.add_field(FieldType.ResRef, "OnTriggered",     self.get_node_data("Scripts", "Triggered"))
        utp.root.add_field(FieldType.ResRef, "OnCustom",        self.get_node_data("Scripts", "Custom"))

        utp.root.add_field(FieldType.UInt8, "TrapFlag",       self.get_node_data("Trap", "Is Trap"))
        utp.root.add_field(FieldType.UInt8, "TrapOneShot",    self.get_node_data("Trap", "One-Shot"))
        utp.root.add_field(FieldType.UInt8, "TrapDetectable", self.get_node_data("Trap", "Detectable"))
        utp.root.add_field(FieldType.UInt8, "TrapDisarmable", self.get_node_data("Trap", "Disarmable"))
        utp.root.add_field(FieldType.UInt8, "TrapDetectDC",   self.get_node_data("Trap", "Detection DC"))
        utp.root.add_field(FieldType.UInt8, "DisarmDC",       self.get_node_data("Trap", "Disarm DC"))
        utp.root.add_field(FieldType.UInt8, "TrapType",       self.get_node_data("Trap", "Trap Type"))

        utp.root.add_field(FieldType.UInt8, "Locked",         self.get_node_data("Lock", "Is Locked"))
        utp.root.add_field(FieldType.UInt8, "Lockable",       self.get_node_data("Lock", "Lockable"))
        utp.root.add_field(FieldType.UInt8, "KeyRequired",    self.get_node_data("Lock", "Requires Key"))
        utp.root.add_field(FieldType.UInt8, "AutoRemoveKey",  self.get_node_data("Lock", "Remove Key"))
        utp.root.add_field(FieldType.String, "KeyName",       self.get_node_data("Lock", "Key Tag"))
        utp.root.add_field(FieldType.UInt8, "OpenLockDC",     self.get_node_data("Lock", "Unlock DC"))
        utp.root.add_field(FieldType.UInt8, "CloseLockDC",    self.get_node_data("Lock", "Lock DC"))

        utp_item_list = List([])
        for slot, item in enumerate(self.inventory.items):
            item_struct = Struct(slot, [])
            item_struct.add_field(FieldType.ResRef, "InventoryRes", item.res_ref)
            item_struct.add_field(FieldType.UInt16, "Repos_PosX", slot)
            item_struct.add_field(FieldType.UInt16, "Repos_PosY", 0)
            utp_item_list.structs.append(item_struct)
        utp.root.add_field(FieldType.List, "ItemList", utp_item_list)

        return utp



