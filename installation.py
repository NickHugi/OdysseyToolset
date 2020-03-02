import os

from pykotor.formats.mdl import MDL

from pykotor.formats.tlk import TLK
from pykotor.formats.twoda import TwoDA

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

    def get_tlk_entry_count(self):
        return TLK.fetch_entry_count(self.root_path + "/dialog.tlk")

    def get_tlk_entry_text(self, index):
        return TLK.fetch_entry_text(self.root_path + "/dialog.tlk", index)

    def get_appearance_model(self, index):
        # TODO: Allow for a good/evil parameter to influence the texture
        models = []

        appearance = TwoDA.from_data(self.chitin.fetch_resource("appearance", "2da"))
        heads = TwoDA.from_data(self.chitin.fetch_resource("heads", "2da"))

        model_type = appearance.get_cell("modeltype", index)
        race = appearance.get_cell("race", index)
        modela = appearance.get_cell("modela", index)

        if race != "":
            body_model = Installation.find_model(race, self)
        else:
            body_model = Installation.find_model(modela, self)
        models.append(body_model)

        if model_type == "B":
            head_index = appearance.get_integer("normalhead", index)
            head_res_ref = heads.get_cell("head", head_index)
            head_model = self.find_model(head_res_ref, self)
            models.append(head_model)
        print(models)

        return models

    @staticmethod
    def get_appearance_list(installation):
        # TODO: check override for 2da, have premade list for installation==None
        data = TwoDA.from_data(installation.chitin.fetch_resource("appearance", "2da"))
        labels = data.get_column_data("label")
        return labels

    @staticmethod
    def get_soundset_list(installation):
        # TODO: check override for 2da, have premade list for installation==None
        data = TwoDA.from_data(installation.chitin.fetch_resource("soundset", "2da"))
        labels = data.get_column_data("label")
        return labels

    @staticmethod
    def get_placeable_list(installation):
        # TODO: check override for 2da, have premade list for installation==None
        data = TwoDA.from_data(installation.chitin.fetch_resource("placeables", "2da"))
        labels = data.get_column_data("label")
        return labels

    @staticmethod
    def get_door_list(installation):
        # TODO: check override for 2da, have premade list for installation==None
        data = TwoDA.from_data(installation.chitin.fetch_resource("genericdoors", "2da"))
        labels = data.get_column_data("label")
        return labels

    @staticmethod
    def get_trap_type_list(tsl=True):
        list = ["Stun Minor", "Stun Average", "Stun Deadly", "Frag Minor", "Frag Average", "Frag Deadly",
                "Plasma Minor", "Plasma Average", "Plasma Deadly", "Gas Minor", "Gas Average", "Gas Deadly",
                "Rock Fall 2", "Rock Fall 1", "Sonic Minor", "Sonic Average", "Sonic Deadly", "Stun Strong",
                "Stun Devastating", "Frag Strong", "Frag Devastating", "Plasma Strong", "Plasma Devastating",
                "Gas Strong", "Gas Devastating", "Sonic Strong", "Sonic Devastating"]
        if not tsl:
            list = list[:14]
        return list

    @staticmethod
    def get_bodybag_list():
        return ["Default", "Backpack", "Equipment Pack", "Bagand Strap", "Metal Case", "Cloth Pile", "Pouch",
                "Tuskan Rags", "Rancor Corpse", "Krayt Corpse"]

    @staticmethod
    def get_faction_list(tsl=True):
        list = ["Friendly 1", "Hostile 2", "Friendly 2", "Neutral", "Insane", "Tuskan",
                "GLB XOR", "Surrender 1", "Surrender 2", "Predator", "Prey", "Trap",
                "Endar Spire", "Rancor", "Gizka 1", "Gizka 2", "Czerka",
                "Zone Controller", "Sacrifice", "One On One", "Party Puppet"]

        if not tsl:
            list = list[:-3]

        return list

    @staticmethod
    def get_gender_list():
        return ["Male", "Female", "Both", "Other", "None"]

    @staticmethod
    def get_race_list():
        return ["Human", "Droid"]

    @staticmethod
    def get_subrace_list(tsl=True):
        list = ["None", "Wookie", "Beast", "Zabrak"]
        if not tsl:
            list = list[:-1]
        return list

    @staticmethod
    def get_phenotype_list():
        return ["Normal", "Skinny", "Large"]

    @staticmethod
    def get_perception_list():
        return ["Short", "Medium", "Long", "Default", "Player", "Monster"]

    @staticmethod
    def get_speed_list():
        return ["PC Movement", "Immobile", "Very Slow", "Slow", "Normal", "Fast", "Very Fast", "Default", "DM Fast",
                "Huge", "Giant", "Wee Folk"]

    @staticmethod
    def get_class_list(tsl=True):
        list = ["Soldier", "Scout", "Scoundrel", "Jedi Guardian", "Jedi Consular", "Jedi Sentinel", "Combat Droid",
                "Expert Droid", "Minion", "Tech Specialist", "[CUT] Bounty Hunter", "Jedi Weaponmaster", "Jedi Master",
                "Jedi Watchman", "Sith Marauder", "Sith Lord", "Sith Assassin"]
        if not tsl:
            list = list [:-8]
        return list

    @staticmethod
    def get_max_level(tsl=True):
        if tsl:
            return 50
        else:
            return 20

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

        if installation is not None:
            data = installation.chitin.fetch_resource(res_ref, res_type)
            if data is not None:
                return data

        if installation is not None and os.path.exists(installation.override_path + "/" + file_name):
            file = open(installation.override_path + "/" + file_name, 'rb')
            data = file.read()
            file.close()
            return data

    @staticmethod
    def find_texture(res_ref, installation=None, priority_path=""):
        if installation is not None:
            data = ERF.fetch_resource(installation.textures_path + "/swpc_tex_tpa.erf", res_ref, "tpc")
            texture = TPC.from_data(data)
            return texture

        return None

    @staticmethod
    def find_model(res_ref, installation=None, priority_path=""):
        if installation is not None:
            data = installation.chitin.fetch_resource(res_ref.lower(), "mdl")
            data_ext = installation.chitin.fetch_resource(res_ref.lower(), "mdx")
            if data is None:
                return None
            return MDL.from_data(data, data_ext)
