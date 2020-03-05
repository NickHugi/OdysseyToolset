from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget

from installation import Installation
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
        self.set_note_data("Basic", "Script Tag", utw.find_field_data("Tag", default=""))
        self.set_note_data("Basic", "Template", utw.find_field_data("TemplateResRef", default=""))
        self.set_note_data("Basic", "Dialog", utw.find_field_data("Conversation", default=""))
        self.set_note_data("Basic", "Appearance", utw.find_field_data("GenericType", default=0))

        self.set_note_data("Advanced", "State", utw.find_field_data("AnimationState", default=0))
        self.set_note_data("Advanced", "Faction", utw.find_field_data("Faction", default=0))

        self.set_note_data("Other", "Fortitude", utw.find_field_data("Fort", default=0))
        self.set_note_data("Other", "Will", utw.find_field_data("Will", default=0))
        self.set_note_data("Other", "Reflex", utw.find_field_data("Ref", default=0))
        self.set_note_data("Other", "Health", utw.find_field_data("CurrentHP", default=0))
        self.set_note_data("Other", "Hardness", utw.find_field_data("Hardness", default=0))

        self.set_note_data("Flags", "Plot", utw.find_field_data("Plot", default=False))
        self.set_note_data("Flags", "Interruptable", utw.find_field_data("Interruptable", default=False))
        self.set_note_data("Flags", "Invincible", utw.find_field_data("Min1HP", default=False))
        self.set_note_data("Flags", "Static", utw.find_field_data("Static", default=False))

        self.set_note_data("Scripts", "Routine", utw.find_field_data("OnHeartbeat", default=""))
        self.set_note_data("Scripts", "Clicked", utw.find_field_data("OnClick", default=""))
        self.set_note_data("Scripts", "Opened", utw.find_field_data("OnOpen", default=""))
        self.set_note_data("Scripts", "Closed", utw.find_field_data("OnClosed", default=""))
        self.set_note_data("Scripts", "Unlocked", utw.find_field_data("OnUnlock", default=""))
        self.set_note_data("Scripts", "Locked", utw.find_field_data("OnLock", default=""))
        self.set_note_data("Scripts", "Failed", utw.find_field_data("OnFailToOpen", default=""))
        self.set_note_data("Scripts", "Attacked Physically", utw.find_field_data("OnMeleeAttacked", default=""))
        self.set_note_data("Scripts", "Attacked Ability", utw.find_field_data("OnSpellCastAt", default=""))
        self.set_note_data("Scripts", "Damaged", utw.find_field_data("OnDamaged", default=""))
        self.set_note_data("Scripts", "Death", utw.find_field_data("OnDeath", default=""))
        self.set_note_data("Scripts", "Disarmed", utw.find_field_data("OnDisarm", default=""))
        self.set_note_data("Scripts", "Triggered", utw.find_field_data("OnTrapTriggered", default=""))
        self.set_note_data("Scripts", "Custom", utw.find_field_data("OnUserDefined", default=""))

        self.set_note_data("Trap", "Is Trap", utw.find_field_data("TrapFlag", default=False))
        self.set_note_data("Trap", "One-Shot", utw.find_field_data("TrapOneShot", default=False))
        self.set_note_data("Trap", "Detectable", utw.find_field_data("TrapDetectable", default=False))
        self.set_note_data("Trap", "Disarmable", utw.find_field_data("TrapDisarmable", default=False))
        self.set_note_data("Trap", "Detection DC", utw.find_field_data("TrapDetectDC", default=0))
        self.set_note_data("Trap", "Disarm DC", utw.find_field_data("DisarmDC", default=0))
        self.set_note_data("Trap", "Trap Type", utw.find_field_data("TrapType", default=0))

        self.set_note_data("Lock", "Is Locked", utw.find_field_data("Locked", default=False))
        self.set_note_data("Lock", "Lockable", utw.find_field_data("Lockable", default=False))
        self.set_note_data("Lock", "Requires Key", utw.find_field_data("KeyRequired", default=False))
        self.set_note_data("Lock", "Removes Key", utw.find_field_data("AutoRemoveKey", default=False))
        self.set_note_data("Lock", "Key Tag", utw.find_field_data("KeyName", default=""))
        self.set_note_data("Lock", "Lock DC", utw.find_field_data("CloseLockDC", default=0))
        self.set_note_data("Lock", "Unlock DC", utw.find_field_data("OpenLockDC", default=0))

        self.set_localized_string_nodes("Name", utw.find_field_data("LocName"))
