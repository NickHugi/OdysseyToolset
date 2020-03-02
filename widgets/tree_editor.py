from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QFontInfo, QFontMetrics
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider, QTreeWidgetItem, \
    QPlainTextEdit, QFrame, QSizePolicy, QLabel


class AbstractTreeEditor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

    def init_button(self, catergory, field, text):
        button = QPushButton()
        button.setText(text)
        button.setFixedHeight(17)
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, button)
        return button

    def init_line_edit(self, catergory, field):
        line_edit = QLineEdit()
        line_edit.setFixedHeight(23)
        line_edit.setStyleSheet("background: rgb(0,0,0,0%)")
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, line_edit)
        return line_edit

    def init_label(self, catergory, field):
        label = QLabel()
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, label)
        return label

    def init_multiline_edit(self, catergory, field):
        line_edit = QPlainTextEdit()
        line_edit.setMaximumHeight(69)
        line_edit.setFrameStyle(QFrame.NoFrame)
        line_edit.setStyleSheet("background: rgb(0,0,0,0%)")
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, line_edit)
        return line_edit

    def init_spin_box(self, catergory, field, min=0, max=999999):
        spin_box = QSpinBox()
        spin_box.setMaximum(max)
        spin_box.setMinimum(min)
        spin_box.setFixedHeight(23)
        spin_box.setStyleSheet("background: rgb(0,0,0,0%); border-width: 0px; border-style: none;")
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, spin_box)
        return spin_box

    def init_check_box(self, catergory, field, checked=False):
        check_box = QCheckBox()
        check_box.setFixedHeight(23)
        check_box.setChecked(checked)
        check_box.setStyleSheet("QCheckBox::indicator { width: 23; height: 23;}")
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, check_box)
        return check_box

    def init_combo_box(self, catergory, field, items=None):
        if items is None:
            items = []
        combo_box = QComboBox()
        combo_box.setFixedHeight(23)
        combo_box.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        combo_box.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        combo_box.addItems(items)
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, combo_box)
        return combo_box

    def init_slider(self, catergory, field, min=0, max=100):
        slider = QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setFixedHeight(23)
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, slider)
        return slider

    def get_node(self, category, field):
        catergory_node = self.ui.tree.findItems(category, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)[0]
        for i in range(catergory_node.childCount()):
            child = catergory_node.child(i)
            if child.text(0) == field:
                return child

    def get_node_widget(self, catergory, field):
        node = self.get_node(catergory, field)
        return self.ui.tree.itemWidget(node, 1)
