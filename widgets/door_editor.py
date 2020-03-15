from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget

from installation import Installation
from pykotor.formats.gff import FieldType, GFF
from pykotor.formats.mdl import MDL
from pykotor.formats.twoda import TwoDA
from ui import door_editor
from widgets.model_renderer import ModelRenderer, Object
from widgets.tree_editor import AbstractTreeEditor


class DoorEditor(AbstractTreeEditor):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.ui = door_editor.Ui_Form()
        self.ui.setupUi(self)

        self.installation = self.window().active_installation

        if self.installation is not None:
            self.model_renderer = ModelRenderer(self)
            self.ui.splitter.addWidget(self.model_renderer)

        self.init_tree()

    def init_tree(self):
        for i in range(self.ui.tree.topLevelItemCount()):
            self.ui.tree.topLevelItem(i).setForeground(0, QBrush(QtCore.Qt.gray))

        self.init_line_edit("Basic", "Template")
        self.init_line_edit("Basic", "Script Tag")
        self.init_line_edit("Basic", "Dialog")

        self.init_localized_string_nodes("Name")

        self.init_combo_box("Advanced", "State", items=["Default", "Opened", "Closed"])
        self.init_combo_box("Advanced", "Faction", items=Installation.get_faction_list())

        self.init_spin_box("Other", "Fortitude")
        self.init_spin_box("Other", "Reflex")
        self.init_spin_box("Other", "Will")
        self.init_spin_box("Other", "Health")
        self.init_spin_box("Other", "Hardness")

        self.init_check_box("Flags", "Plot")
        self.init_check_box("Flags", "Interruptable")
        self.init_check_box("Flags", "Invincible")
        self.init_check_box("Flags", "Static")

        self.init_line_edit("Scripts", "Routine")
        self.init_line_edit("Scripts", "Clicked")
        self.init_line_edit("Scripts", "Opened")
        self.init_line_edit("Scripts", "Closed")
        self.init_line_edit("Scripts", "Unlocked")
        self.init_line_edit("Scripts", "Locked")
        self.init_line_edit("Scripts", "Failed")
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
            self.init_combo_box("Basic", "Appearance", items=Installation.get_door_list(self.installation))
            self.get_node_widget("Basic", "Appearance").currentIndexChanged.connect(self.appearance_changed)

    def appearance_changed(self, index):
        try:
            genericdoors_data = TwoDA.from_data(self.installation.chitin.fetch_resource("genericdoors", "2da"))
            model_name = genericdoors_data.get_cell("modelname", index).lower()
            mdl_data = self.installation.chitin.fetch_resource(model_name, "mdl")
            mdx_data = self.installation.chitin.fetch_resource(model_name, "mdx")
            model = MDL.from_data(mdl_data, mdx_data)
            self.model_renderer.model_buffer[model_name] = model
            self.model_renderer.objects.clear()
            self.model_renderer.objects.append(Object(model_name))
        except Exception as e:
            print("Failed to load door appearance model:", e)

    def load(self, utw):
        self.set_node_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_node_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_node_data("Basic", "Dialog", utw.find_field_data("Conversation", default=""))
        self.set_node_data("Basic", "Appearance", utw.find_field_data("GenericType", default=0))

        self.set_node_data("Advanced", "State", utw.find_field_data("AnimationState", default=0))
        self.set_node_data("Advanced", "Faction", utw.find_field_data("Faction", default=0))

        self.set_node_data("Other", "Fortitude", utw.find_field_data("Fort", default=0))
        self.set_node_data("Other", "Will", utw.find_field_data("Will", default=0))
        self.set_node_data("Other", "Reflex", utw.find_field_data("Ref", default=0))
        self.set_node_data("Other", "Health", utw.find_field_data("CurrentHP", default=0))
        self.set_node_data("Other", "Hardness", utw.find_field_data("Hardness", default=0))

        self.set_node_data("Flags", "Plot", utw.find_field_data("Plot", default=False))
        self.set_node_data("Flags", "Interruptable", utw.find_field_data("Interruptable", default=False))
        self.set_node_data("Flags", "Invincible", utw.find_field_data("Min1HP", default=False))
        self.set_node_data("Flags", "Static", utw.find_field_data("Static", default=False))

        self.set_node_data("Scripts", "Routine", utw.find_field_data("OnHeartbeat", default=""))
        self.set_node_data("Scripts", "Clicked", utw.find_field_data("OnClick", default=""))
        self.set_node_data("Scripts", "Opened", utw.find_field_data("OnOpen", default=""))
        self.set_node_data("Scripts", "Closed", utw.find_field_data("OnClosed", default=""))
        self.set_node_data("Scripts", "Unlocked", utw.find_field_data("OnUnlock", default=""))
        self.set_node_data("Scripts", "Locked", utw.find_field_data("OnLock", default=""))
        self.set_node_data("Scripts", "Failed", utw.find_field_data("OnFailToOpen", default=""))
        self.set_node_data("Scripts", "Attacked Physically", utw.find_field_data("OnMeleeAttacked", default=""))
        self.set_node_data("Scripts", "Attacked Ability", utw.find_field_data("OnSpellCastAt", default=""))
        self.set_node_data("Scripts", "Damaged", utw.find_field_data("OnDamaged", default=""))
        self.set_node_data("Scripts", "Death", utw.find_field_data("OnDeath", default=""))
        self.set_node_data("Scripts", "Disarmed", utw.find_field_data("OnDisarm", default=""))
        self.set_node_data("Scripts", "Triggered", utw.find_field_data("OnTrapTriggered", default=""))
        self.set_node_data("Scripts", "Custom", utw.find_field_data("OnUserDefined", default=""))

        self.set_node_data("Trap", "Is Trap", utw.find_field_data("TrapFlag", default=False))
        self.set_node_data("Trap", "One-Shot", utw.find_field_data("TrapOneShot", default=False))
        self.set_node_data("Trap", "Detectable", utw.find_field_data("TrapDetectable", default=False))
        self.set_node_data("Trap", "Disarmable", utw.find_field_data("TrapDisarmable", default=False))
        self.set_node_data("Trap", "Detection DC", utw.find_field_data("TrapDetectDC", default=0))
        self.set_node_data("Trap", "Disarm DC", utw.find_field_data("DisarmDC", default=0))
        self.set_node_data("Trap", "Trap Type", utw.find_field_data("TrapType", default=0))

        self.set_node_data("Lock", "Is Locked", utw.find_field_data("Locked", default=False))
        self.set_node_data("Lock", "Lockable", utw.find_field_data("Lockable", default=False))
        self.set_node_data("Lock", "Requires Key", utw.find_field_data("KeyRequired", default=False))
        self.set_node_data("Lock", "Removes Key", utw.find_field_data("AutoRemoveKey", default=False))
        self.set_node_data("Lock", "Key Tag", utw.find_field_data("KeyName", default=""))
        self.set_node_data("Lock", "Lock DC", utw.find_field_data("CloseLockDC", default=0))
        self.set_node_data("Lock", "Unlock DC", utw.find_field_data("OpenLockDC", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocName"))

    def build(self):
        utd = GFF()

        utd.root.add_field(FieldType.String, "Tag",             self.get_node_data("Basic", "Script Tag"))
        utd.root.add_field(FieldType.ResRef, "TemplateResRef",  self.get_node_data("Basic", "Template"))
        utd.root.add_field(FieldType.UInt16, "Appearance",      self.get_node_data("Basic", "Appearance"))
        utd.root.add_field(FieldType.ResRef, "Conversation",    self.get_node_data("Basic", "Dialog"))

        utd.root.add_field(FieldType.LocalizedString, "LocName", self.get_node_localized_string("Name"))

        utd.root.add_field(FieldType.UInt8, "AnimationState",   self.get_node_data("Advanced", "State"))
        utd.root.add_field(FieldType.UInt32, "Faction",         self.get_node_data("Advanced", "Faction"))

        utd.root.add_field(FieldType.UInt8, "Fort",             self.get_node_data("Other", "Fortitude"))
        utd.root.add_field(FieldType.UInt8, "Ref",              self.get_node_data("Other", "Reflex"))
        utd.root.add_field(FieldType.UInt8, "Will",             self.get_node_data("Other", "Will"))
        utd.root.add_field(FieldType.UInt8, "Hardness",         self.get_node_data("Other", "Hardness"))
        utd.root.add_field(FieldType.Int16, "HP",               self.get_node_data("Other", "Health"))

        utd.root.add_field(FieldType.UInt8, "Plot",             self.get_node_data("Flags", "Plot"))
        utd.root.add_field(FieldType.UInt8, "Interruptable",    self.get_node_data("Flags", "Interruptable"))
        utd.root.add_field(FieldType.UInt8, "Min1HP",           self.get_node_data("Flags", "Invincible"))
        utd.root.add_field(FieldType.UInt8, "Static",           self.get_node_data("Flags", "Static"))

        utd.root.add_field(FieldType.ResRef, "OnHeartbeat",     self.get_node_data("Scripts", "Routine"))
        utd.root.add_field(FieldType.ResRef, "OnClick",         self.get_node_data("Scripts", "Clicked"))
        utd.root.add_field(FieldType.ResRef, "OnOpen",          self.get_node_data("Scripts", "Opened"))
        utd.root.add_field(FieldType.ResRef, "OnClosed",        self.get_node_data("Scripts", "Closed"))
        utd.root.add_field(FieldType.ResRef, "OnUnlock",        self.get_node_data("Scripts", "Unlocked"))
        utd.root.add_field(FieldType.ResRef, "OnLock",          self.get_node_data("Scripts", "Locked"))
        utd.root.add_field(FieldType.ResRef, "OnFailToOpen",    self.get_node_data("Scripts", "Failed"))
        utd.root.add_field(FieldType.ResRef, "OnMeleeAttacked", self.get_node_data("Scripts", "Attacked Physically"))
        utd.root.add_field(FieldType.ResRef, "OnSpellCastAt",   self.get_node_data("Scripts", "Attacked Ability"))
        utd.root.add_field(FieldType.ResRef, "OnDamaged",       self.get_node_data("Scripts", "Damaged"))
        utd.root.add_field(FieldType.ResRef, "OnDeath",         self.get_node_data("Scripts", "Death"))
        utd.root.add_field(FieldType.ResRef, "OnDisarm",        self.get_node_data("Scripts", "Disarmed"))
        utd.root.add_field(FieldType.ResRef, "OnTriggered",     self.get_node_data("Scripts", "Triggered"))
        utd.root.add_field(FieldType.ResRef, "OnCustom",        self.get_node_data("Scripts", "Custom"))

        utd.root.add_field(FieldType.UInt8, "TrapFlag",         self.get_node_data("Trap", "Is Trap"))
        utd.root.add_field(FieldType.UInt8, "TrapOneShot",      self.get_node_data("Trap", "One-Shot"))
        utd.root.add_field(FieldType.UInt8, "TrapDetectable",   self.get_node_data("Trap", "Detectable"))
        utd.root.add_field(FieldType.UInt8, "TrapDisarmable",   self.get_node_data("Trap", "Disarmable"))
        utd.root.add_field(FieldType.UInt8, "TrapDetectDC",     self.get_node_data("Trap", "Detection DC"))
        utd.root.add_field(FieldType.UInt8, "DisarmDC",         self.get_node_data("Trap", "Disarm DC"))
        utd.root.add_field(FieldType.UInt8, "TrapType",         self.get_node_data("Trap", "Trap Type"))

        utd.root.add_field(FieldType.UInt8, "Locked",           self.get_node_data("Lock", "Is Locked"))
        utd.root.add_field(FieldType.UInt8, "Lockable",         self.get_node_data("Lock", "Lockable"))
        utd.root.add_field(FieldType.UInt8, "KeyRequired",      self.get_node_data("Lock", "Requires Key"))
        utd.root.add_field(FieldType.UInt8, "AutoRemoveKey",    self.get_node_data("Lock", "Remove Key"))
        utd.root.add_field(FieldType.String, "KeyName",         self.get_node_data("Lock", "Key Tag"))
        utd.root.add_field(FieldType.UInt8, "OpenLockDC",       self.get_node_data("Lock", "Unlock DC"))
        utd.root.add_field(FieldType.UInt8, "CloseLockDC",      self.get_node_data("Lock", "Lock DC"))

        return utd
