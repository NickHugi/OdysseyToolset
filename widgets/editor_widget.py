from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from installation import Installation


class EditorWidget(QWidget):
    def __init__(self, parent, ui_module, icon=""):
        QWidget.__init__(self, parent)

        self.ui = ui_module.Ui_Form()
        self.ui.setupUi(self)

        self.icon = icon
        self.installation = self.window().active_installation
        self.file_path = ""
        self.res_ref = ""
        self.res_type = None

    def save_existing(self):
        raise NotImplementedError

    def save_to_path(self):
        raise NotImplementedError

    def save_to_module(self):
        raise NotImplementedError

    def setup(self, file_path, res_ref, res_type):
        file_tabs = self.window().ui.file_tabs
        file_tabs.addTab(self, res_ref + "." + res_type.extension)
        tab_index = -1
        for i in range(file_tabs.count()):
            if file_tabs.widget(i) == self:
                tab_index = i

        if self.installation is None:
            file_tabs.setTabIcon(tab_index, QIcon(":/kx_icons/" + self.icon))
        elif self.installation.is_tsl():
            file_tabs.setTabIcon(tab_index, QIcon(":/k2_icons/" + self.icon))
        else:
            file_tabs.setTabIcon(tab_index, QIcon(":/k1_icons/" + self.icon))

        installation_name = "None" if self.installation is None else self.installation.name
        file_tabs.setTabToolTip(tab_index, "Path: " + file_path + "\n" +
                                           "Resource: " + res_ref + "." + res_type.extension + "\n" +
                                            "Installation: " + installation_name)

    def load(self, some_data):
        raise NotImplementedError


