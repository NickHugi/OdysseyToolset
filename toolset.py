from PyQt5.QtCore import QSettings, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QFileDialog
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
        self.modules_tree_model = QStandardItemModel()
        self.modules_tree_proxy = QSortFilterProxyModel(self)
        self.override_tree_model = QStandardItemModel()
        self.override_tree_proxy = QSortFilterProxyModel(self)
        self.init_tree_model(self.ui.core_tree, self.core_tree_model, self.core_tree_proxy)
        self.init_tree_model(self.ui.modules_tree, self.modules_tree_model, self.modules_tree_proxy)
        self.init_tree_model(self.ui.override_tree, self.override_tree_model, self.override_tree_proxy)

        self.refresh_installation_list()

        self.init_ui_events()

    def init_tree_model(self, tree, model, proxy):
        model.setHorizontalHeaderLabels(["ResRef", "Type"])
        proxy.setSourceModel(model)
        proxy.setRecursiveFilteringEnabled(True)
        tree.setModel(proxy)

    def init_ui_events(self):
        self.ui.installation_combo.currentIndexChanged.connect(self.installation_combo_changed)

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
        self.modules_tree_proxy.setFilterFixedString("")
        self.override_tree_proxy.setFilterFixedString("")
        # self.core_tree_model.removeRows(0, self.tree_model.rowCount())
        # self.modules_tree_model.removeRows(0, self.tree_model.rowCount())
        # self.override_tree_model.removeRows(0, self.tree_model.rowCount())

    def build_trees(self):
        self.clear_trees()
        for entry in self.active_installation.chitin.keys.values():
            res_type = resource_types[entry.res_type]
            self.build_tree_add_resource(self.core_tree_model, entry.res_ref, res_type)

        self.ui.modules_combo.clear()
        for name, path in self.active_installation.get_module_list().items():
            self.ui.modules_combo.addItem(name)

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
        if hasattr(parent, "node_" + res_type.category) is not True:
            category_node = self.build_tree_add_node(parent, res_type.category)
            setattr(parent, "node_" + res_type.category, category_node)
        return self.build_tree_add_node(getattr(parent, "node_" + res_type.category), res_ref, res_type.extension)

    # Events
    def installation_combo_changed(self, index):
        self.clear_trees()
        self.active_installation = None

        if index > 0:
            installation_name = self.ui.installation_combo.itemText(index)
            self.load_installation(installation_name)
