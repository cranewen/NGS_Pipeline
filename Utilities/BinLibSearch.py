from AAV.Sequence import BarcodeMapper as bm
from collections import defaultdict

# A class for track decimal numbers back to binary numbers to match the libraries.
class BinLibSearch:
    def __init__(self, decimal_num, lib_path):
        self.decimal_num = decimal_num
        self.barcode_dict = defaultdict()
        self.barcode_array = []
        bar = bm.BarcodeMapper()
        reader = bm.YamlReader()
        reader.set_file_path(lib_path)
        data = reader.read_yaml()

        for d in data:
            bar.set_barcode_dict(d[bm.BarcodeYaml.BARCODE_DICT.value])
            self.barcode_dict = bar.barcode_dict
            bar.set_barcode_array(d[bm.BarcodeYaml.BARCODE_ARRAY.value])
            self.barcode_array = bar.barcode_array

    def track_back(self):
        barcode_array_len = len(self.barcode_array)
        barcode_bin_array = []
        for i in range(barcode_array_len):
            barcode_bin_array.append(self.decimal_num % 2)
            self.decimal_num = self.decimal_num >> 1
        barcode_bin_array.reverse()

        barcode_codon_array = [] # for storing tracked back codons in the keys of the library dictionary

        bin_index = 0
        barcode_dict_2_array = []
        for key, value in self.barcode_dict.items():
            barcode_dict_2_array.append([key, value])


        for i in range(barcode_array_len):
            if (barcode_bin_array[i] == barcode_dict_2_array[i*2][1]):
                barcode_codon_array.append(barcode_dict_2_array[i*2][0])
            else:
                barcode_codon_array.append(barcode_dict_2_array[i*2+1][0])

        return barcode_codon_array


def main():
    bls = BinLibSearch(1061, "../Barcode_libs/Anc80Config.yaml")
    print(bls.track_back())

if __name__ == '__main__':
    main()




