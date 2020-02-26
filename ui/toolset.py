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
        self.tab_widget = QtWidgets.QTabWidget(self.splitter)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setObjectName("tab_widget")
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
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.core_tree = QtWidgets.QTreeView(self.tab)
        self.core_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.core_tree.setAlternatingRowColors(True)
        self.core_tree.setObjectName("core_tree")
        self.gridLayout_3.addWidget(self.core_tree, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.modules_tree = QtWidgets.QTreeView(self.tab_2)
        self.modules_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.modules_tree.setAlternatingRowColors(True)
        self.modules_tree.setObjectName("modules_tree")
        self.gridLayout_4.addWidget(self.modules_tree, 1, 0, 1, 1)
        self.modules_combo = QtWidgets.QComboBox(self.tab_2)
        self.modules_combo.setObjectName("modules_combo")
        self.gridLayout_4.addWidget(self.modules_combo, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.override_tree = QtWidgets.QTreeView(self.tab_3)
        self.override_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.override_tree.setAlternatingRowColors(True)
        self.override_tree.setObjectName("override_tree")
        self.gridLayout_5.addWidget(self.override_tree, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_extract = QtWidgets.QPushButton(self.layoutWidget)
        self.button_extract.setObjectName("button_extract")
        self.gridLayout.addWidget(self.button_extract, 0, 0, 1, 1)
        self.button_open = QtWidgets.QPushButton(self.layoutWidget)
        self.button_open.setObjectName("button_open")
        self.gridLayout.addWidget(self.button_open, 0, 1, 1, 1)
        self.button_clear = QtWidgets.QPushButton(self.layoutWidget)
        self.button_clear.setObjectName("button_clear")
        self.gridLayout.addWidget(self.button_clear, 1, 0, 1, 1)
        self.button_toggle_selection = QtWidgets.QPushButton(self.layoutWidget)
        self.button_toggle_selection.setObjectName("button_toggle_selection")
        self.gridLayout.addWidget(self.button_toggle_selection, 1, 1, 1, 1)
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
        self.actionItem = QtWidgets.QAction(MainWindow)
        self.actionItem.setObjectName("actionItem")
        self.actionDialogue = QtWidgets.QAction(MainWindow)
        self.actionDialogue.setObjectName("actionDialogue")
        self.actionMerchant = QtWidgets.QAction(MainWindow)
        self.actionMerchant.setObjectName("actionMerchant")
        self.actionScript = QtWidgets.QAction(MainWindow)
        self.actionScript.setObjectName("actionScript")
        self.actionTrigger = QtWidgets.QAction(MainWindow)
        self.actionTrigger.setObjectName("actionTrigger")
        self.actionEncounter = QtWidgets.QAction(MainWindow)
        self.actionEncounter.setObjectName("actionEncounter")
        self.actionDoor = QtWidgets.QAction(MainWindow)
        self.actionDoor.setObjectName("actionDoor")
        self.menuNew.addAction(self.action_new_module)
        self.menuNew.addAction(self.action_new_archve)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.action_new_creature)
        self.menuNew.addAction(self.action_new_placeable)
        self.menuNew.addAction(self.actionDoor)
        self.menuNew.addAction(self.actionDialogue)
        self.menuNew.addAction(self.actionEncounter)
        self.menuNew.addAction(self.actionMerchant)
        self.menuNew.addAction(self.actionTrigger)
        self.menuNew.addAction(self.actionScript)
        self.menuNew.addAction(self.actionItem)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.action_new_gff)
        self.menuNew.addAction(self.action_new_2da)
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
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.installation_combo.setItemText(0, _translate("MainWindow", "[None]"))
        self.filter_edit.setPlaceholderText(_translate("MainWindow", "filter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Core"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Modules"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Override"))
        self.button_extract.setText(_translate("MainWindow", "Extract"))
        self.button_open.setText(_translate("MainWindow", "Open"))
        self.button_clear.setText(_translate("MainWindow", "Clear"))
        self.button_toggle_selection.setText(_translate("MainWindow", "Single"))
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
        self.actionItem.setText(_translate("MainWindow", "Item"))
        self.actionDialogue.setText(_translate("MainWindow", "Conversation"))
        self.actionMerchant.setText(_translate("MainWindow", "Merchant"))
        self.actionScript.setText(_translate("MainWindow", "Script"))
        self.actionTrigger.setText(_translate("MainWindow", "Trigger"))
        self.actionEncounter.setText(_translate("MainWindow", "Encounter"))
        self.actionDoor.setText(_translate("MainWindow", "Door"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
