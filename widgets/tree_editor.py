from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QFontInfo, QFontMetrics
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider, QTreeWidgetItem, \
    QPlainTextEdit, QFrame, QSizePolicy, QLabel, QDoubleSpinBox

from pykotor.formats.gff import LocalizedString
from pykotor.globals import Language


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

    def init_spin_box(self, catergory, field, min=0, max=999999, default=0):
        spin_box = QSpinBox()
        spin_box.setMaximum(max)
        spin_box.setMinimum(min)
        spin_box.setFixedHeight(23)
        spin_box.setValue(default)
        spin_box.setStyleSheet("background: rgb(0,0,0,0%); border-width: 0px; border-style: none;")
        self.ui.tree.setItemWidget(self.get_node(catergory, field), 1, spin_box)
        return spin_box

    def init_double_spin_box(self, catergory, field, min=0, max=999999, default=0):
        spin_box = QDoubleSpinBox()
        spin_box.setMaximum(max)
        spin_box.setMinimum(min)
        spin_box.setFixedHeight(23)
        spin_box.setValue(default)
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
        catergory_node = self.ui.tree.findItems(category, QtCore.Qt.MatchExactly)[0]
        for i in range(catergory_node.childCount()):
            child = catergory_node.child(i)
            if child.text(0) == field:
                return child

    def get_node_widget(self, catergory, field):
        node = self.get_node(catergory, field)
        return self.ui.tree.itemWidget(node, 1)

    def set_node_data(self, catergory, field, data):
        widget = self.get_node_widget(catergory, field)

        if type(data) is int and data == 4294967295:
            data = -1

        if type(widget) is QLineEdit:
            if type(data) is str:
                widget.setText(data)
        if type(widget) is QCheckBox:
            if type(data) is int:
                if data == 1: widget.setChecked(True)
                else: widget.setChecked(False)
            elif type(data) is bool:
                widget.setChecked(data)
        if type(widget) is QSpinBox:
            if type(data) is int:
                widget.setValue(data)
        if type(widget) is QDoubleSpinBox:
            if type(data) is float:
                widget.setValue(data)
        if type(widget) is QSlider:
            if type(data) is int:
                widget.setValue(data)
        if type(widget) is QComboBox:
            if type(data) is int:
                widget.setCurrentIndex(data)
        if type(widget) is QPlainTextEdit:
            if type(data) is str:
                widget.setPlainText(data)

    def get_node_data(self, category, field):
        widget = self.get_node_widget(category, field)

        if type(widget) is QLineEdit:
            return widget.text()
        if type(widget) is QCheckBox:
            if widget.isChecked(): return 1
            else: return 0
        if type(widget) is QSpinBox:
            return widget.value()
        if type(widget) is QSlider:
            return widget.value()
        if type(widget) is QDoubleSpinBox:
            return widget.value()
        if type(widget) is QComboBox:
            return widget.currentIndex()
        if type(widget) is QPlainTextEdit:
            return widget.toPlainText()

    def get_node_localized_string(self, category):
        localized_string = LocalizedString(0, {})
        localized_string.string_id = self.get_node_data(category, "TLK Reference")

        if self.get_node_data(category, "English") != "":
            localized_string.substrings[Language.English * 2] = self.get_node_data(category, "English")
        if self.get_node_data(category, "French") != "":
            localized_string.substrings[Language.French * 2] = self.get_node_data(category, "French")
        if self.get_node_data(category, "German") != "":
            localized_string.substrings[Language.German * 2] = self.get_node_data(category, "German")
        if self.get_node_data(category, "Italian") != "":
            localized_string.substrings[Language.Italian * 2] = self.get_node_data(category, "Italian")
        if self.get_node_data(category, "Spanish") != "":
            localized_string.substrings[Language.Spanish * 2] = self.get_node_data(category, "Spanish")
        if self.get_node_data(category, "Polish") != "":
            localized_string.substrings[Language.Polish * 2] = self.get_node_data(category, "Polish")
        return localized_string

    def set_localized_string_nodes(self, category, localized_string):
        if localized_string is not None:
            self.set_node_data(category, "TLK Reference", localized_string.string_id)
            if Language.English * 2 in localized_string.substrings:
                self.set_node_data(category, "English", localized_string.substrings[Language.English * 2])
            if Language.French * 2 in localized_string.substrings:
                self.set_node_data(category, "French", localized_string.substrings[Language.French * 2])
            if Language.German * 2 in localized_string.substrings:
                self.set_node_data(category, "German", localized_string.substrings[Language.German * 2])
            if Language.Italian * 2 in localized_string.substrings:
                self.set_node_data(category, "Italian", localized_string.substrings[Language.Italian * 2])
            if Language.Spanish * 2 in localized_string.substrings:
                self.set_node_data(category, "Spanish", localized_string.substrings[Language.Spanish * 2])
            if Language.Polish * 2 in localized_string.substrings:
                self.set_node_data(category, "Polish", localized_string.substrings[Language.Polish * 2])

    def init_localized_string_nodes(self, catergory, multiline=False):
        if multiline:
            self.init_spin_box(catergory, "TLK Reference", min=-1, default=-1)
            self.init_multiline_edit(catergory, "TLK Text")
            self.get_node_widget(catergory, "TLK Text").setReadOnly(True)
            self.init_multiline_edit(catergory, "English")
            self.init_multiline_edit(catergory, "French")
            self.init_multiline_edit(catergory, "German")
            self.init_multiline_edit(catergory, "Italian")
            self.init_multiline_edit(catergory, "Spanish")
            self.init_multiline_edit(catergory, "Polish")
            self.init_multiline_edit(catergory, "Korean")
        else:
            self.init_spin_box(catergory, "TLK Reference", min=-1, default=-1)
            self.init_line_edit(catergory, "TLK Text")
            self.get_node_widget(catergory, "TLK Text").setReadOnly(True)
            self.init_line_edit(catergory, "English")
            self.init_line_edit(catergory, "French")
            self.init_line_edit(catergory, "German")
            self.init_line_edit(catergory, "Italian")
            self.init_line_edit(catergory, "Spanish")
            self.init_line_edit(catergory, "Polish")
            self.init_line_edit(catergory, "Korean")

        if self.installation is None:
            self.get_node(catergory, "TLK Text").parent().removeChild(self.get_node(catergory, "TLK Text"))

        self.get_node_widget(catergory, "TLK Reference").valueChanged.connect(
            lambda category=catergory: self.tlk_reference_changed(catergory))

    def tlk_reference_changed(self, category):
        if self.installation is not None:
            index = self.get_node_widget(category, "TLK Reference").value()
            widget = self.get_node_widget(category, "TLK Text")

            if type(widget) is QLineEdit:
                self.get_node_widget(category, "TLK Text").setText("")
            if type(widget) is QPlainTextEdit:
                self.get_node_widget(category, "TLK Text").setPlainText("")

            if index < self.installation.get_tlk_entry_count() and index != -1:
                text = self.installation.get_tlk_entry_text(index)
                if type(widget) is QLineEdit:
                    self.get_node_widget(category, "TLK Text").setText(text)
                if type(widget) is QPlainTextEdit:
                    self.get_node_widget(category, "TLK Text").setPlainText(text)

