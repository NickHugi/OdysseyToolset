# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolset.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1169, 717)
        MainWindow.setAcceptDrops(False)
        MainWindow.setWindowTitle("Odyssey Toolset")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.file_tabs = QtWidgets.QTabWidget(self.splitter)
        self.file_tabs.setTabsClosable(True)
        self.file_tabs.setObjectName("file_tabs")
        self.console = QtWidgets.QTextEdit(self.splitter)
        self.console.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.console.setObjectName("console")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.installation_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.installation_combo.setObjectName("installation_combo")
        self.installation_combo.addItem("")
        self.verticalLayout.addWidget(self.installation_combo)
        self.filter_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.filter_edit.setObjectName("filter_edit")
        self.verticalLayout.addWidget(self.filter_edit)
        self.tree_tabs = QtWidgets.QTabWidget(self.layoutWidget)
        self.tree_tabs.setObjectName("tree_tabs")
        self.core_tab = QtWidgets.QWidget()
        self.core_tab.setObjectName("core_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.core_tab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.core_tree = QtWidgets.QTreeView(self.core_tab)
        self.core_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.core_tree.setAlternatingRowColors(True)
        self.core_tree.setObjectName("core_tree")
        self.gridLayout_3.addWidget(self.core_tree, 0, 0, 1, 1)
        self.tree_tabs.addTab(self.core_tab, "")
        self.modules_tab = QtWidgets.QWidget()
        self.modules_tab.setObjectName("modules_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.modules_tab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.modules_tree = QtWidgets.QTreeView(self.modules_tab)
        self.modules_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.modules_tree.setAlternatingRowColors(True)
        self.modules_tree.setObjectName("modules_tree")
        self.gridLayout_4.addWidget(self.modules_tree, 1, 0, 1, 1)
        self.modules_combo = QtWidgets.QComboBox(self.modules_tab)
        self.modules_combo.setObjectName("modules_combo")
        self.gridLayout_4.addWidget(self.modules_combo, 0, 0, 1, 1)
        self.tree_tabs.addTab(self.modules_tab, "")
        self.override_tab = QtWidgets.QWidget()
        self.override_tab.setObjectName("override_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.override_tab)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.override_tree = QtWidgets.QTreeView(self.override_tab)
        self.override_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.override_tree.setAlternatingRowColors(True)
        self.override_tree.setObjectName("override_tree")
        self.gridLayout_5.addWidget(self.override_tree, 0, 0, 1, 1)
        self.tree_tabs.addTab(self.override_tab, "")
        self.project_tab = QtWidgets.QWidget()
        self.project_tab.setObjectName("project_tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.project_tab)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.project_tree = QtWidgets.QTreeView(self.project_tab)
        self.project_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.project_tree.setAlternatingRowColors(True)
        self.project_tree.setObjectName("project_tree")
        self.gridLayout_6.addWidget(self.project_tree, 0, 0, 1, 1)
        self.tree_tabs.addTab(self.project_tab, "")
        self.verticalLayout.addWidget(self.tree_tabs)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_extract = QtWidgets.QPushButton(self.layoutWidget)
        self.button_extract.setObjectName("button_extract")
        self.gridLayout.addWidget(self.button_extract, 0, 0, 1, 1)
        self.button_open = QtWidgets.QPushButton(self.layoutWidget)
        self.button_open.setObjectName("button_open")
        self.gridLayout.addWidget(self.button_open, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1169, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.action_save_as = QtWidgets.QAction(MainWindow)
        self.action_save_as.setEnabled(False)
        self.action_save_as.setObjectName("action_save_as")
        self.action_new_gff = QtWidgets.QAction(MainWindow)
        self.action_new_gff.setObjectName("action_new_gff")
        self.action_save_to_module = QtWidgets.QAction(MainWindow)
        self.action_save_to_module.setEnabled(False)
        self.action_save_to_module.setObjectName("action_save_to_module")
        self.actionImage_Viewer = QtWidgets.QAction(MainWindow)
        self.actionImage_Viewer.setObjectName("actionImage_Viewer")
        self.actionModel_Viewer = QtWidgets.QAction(MainWindow)
        self.actionModel_Viewer.setObjectName("actionModel_Viewer")
        self.action_save_to_override = QtWidgets.QAction(MainWindow)
        self.action_save_to_override.setEnabled(False)
        self.action_save_to_override.setObjectName("action_save_to_override")
        self.action_new_archve = QtWidgets.QAction(MainWindow)
        self.action_new_archve.setObjectName("action_new_archve")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setEnabled(False)
        self.action_save.setObjectName("action_save")
        self.action_tools_tlk = QtWidgets.QAction(MainWindow)
        self.action_tools_tlk.setObjectName("action_tools_tlk")
        self.action_new_2da = QtWidgets.QAction(MainWindow)
        self.action_new_2da.setObjectName("action_new_2da")
        self.action_new_creature = QtWidgets.QAction(MainWindow)
        self.action_new_creature.setObjectName("action_new_creature")
        self.action_new_placeable = QtWidgets.QAction(MainWindow)
        self.action_new_placeable.setObjectName("action_new_placeable")
        self.action_new_module = QtWidgets.QAction(MainWindow)
        self.action_new_module.setObjectName("action_new_module")
        self.action_new_item = QtWidgets.QAction(MainWindow)
        self.action_new_item.setObjectName("action_new_item")
        self.action_new_dialog = QtWidgets.QAction(MainWindow)
        self.action_new_dialog.setObjectName("action_new_dialog")
        self.action_new_merchant = QtWidgets.QAction(MainWindow)
        self.action_new_merchant.setObjectName("action_new_merchant")
        self.action_new_script = QtWidgets.QAction(MainWindow)
        self.action_new_script.setObjectName("action_new_script")
        self.action_new_trigger = QtWidgets.QAction(MainWindow)
        self.action_new_trigger.setObjectName("action_new_trigger")
        self.action_new_encounter = QtWidgets.QAction(MainWindow)
        self.action_new_encounter.setObjectName("action_new_encounter")
        self.action_new_door = QtWidgets.QAction(MainWindow)
        self.action_new_door.setObjectName("action_new_door")
        self.action_tools_2da = QtWidgets.QAction(MainWindow)
        self.action_tools_2da.setObjectName("action_tools_2da")
        self.action_tools_erf = QtWidgets.QAction(MainWindow)
        self.action_tools_erf.setObjectName("action_tools_erf")
        self.action_new_waypoint = QtWidgets.QAction(MainWindow)
        self.action_new_waypoint.setObjectName("action_new_waypoint")
        self.action_new_sound = QtWidgets.QAction(MainWindow)
        self.action_new_sound.setObjectName("action_new_sound")
        self.menuNew.addAction(self.action_new_creature)
        self.menuNew.addAction(self.action_new_placeable)
        self.menuNew.addAction(self.action_new_door)
        self.menuNew.addAction(self.action_new_dialog)
        self.menuNew.addAction(self.action_new_waypoint)
        self.menuNew.addAction(self.action_new_encounter)
        self.menuNew.addAction(self.action_new_merchant)
        self.menuNew.addAction(self.action_new_trigger)
        self.menuNew.addAction(self.action_new_sound)
        self.menuNew.addAction(self.action_new_script)
        self.menuNew.addAction(self.action_new_item)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.action_new_gff)
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.action_save_as)
        self.menuFile.addAction(self.action_save_to_module)
        self.menuFile.addAction(self.action_save_to_override)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_settings)
        self.menuTools.addAction(self.action_tools_tlk)
        self.menuTools.addAction(self.action_tools_2da)
        self.menuTools.addAction(self.action_tools_erf)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        self.tree_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.installation_combo.setItemText(0, _translate("MainWindow", "[None]"))
        self.filter_edit.setPlaceholderText(_translate("MainWindow", "filter..."))
        self.tree_tabs.setTabText(self.tree_tabs.indexOf(self.core_tab), _translate("MainWindow", "Core"))
        self.tree_tabs.setTabText(self.tree_tabs.indexOf(self.modules_tab), _translate("MainWindow", "Modules"))
        self.tree_tabs.setTabText(self.tree_tabs.indexOf(self.override_tab), _translate("MainWindow", "Override"))
        self.tree_tabs.setTabText(self.tree_tabs.indexOf(self.project_tab), _translate("MainWindow", "Project"))
        self.button_extract.setText(_translate("MainWindow", "Extract"))
        self.button_open.setText(_translate("MainWindow", "Open"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.action_open.setText(_translate("MainWindow", "Open"))
        self.action_settings.setText(_translate("MainWindow", "Settings"))
        self.action_save_as.setText(_translate("MainWindow", "Save As"))
        self.action_new_gff.setText(_translate("MainWindow", "GFF"))
        self.action_save_to_module.setText(_translate("MainWindow", "Save To Module"))
        self.actionImage_Viewer.setText(_translate("MainWindow", "Image Viewer"))
        self.actionModel_Viewer.setText(_translate("MainWindow", "Model Viewer"))
        self.action_save_to_override.setText(_translate("MainWindow", "Save To Override"))
        self.action_new_archve.setText(_translate("MainWindow", "Archive"))
        self.action_save.setText(_translate("MainWindow", "Save"))
        self.action_tools_tlk.setText(_translate("MainWindow", "TLK Editor"))
        self.action_new_2da.setText(_translate("MainWindow", "2DA"))
        self.action_new_creature.setText(_translate("MainWindow", "Creature"))
        self.action_new_placeable.setText(_translate("MainWindow", "Placeable"))
        self.action_new_module.setText(_translate("MainWindow", "Module"))
        self.action_new_item.setText(_translate("MainWindow", "Item"))
        self.action_new_dialog.setText(_translate("MainWindow", "Conversation"))
        self.action_new_merchant.setText(_translate("MainWindow", "Merchant"))
        self.action_new_script.setText(_translate("MainWindow", "Script"))
        self.action_new_trigger.setText(_translate("MainWindow", "Trigger"))
        self.action_new_encounter.setText(_translate("MainWindow", "Encounter"))
        self.action_new_door.setText(_translate("MainWindow", "Door"))
        self.action_tools_2da.setText(_translate("MainWindow", "2DA Editor"))
        self.action_tools_erf.setText(_translate("MainWindow", "ERF Editor"))
        self.action_new_waypoint.setText(_translate("MainWindow", "Waypoint"))
        self.action_new_sound.setText(_translate("MainWindow", "Sound"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
