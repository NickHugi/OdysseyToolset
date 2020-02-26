from pykotor.formats.key import KEY


class Installation:
    def __init__(self, directory):
        self.root_path = directory

        self.chitin_path = self.root_path + "/chitin.key"

        self.modules_path = self.root_path + "/modules"
        self.override_path = self.root_path + "/override"
        self.textures_path = self.root_path + "/texturepacks"

        self.chitin = None
        self.modules = {}
        self.override = {}
        self.textures = {}

        self.load()

    def load(self):
        self.load_chitin()

    def load_chitin(self):
        self.chitin = KEY.from_path(self.chitin_path)

