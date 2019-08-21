from collections import defaultdict, OrderedDict
from enum import Enum
import yaml
from AAV.Sequence import Normalization

'''
class BarcodeYaml(Enum):
    LIBNAME = 'libName'
    BARCODE_DICT = 'barcodeDict'
    BARCODE_INDICES = 'barcodeIndices'
    BARCODE_ARRAY = 'barcodeArray'
    LIBSIZE = 'libSize'

class ControlYaml(Enum):
    CONTROLBC = 'controlBC'

class YamlReader:
    def __init__(self):
        self.file_path = ''

    def set_file_path(self, file_path):
        self.file_path = file_path

    def read_yaml(self):
        stream = open(self.file_path, 'r')
        data = yaml.load_all(stream)
        return data
'''

class BarcodeMapper:
    def __init__(self):
        self.barcode_array = []
        self.barcode_dict = defaultdict()
        self.barcode_indices = defaultdict()
        self.barcode_libName = ''
        self.barcode_libSize = 0

        self.ordered_bin_seq_count_dict = defaultdict()
        self.ordered_bin_seq_count_dict_log2 = defaultdict()

    def set_barcode_array(self, barcode_array):
        self.barcode_array = barcode_array

    def set_barcode_dict(self, barcode_dict):
        self.barcode_dict = barcode_dict

    def set_barcode_indices(self, barcode_indices):
        self.barcode_indices = barcode_indices

    def set_barcode_libName(self, barcode_libName):
        self.barcode_libName = barcode_libName

    def set_barcode_libSize(self, barcode_libSize):
        self.barcode_libSize = barcode_libSize


    # reads to binary_barcode using bit shift, it's a binary form, but returns a decimal.
    def read_2_binary_barcode(self, seq):
        barcode_array_len = len(self.barcode_array)
        bin_barcode = 0b0
        for i in range(barcode_array_len):
            if (self.barcode_array[barcode_array_len - 1 - i] + '_' + seq[i*7 : i*7+3] in self.barcode_dict):
                bin_barcode += self.barcode_dict[self.barcode_array[barcode_array_len - 1 - i] + '_' + seq[i*7 : i*7+3]] << i
            else:
                return None
        return bin_barcode


    # arg counted_seq is from SeqCounter's results, a dictionary {seq : counts}
    # arg lib_name is from yaml file
    # function returns a dictionary, e.g. {Anc80_0..2047 : counts}
    def sum_binary_count(self, counted_seq, lib_name, lib_size):
        bin_seq_count = defaultdict()
        for key, value in counted_seq.items():
            bin_key = self.read_2_binary_barcode(key) # converting seq to binary form
            if bin_key in bin_seq_count:
                bin_seq_count[bin_key] += value
            else:
                bin_seq_count[bin_key] = value

        # Checking those binary counts are 0, which are not included in the dictionary, so we add them manually.
        for i in range(lib_size):
            k = i
            if not k in bin_seq_count:
               bin_seq_count[k] = 0

        # Delete those 'None' counts.
        del bin_seq_count[None]

        # Sort the dictionary with original (int) keys. Then append the libName to rename the keys.
        ordered_bin_seq_count = OrderedDict(sorted(bin_seq_count.items()))

        # Combine libName and number together
        for k in range(lib_size):
            ordered_bin_seq_count[lib_name + str(k)] = ordered_bin_seq_count.pop(k)

        total_mapped_count = sum(ordered_bin_seq_count.values())
        norm = Normalization.Normalization()

        ordered_bin_seq_count_dict_log2 = defaultdict()
        for key, value in ordered_bin_seq_count.items():
            ordered_bin_seq_count_dict_log2[key] = norm.log2func(total_mapped_count, value)

        self.ordered_bin_seq_count_dict = ordered_bin_seq_count
        self.ordered_bin_seq_count_dict_log2 = ordered_bin_seq_count_dict_log2

        # return ordered_bin_seq_count_dict_log2




def main():
    '''
    bar = BarcodeMapper()
    reader = YamlReader()
    reader.set_file_path('../Barcode_libs/Anc80Config.yaml')
    # bar.barcodeYaml_test()
    data = reader.read_yaml()

    for d in data:
        bar.set_barcode_dict(d[BarcodeYaml.BARCODE_DICT.value])
        # bar.set_barcode_indices(d[BarcodeYaml.BARCODE_INDICES.value])
    for k, v in bar.barcode_dict.items():
        print(k + " : ", v)
    for k, v in bar.barcode_indices.items():
        print(k + " : ", v)

    print(bar.barcode_indices['B1'])

    bin_code = 0b0
    for i in range(6):
        bin_code += 1 << i

    print(bin(bin_code))
    print(bin_code)
    '''

if __name__ == '__main__':
    main()
