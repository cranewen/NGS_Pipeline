from AAV.Utilities import YamlReader as yr
from collections import defaultdict, OrderedDict
from AAV.Sequence import Reader
from AAV.Sequence import Trimmer

class Anc83Mapper:
    def __init__(self):
        # all the alt variables are for B5_AAC
        self.barcode_array = []
        self.barcode_dict = defaultdict()
        self.barcode_AAC_dict = defaultdict()
        self.barcode_indices = defaultdict()
        self.barcode_libName = ''
        self.barcode_libName_alt = self.barcode_libName + '-'
        self.barcode_libSize = 0
        self.barcode_libSize_alt = self.barcode_libSize / 2
        self.barcode_count_dict = defaultdict() # for barcode results
        self.barcode_AAC_count_dict = defaultdict() # results for B5_AAC results
        self.control_count_dict = defaultdict() # for control results
        # self.aac_count_dict = defaultdict() # results for AAC barcode
        self.fastq_seq_records = [] # raw data
        self.trimmed_seq_gen = []
        self.dec_code = 0b0 # every single read to decimal number
        # self.dec_code_AAC = '' # particularly for p5 AAC variant, using variant 1 as barcode and add _1 as the result
        self.dec_code_AAC = 0b0

    def set_barcode_dict(self, lib_num, relative_path = False):
        yaml_reader = yr.YamlReader(relative_path)
        data = yaml_reader.read_yaml(lib_num)
        for d in data:
            self.barcode_array = d[yr.BarcodeYaml.BARCODE_ARRAY.value]
            self.barcode_dict = d[yr.BarcodeYaml.BARCODE_DICT.value]
            self.barcode_libName = d[yr.BarcodeYaml.LIBNAME.value]
            self.barcode_libSize = d[yr.BarcodeYaml.LIBSIZE.value]

    def read_file(self, file_path):
        r = Reader.Reader(file_path)
        self.fastq_seq_records = r.parse_fastq()

    def read_2_decimal(self, seq):
        bc_len = len(self.barcode_array)
        bin_code = 0b0
        bin_code_AAC = 0b0

        for i in range(bc_len):
            if (self.barcode_array[bc_len - 1 - i] + '_' + seq[i*7 : i*7+3] in self.barcode_dict):
                bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' + seq[i*7 : i*7+3]] << i
            elif (self.barcode_array[bc_len - 1 - i] + '_' + seq[i*7 : i*7+3] == 'AAC' and i == 4):
                bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' + seq[i*7 : i*7+3]] << i
                # bin_code_AAC = ~(bin_code + 1 << bc_len) + 1 # convert to - numbers
                # bin_code_AAC = bin_code
                # modified version, for each toggle 1, add 0b100000000 (256 in decimal) to eliminate the current
                # duplicated variants
                bin_code_AAC = bin_code + 0b100000000
            else:
                self.dec_code = None
                self.dec_code_AAC = None
                break

        if bin_code_AAC == '1':
            self.dec_code_AAC = str(bin_code) + '_1'
            self.dec_code = None
        else:
            self.dec_code = bin_code

    def trim_seq(self, seq_gen, min_len, quality_score):
        t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'CGCATCCCGTG')
        t.set_min_len(min_len)
        t.set_phred_threshold(quality_score)
        for seq in seq_gen:
            t.trim(seq)
            yield t.get_trimmed_seq()


    def count_barcode(self):
        if self.dec_code is not None:
            if (self.dec_code) in self.barcode_count_dict:
                self.barcode_count_dict[self.dec_code] += 1
            else:
                self.barcode_count_dict[self.dec_code] = 1

        if self.dec_code_AAC is not '':
            if (self.dec_code_AAC) in self.barcode_count_dict:
                self.barcode_count_dict[self.dec_code_AAC] += 1
            else:
                self.barcode_count_dict[self.dec_code_AAC] = 1

    def sort_barcode(self):
        for i in range(int(self.barcode_libSize / 2 * 3)):
            k = i
            # adding 0 count variants
            if k not in self.barcode_count_dict and (k + 1) % 3 != 0:
                self.barcode_count_dict[k] = 0
        self.barcode_count_dict = OrderedDict(sorted(self.barcode_count_dict.items()))
        # adding prefix to the key
        for j in range(self.barcode_libSize):
            self.barcode_count_dict[self.barcode_libName + str(j)] = self.barcode_count_dict.pop(j)




def main():
    anc83 = Anc83Mapper()
    anc83.set_barcode_dict(83)
    # anc81.read_2_decimal('AGTaaccAGCcttgGTGagagAACagttGACCTTactaAGCGAGaaggCGGattaCAGAGAggacCACAACcacaAGAACG')
    anc83.read_2_decimal('AGTaaccGCAcaatGTGtggcAGTtttgGACCTTgtgaGACagcgACGCGGatatGAGAGAggttAGCAACcctgAAAAGC')
    print(anc83.dec_code)

if __name__ == '__main__':
    main()








