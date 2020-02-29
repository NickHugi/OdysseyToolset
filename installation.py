import os

from pykotor.globals import resource_types

from pykotor.formats.erf import ERF
from pykotor.formats.key import KEY
from pykotor.formats.tpc import TPC


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

    @staticmethod
    def find_resource(res_ref, res_type, installation=None, priority_path=""):
        if type(res_type) is str:
            res_type = resource_types[res_type]
        file_name = res_ref + "." + res_type.extension

        if priority_path != "" and os.path.exists(priority_path + "/" + file_name):
            file = open(priority_path + "/" + file_name, 'rb')
            data = file.read()
            file.close()
            return data

        if installation is not None:  # TODO and installation.chitin.has_resource(res_ref, res_type):
            data = installation.chitin.fetch_resource(res_ref, res_type)
            if data is not None:
                return data

        if installation is not None and os.path.exists(installation.override_path + "/" + file_name):
            file = open(installation.override_path + "/" + file_name, 'rb')
            data = file.read()
            file.close()
            return data

