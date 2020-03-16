# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item_property_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(747, 414)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.property_list = QtWidgets.QListWidget(self.layoutWidget)
        self.property_list.setObjectName("property_list")
        self.verticalLayout.addWidget(self.property_list)
        self.add_button = QtWidgets.QPushButton(self.layoutWidget)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.layoutWidget)
        self.remove_button.setObjectName("remove_button")
        self.verticalLayout.addWidget(self.remove_button)
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.parameter_a_combo = QtWidgets.QComboBox(self.frame)
        self.parameter_a_combo.setObjectName("parameter_a_combo")
        self.gridLayout_2.addWidget(self.parameter_a_combo, 1, 1, 1, 1)
        self.subtype_label = QtWidgets.QLabel(self.frame)
        self.subtype_label.setObjectName("subtype_label")
        self.gridLayout_2.addWidget(self.subtype_label, 2, 0, 1, 1)
        self.property_label = QtWidgets.QLabel(self.frame)
        self.property_label.setObjectName("property_label")
        self.gridLayout_2.addWidget(self.property_label, 0, 0, 1, 1)
        self.parameter_b_label = QtWidgets.QLabel(self.frame)
        self.parameter_b_label.setObjectName("parameter_b_label")
        self.gridLayout_2.addWidget(self.parameter_b_label, 2, 1, 1, 1)
        self.parameter_a_label = QtWidgets.QLabel(self.frame)
        self.parameter_a_label.setObjectName("parameter_a_label")
        self.gridLayout_2.addWidget(self.parameter_a_label, 0, 1, 1, 1)
        self.upgrade_label = QtWidgets.QLabel(self.frame)
        self.upgrade_label.setObjectName("upgrade_label")
        self.gridLayout_2.addWidget(self.upgrade_label, 4, 1, 1, 1)
        self.property_combo = QtWidgets.QComboBox(self.frame)
        self.property_combo.setObjectName("property_combo")
        self.gridLayout_2.addWidget(self.property_combo, 1, 0, 1, 1)
        self.subtype_combo = QtWidgets.QComboBox(self.frame)
        self.subtype_combo.setObjectName("subtype_combo")
        self.gridLayout_2.addWidget(self.subtype_combo, 3, 0, 1, 1)
        self.parameter_b_combo = QtWidgets.QComboBox(self.frame)
        self.parameter_b_combo.setObjectName("parameter_b_combo")
        self.gridLayout_2.addWidget(self.parameter_b_combo, 3, 1, 1, 1)
        self.value_label = QtWidgets.QLabel(self.frame)
        self.value_label.setObjectName("value_label")
        self.gridLayout_2.addWidget(self.value_label, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 288, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 1, 1, 1)
        self.upgrade_combo = QtWidgets.QComboBox(self.frame)
        self.upgrade_combo.setObjectName("upgrade_combo")
        self.gridLayout_2.addWidget(self.upgrade_combo, 5, 1, 1, 1)
        self.value_combo = QtWidgets.QComboBox(self.frame)
        self.value_combo.setObjectName("value_combo")
        self.gridLayout_2.addWidget(self.value_combo, 5, 0, 1, 1)
        self.save_button = QtWidgets.QPushButton(self.frame)
        self.save_button.setObjectName("save_button")
        self.gridLayout_2.addWidget(self.save_button, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_button.setText(_translate("Dialog", "Add"))
        self.remove_button.setText(_translate("Dialog", "Remove"))
        self.subtype_label.setText(_translate("Dialog", "Subtype"))
        self.property_label.setText(_translate("Dialog", "Property"))
        self.parameter_b_label.setText(_translate("Dialog", "Parameter B"))
        self.parameter_a_label.setText(_translate("Dialog", "Parameter A"))
        self.upgrade_label.setText(_translate("Dialog", "Upgrade Required"))
        self.value_label.setText(_translate("Dialog", "Value"))
        self.save_button.setText(_translate("Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
