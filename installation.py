import os

from pykotor.formats.key import KEY


class Installation:
    def __init__(self, directory):
        self.root_path = directory

        self.chitin_path = self.root_path + "/chitin.key"

        self.modules_path = self.root_path + "/modules"
        self.override_path = self.root_path + "/override"
        self.textures_path = self.root_path + "/texturepacks"

        self.chitin = None

        self.chitin = KEY.from_path(self.chitin_path)
        self.get_module_list()

    def get_module_list(self):
        modules = {}
        for file in os.listdir(self.modules_path):
            file_path = self.modules_path + "/" + file
            modules[file] = file_path
        return modules

    def get_override_list(self):
        override = {}
        for file in os.listdir(self.override_path):
            file_path = self.modules_path + "/" + file
            override[file] = file_path
        return override