from PyQt5.QtCore import QSettings, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from pykotor.formats.erf import ERF

from pykotor.formats.rim import RIM

from pykotor.globals import resource_types

from installation import Installation
from ui import toolset


class Toolset(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = toolset.Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.console.hide()

        self.settings = QSettings("toolset")
        self.installations = {}
        self.active_installation: Installation = None

        self.core_tree_model = QStandardItemModel()
        self.core_tree_proxy = QSortFilterProxyModel(self)
        self.modules_model = QStandardItemModel()
        self.modules_proxy = QSortFilterProxyModel(self)
        self.override_model = QStandardItemModel()
        self.override_proxy = QSortFilterProxyModel(self)
        self.init_tree_model(self.ui.core_tree, self.core_tree_model, self.core_tree_proxy)
        self.init_tree_model(self.ui.modules_tree, self.modules_model, self.modules_proxy)
        self.init_tree_model(self.ui.override_tree, self.override_model, self.override_proxy)

        self.refresh_installation_list()

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
        self.core_tree_proxy.setFilterFixedString("")
        self.modules_proxy.setFilterFixedString("")
        self.override_proxy.setFilterFixedString("")
        self.core_tree_model.removeRows(0, self.core_tree_model.rowCount())
        self.modules_model.removeRows(0, self.modules_model.rowCount())
        self.override_model.removeRows(0, self.override_model.rowCount())

    def build_trees(self):
        self.clear_trees()
        for entry in self.active_installation.chitin.keys.values():
            res_type = entry.res_type
            node = self.build_tree_add_resource(self.core_tree_model, entry.res_ref, res_type)

        self.ui.modules_combo.clear()
        for name, path in self.active_installation.get_module_list().items():
            item = QStandardItem(name)
            self.ui.modules_combo.addItem(name, path)

        for name, path in self.active_installation.get_override_list().items():
            res_ref = name[:name.index('.')]
            self.build_tree_add_resource(self.override_model, res_ref, resource_types[name[name.index(".") + 1:]])

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

    # Events
    def installation_combo_changed(self, index):
        self.clear_trees()
        self.active_installation = None

        if index > 0:
            installation_name = self.ui.installation_combo.itemText(index)
            self.load_installation(installation_name)

    def modules_combo_changed(self, index):
        self.modules_model.removeRows(0, self.modules_model.rowCount())
        path: str = self.ui.modules_combo.itemData(index)

        if ".rim" in path:
            resource_list = RIM.fetch_resource_list(path)
        else:
            resource_list = ERF.get_resource_list(path)

        self.modules_model.removeRows(0, self.modules_model.rowCount())
        for entry in resource_list:
            self.build_tree_add_resource(self.modules_model, entry["res_ref"], entry["res_type"])

    def open_button_clicked(self):
        data = None

        if self.ui.tree_tabs.currentIndex() == 0:  # CORE
            pass
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
                    data = RIM.fetch_resource(path, res_ref, res_type)
                else:
                    data = ERF.fetch_resource(path, res_ref, res_type)
        if self.ui.tree_tabs.currentIndex() == 2:  # OVERRIDE
            if len(self.ui.override_tree.selectedIndexes()) > 0:
                index0 = self.ui.override_tree.selectedIndexes()[0]
                index1 = self.ui.override_tree.selectedIndexes()[1]
                res_ref_item = self.override_model.itemFromIndex(self.override_proxy.mapToSource(index0))
                res_type_item = self.override_model.itemFromIndex(self.override_proxy.mapToSource(index1))
                res_ref = res_ref_item.text()
                res_type = resource_types[res_type_item.text().lower()]

                file = open(self.active_installation.override_path + "/" + res_ref + "." + res_type.extension, "rb")
                data = file.read()
                file.close()

