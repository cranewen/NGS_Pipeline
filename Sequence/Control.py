from AAV.Utilities import YamlReader as yr
from collections import defaultdict

class Control:
    # arg count_lib is the control library file path
    def __init__(self, control_lib):
        self.reader = yr.YamlReader()
        self.data = self.reader.read_yaml(control_lib)
        self.control_dict = defaultdict()
        for d in self.data:
            self.control_dict = d[yr.ControlYaml.CONTROLBC.value]

        self.control_count_dict = defaultdict()

    # arg count_dict is a dictionary from duplicated counts from original fastq file
    def count_controls(self, seq):
        for k,v in self.control_dict.items():
            if (seq == v and k in self.control_count_dict):
                self.control_count_dict[k] += 1
            elif (seq == v):
                self.control_count_dict[k] = 1
            elif (k not in self.control_count_dict):
                self.control_count_dict[k] = 0





