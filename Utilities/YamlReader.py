from enum import Enum
import yaml


class BarcodeYaml(Enum):
    LIBNAME = 'libName'
    BARCODE_DICT = 'barcodeDict'
    BARCODE_INDICES = 'barcodeIndices'
    BARCODE_ARRAY = 'barcodeArray'
    LIBSIZE = 'libSize'


class ControlYaml(Enum):
    CONTROLBC = 'controlBC'


class YamlReader:
    def __init__(self, relative_path = False):
        if relative_path == True:
            self.barcode_lib_file_path = '../Barcode_libs/'
            self.control_lib_file_path = '../Control_libs/'
        else:
            self.barcode_lib_file_path = 'Barcode_libs/'
            self.control_lib_file_path = 'Control_libs/'
        self.lib_collection = {
            80: "Anc80Config.yaml",
            81: "Anc81Config.yaml",
            82: "Anc82Config.yaml",
            83: "Anc83Config.yaml",
            '83_1': "Anc83Config_1.yaml", # for Anc 83 P5 AAC variant (special case)
            84: "Anc84Config.yaml",
            110: "Anc110Config.yaml",
            113: "Anc113Config.yaml",
            126: "Anc126Config.yaml",
            127: "Anc127Config.yaml"
        }
        self.control_collection = {
            "control_20180322": "20180322controlSet.yaml"
        }

    def read_yaml(self, anc_num_or_control):
        if anc_num_or_control in self.lib_collection:
            stream = open(self.barcode_lib_file_path + self.lib_collection[anc_num_or_control], 'r')
            data = yaml.load_all(stream)
            return data
        if anc_num_or_control in self.control_collection:
            stream = open(self.control_lib_file_path + self.control_collection[anc_num_or_control], 'r')
            data = yaml.load_all(stream)
            return data
