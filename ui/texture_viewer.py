# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'texture_viewer.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(552, 449)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.texture_label = QtWidgets.QLabel(self.splitter)
        self.texture_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.texture_label.setAlignment(QtCore.Qt.AlignCenter)
        self.texture_label.setObjectName("texture_label")
        self.txi_edit = QtWidgets.QPlainTextEdit(self.splitter)
        self.txi_edit.setObjectName("txi_edit")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.texture_label.setText(_translate("Form", "[texture]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
