import os

from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QMenu, QAction

from pykotor.formats.gff import GFF
from pykotor.formats.mdl import MDL

from pykotor.formats.erf import ERF

from pykotor.formats.rim import RIM
from pykotor.formats.tpc import TPC

from pykotor.globals import resource_types

from installation import Installation
from ui import toolset
from widgets.creature_editor import CreatureEditor
from widgets.dialog_editor import DialogEditor
from widgets.door_editor import DoorEditor
from widgets.encounter_editor import EncounterEditor
from widgets.erf_editor import ERFEditor
from widgets.item_editor import ItemEditor
from widgets.merchant_editor import MerchantEditor
from widgets.model_renderer import ModelRenderer, Object
from widgets.placeable_editor import PlaceableEditor
from widgets.sound_editor import SoundEditor
from widgets.texture_viewer import TextureViewer
from widgets.tlk_editor import TLKEditor
from widgets.trigger_editor import TriggerEditor
from widgets.twoda_editor import TwoDAEditor
from widgets.waypoint_editor import WaypointEditor


class Toolset(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = toolset.Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.tree_tabs.setEnabled(False)
        self.ui.filter_edit.setEnabled(False)
        self.ui.tree_tabs.setTabEnabled(3, False)
        self.ui.console.hide()

        self.subwindows = []

        self.settings = QSettings("toolset")
        self.installations = {}
        self.active_installation: Installation = None

        self.core_model = QStandardItemModel()
        self.core_proxy = QSortFilterProxyModel(self)
        self.modules_model = QStandardItemModel()
        self.modules_proxy = QSortFilterProxyModel(self)
        self.override_model = QStandardItemModel()
        self.override_proxy = QSortFilterProxyModel(self)
        self.project_model = QStandardItemModel()
        self.project_proxy = QSortFilterProxyModel(self)
        self.init_tree_model(self.ui.core_tree, self.core_model, self.core_proxy)
        self.init_tree_model(self.ui.modules_tree, self.modules_model, self.modules_proxy)
        self.init_tree_model(self.ui.override_tree, self.override_model, self.override_proxy)
        self.init_tree_model(self.ui.project_tree, self.project_model, self.project_proxy)

        self.ui.core_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.modules_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.override_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.project_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.refresh_installation_list()

        self.project_directory = "A:/KM/Analysis Files/ut"

        self.init_ui_events()

    def init_tree_model(self, tree, model, proxy):
        model.setHorizontalHeaderLabels(["ResRef", "Type"])
        proxy.setSourceModel(model)
        proxy.setRecursiveFilteringEnabled(True)
        tree.setModel(proxy)

    def init_ui_events(self):
        self.ui.installation_combo.currentIndexChanged.connect(self.installation_combo_changed)
        self.ui.modules_combo.currentIndexChanged.connect(self.modules_combo_changed)
        self.ui.button_open.clicked.connect(self.open_button_clicked)
        self.ui.button_extract.clicked.connect(self.extract_button_clicked)
        self.ui.action_tools_erf.triggered.connect(self.tools_erf_action_triggered)
        self.ui.action_tools_tlk.triggered.connect(self.tools_tlk_action_triggered)
        self.ui.action_tools_2da.triggered.connect(self.tools_2da_action_triggered)
        self.ui.action_new_creature.triggered.connect(self.new_creature_action_triggered)
        self.ui.action_new_placeable.triggered.connect(self.new_placeable_action_triggered)
        self.ui.action_new_door.triggered.connect(self.new_door_action_triggered)
        self.ui.action_new_item.triggered.connect(self.new_item_action_triggered)
        self.ui.action_new_dialog.triggered.connect(self.new_dialog_action_triggered)
        self.ui.action_new_merchant.triggered.connect(self.new_merchant_action_triggered)
        self.ui.action_new_waypoint.triggered.connect(self.new_waypoint_action_triggered)
        self.ui.action_new_trigger.triggered.connect(self.new_trigger_action_triggered)
        self.ui.action_new_encounter.triggered.connect(self.new_encounter_action_triggered)
        self.ui.action_new_sound.triggered.connect(self.new_sound_action_triggered)
        self.ui.action_open.triggered.connect(self.open_action_triggered)
        self.ui.filter_edit.textEdited.connect(self.filter_tree)
        self.ui.core_tree.customContextMenuRequested.connect(self.show_tree_context_menu)
        self.ui.modules_tree.customContextMenuRequested.connect(self.show_tree_context_menu)
        self.ui.override_tree.customContextMenuRequested.connect(self.show_tree_context_menu)
        self.ui.project_tree.customContextMenuRequested.connect(self.show_tree_context_menu)

    def refresh_installation_list(self):
        self.ui.installation_combo.clear()
        self.ui.installation_combo.addItem("[None]")

        if self.settings.value('installations') is None:
            self.settings.setValue('installations', {"KotOR": "", "TSL": ""})

        for path, data_set in self.settings.value('installations').items():
            self.ui.installation_combo.addItem(path)

    def load_installation(self, name):
        self.clear_trees()
        self.active_installation = None

        installations = self.settings.value('installations')
        path = installations[name]

        if path == "":
            dialog = QFileDialog()
            path = installations[name] = dialog.getExistingDirectory(self, "Select KotOR Path")
            self.settings.setValue('installations', installations)

        self.installations[name] = Installation(path)
        self.active_installation = self.installations[name]
        self.build_trees()

    def clear_trees(self):
        self.ui.filter_edit.setText("")
        self.core_proxy.setFilterFixedString("")
        self.modules_proxy.setFilterFixedString("")
        self.override_proxy.setFilterFixedString("")
        self.core_model.removeRows(0, self.core_model.rowCount())
        self.modules_model.removeRows(0, self.modules_model.rowCount())
        self.override_model.removeRows(0, self.override_model.rowCount())

    def build_trees(self):
        self.clear_trees()

        for entry in self.active_installation.chitin.keys.values():
            res_type = entry.res_type
            node = self.build_tree_add_resource(self.core_model, entry.res_ref, res_type)
            node.setData("chitin.key")

        for entry in ERF.fetch_resource_list(self.active_installation.textures_path + "/swpc_tex_tpa.erf"):
            node = self.build_tree_add_resource(self.core_model, entry["res_ref"], entry["res_type"])
            node.setData(self.active_installation.textures_path + "/swpc_tex_tpa.erf")

        for entry in ERF.fetch_resource_list(self.active_installation.textures_path + "/swpc_tex_gui.erf"):
            node = self.build_tree_add_resource(self.core_model, entry["res_ref"], entry["res_type"])
            node.setData(self.active_installation.textures_path + "/swpc_tex_tpa.erf")

        self.ui.modules_combo.clear()
        for name, path in self.active_installation.get_module_list().items():
            item = QStandardItem(name)
            self.ui.modules_combo.addItem(name, path)

        for name, path in self.active_installation.get_override_list().items():
            res_ref = name[:name.index('.')]
            res_extension = name[name.index(".") + 1:].lower()
            self.build_tree_add_resource(self.override_model, res_ref, resource_types[res_extension])

        for file in os.listdir(self.project_directory):
            file_path = self.project_directory + "/" + file
            res_ref = file[:file.index('.')]
            res_extension = file[file.index(".") + 1:].lower()
            self.build_tree_add_resource(self.project_model, res_ref, resource_types[res_extension])

        self.ui.tree_tabs.setEnabled(True)
        self.ui.filter_edit.setEnabled(True)

    def build_tree_add_node(self, parent, name, type=""):
        items = [QStandardItem(str(name)), QStandardItem(str(type.upper()))]

        items[0].setEditable(False)
        items[1].setEditable(False)

        if type == "":
            items[0].setSelectable(False)
            items[1].setSelectable(False)
            items[0].setEnabled(False)
            items[1].setEnabled(False)

        parent.appendRow(items)

        return items[0]

    def build_tree_add_resource(self, parent, res_ref, res_type):
        for i in range(parent.rowCount()):
            if parent.item(i, 0).text() == res_type.category:
                node = parent.item(i, 0)
                break
        else:
            node = self.build_tree_add_node(parent, res_type.category)

        return self.build_tree_add_node(node, res_ref, res_type.extension)

    def get_selected_data(self):
        data = []

        if self.ui.tree_tabs.currentIndex() == 0:  # CORE
            index0 = self.ui.core_tree.selectedIndexes()[0]
            index1 = self.ui.core_tree.selectedIndexes()[1]
            res_ref_item = self.core_model.itemFromIndex(self.core_proxy.mapToSource(index0))
            res_type_item = self.core_model.itemFromIndex(self.core_proxy.mapToSource(index1))
            res_ref = res_ref_item.text()
            res_type = resource_types[res_type_item.text().lower()]
            file_path = ""

            if res_ref_item.data() == "chitin.key":
                res_data = self.active_installation.chitin.fetch_resource(res_ref, res_type)
            elif ".erf" in res_ref_item.data():
                res_data = ERF.fetch_resource(res_ref_item.data(), res_ref, res_type)
                file_path = res_ref_item.data()
            else:
                file = open(res_ref_item.data(), 'rb')
                res_data = file.read()
                file.close()
                file_path = res_ref_item.data()
            data.append({"res_data": res_data,
                         "res_type": res_type,
                         "res_ref": res_ref,
                         "file_path": file_path})
        if self.ui.tree_tabs.currentIndex() == 1:  # MODULES
            if len(self.ui.modules_tree.selectedIndexes()) > 0:
                index0 = self.ui.modules_tree.selectedIndexes()[0]
                index1 = self.ui.modules_tree.selectedIndexes()[1]
                res_ref_item = self.modules_model.itemFromIndex(self.modules_proxy.mapToSource(index0))
                res_type_item = self.modules_model.itemFromIndex(self.modules_proxy.mapToSource(index1))
                res_ref = res_ref_item.text()
                res_type = resource_types[res_type_item.text().lower()]

                path = self.ui.modules_combo.currentData()
                if ".rim" in path:
                    data.append({"res_data": RIM.fetch_resource(path, res_ref, res_type),
                                 "res_type": res_type,
                                 "res_ref": res_ref,
                                 "file_path": path})
                else:
                    data.append({"res_data": ERF.fetch_resource(path, res_ref, res_type),
                                 "res_type": res_type,
                                 "res_ref": res_ref,
                                 "file_path": path})
        if self.ui.tree_tabs.currentIndex() == 2:  # OVERRIDE
            if len(self.ui.override_tree.selectedIndexes()) > 0:
                index0 = self.ui.override_tree.selectedIndexes()[0]
                index1 = self.ui.override_tree.selectedIndexes()[1]
                res_ref_item = self.override_model.itemFromIndex(self.override_proxy.mapToSource(index0))
                res_type_item = self.override_model.itemFromIndex(self.override_proxy.mapToSource(index1))
                res_ref = res_ref_item.text()
                res_type = resource_types[res_type_item.text().lower()]
                file_path = self.active_installation.override_path + "/" + res_ref + "." + res_type.extension

                file = open(file_path, "rb")
                data.append({"res_data": file.read(), "res_type": res_type, "res_ref": res_ref, "file_path": file_path})
                file.close()

        return data

    def open_resource(self, res_ref, res_type, res_data, file_path=""):
        widget = None

        if res_type == "tpc" or res_type == "tga" or res_type == "bmp" or res_type == "png" or res_type == "jpg":
            widget = TextureViewer.open_resource(self, res_ref, res_type, res_data)

        if res_type == "mdl":
            data_ext = Installation.find_resource(res_ref, "mdx", self.active_installation, os.path.dirname(file_path))
            mdl = MDL.from_data(res_data, data_ext)
            widget = ModelRenderer(self)
            widget.model_buffer[res_ref] = mdl
            widget.objects.append(Object(res_ref))

        if widget is not None:
            self.ui.file_tabs.addTab(widget, res_ref + "." + res_type.extension)

    # Events
    def installation_combo_changed(self, index):
        self.clear_trees()
        self.ui.tree_tabs.setEnabled(False)
        self.ui.filter_edit.setEnabled(False)
        self.ui.modules_combo.clear()
        self.active_installation = None

        if index > 0:
            installation_name = self.ui.installation_combo.itemText(index)
            self.load_installation(installation_name)

    def modules_combo_changed(self, index):
        self.modules_model.removeRows(0, self.modules_model.rowCount())

        if index == -1:
            return

        path: str = self.ui.modules_combo.itemData(index)

        if ".rim" in path:
            resource_list = RIM.fetch_resource_list(path)
        else:
            resource_list = ERF.fetch_resource_list(path)

        self.modules_model.removeRows(0, self.modules_model.rowCount())
        for entry in resource_list:
            self.build_tree_add_resource(self.modules_model, entry["res_ref"], entry["res_type"])

    def open_button_clicked(self):
        resource = self.get_selected_data()[0]
        self.open_resource(resource["res_ref"], resource["res_type"], resource["res_data"])

    def extract_button_clicked(self):
        data = self.get_selected_data()[0]["res_data"]
        path = QFileDialog.getSaveFileName(self, "Extract file to")[0]

        file = open(path, 'wb')
        file.write(data)
        file.close()

    def filter_tree(self, string):
        self.core_proxy.setFilterFixedString(string)
        self.modules_proxy.setFilterFixedString(string)
        self.override_proxy.setFilterFixedString(string)

    def show_tree_context_menu(self, position):
        indexes = self.ui.core_tree.selectedIndexes()
        if len(indexes) == 0:
            return

        if self.ui.tree_tabs.currentIndex() == 0:
            model = self.core_model
            tree = self.ui.core_tree
        elif self.ui.tree_tabs.currentIndex() == 1:
            model = self.modules_model
            tree = self.ui.modules_tree
        else:
            model = self.override_model
            tree = self.ui.override_tree

        ext = model.itemFromIndex(self.core_proxy.mapToSource(self.ui.core_tree.selectedIndexes()[1])).text()
        res_type = resource_types[ext.lower()]

        menu = QMenu()

        extract_action = menu.addAction("Extract")
        extract_action.triggered.connect(self.extract_button_clicked)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.open_button_clicked)
        menu.addSeparator()

        if res_type == "mdl":
            menu.addAction("Decompile Binary")
        if res_type == "utc" or res_type == "uti" or res_type == "utd" or res_type == "utp" or res_type == "ute" or \
                res_type == "utt" or res_type == "utm" or res_type == "uts" or res_type == "dlg" or res_type == "utw":
            menu.addAction("Open in GFF Editor")

        menu.exec_(tree.viewport().mapToGlobal(position))

    def tools_erf_action_triggered(self):
        window = ERFEditor()
        window.show()
        self.subwindows.append(window)

    def tools_tlk_action_triggered(self):
        window = TLKEditor()
        window.show()
        self.subwindows.append(window)

    def tools_2da_action_triggered(self):
        window = TwoDAEditor()
        window.show()
        self.subwindows.append(window)

    def new_creature_action_triggered(self):
        widget = CreatureEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utc")

    def new_placeable_action_triggered(self):
        widget = PlaceableEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utp")

    def new_door_action_triggered(self):
        widget = DoorEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utd")

    def new_item_action_triggered(self):
        widget = ItemEditor(self)
        self.ui.file_tabs.addTab(widget, "new.uti")

    def new_dialog_action_triggered(self):
        widget = DialogEditor(self)
        self.ui.file_tabs.addTab(widget, "new.dlg")

    def new_merchant_action_triggered(self):
        widget = MerchantEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utm")

    def new_waypoint_action_triggered(self):
        widget = WaypointEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utw")

    def new_trigger_action_triggered(self):
        widget = TriggerEditor(self)
        self.ui.file_tabs.addTab(widget, "new.utt")

    def new_encounter_action_triggered(self):
        widget = EncounterEditor(self)
        self.ui.file_tabs.addTab(widget, "new.ute")

    def new_sound_action_triggered(self):
        widget = SoundEditor(self)
        self.ui.file_tabs.addTab(widget, "new.uts")

    def open_action_triggered(self):
        file_path = QFileDialog.getOpenFileName(self, "Open File")[0]

        if file_path != "":
            res_ref = os.path.splitext(os.path.basename(file_path))[0]
            res_type = resource_types[os.path.splitext(os.path.basename(file_path))[1].replace(".", "")]

            file = open(file_path, 'rb')
            res_data = file.read()
            file.close()

            self.open_resource(res_ref, res_type, res_data, file_path)
