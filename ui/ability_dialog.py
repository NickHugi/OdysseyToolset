# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ability_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(407, 454)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.table = QtWidgets.QTableView(Dialog)
        self.table.setAlternatingRowColors(True)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setVisible(False)
        self.table.horizontalHeader().setDefaultSectionSize(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.table, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
