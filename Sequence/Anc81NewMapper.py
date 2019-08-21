from AAV.Utilities import YamlReader as yr
from collections import defaultdict, OrderedDict
from AAV.Sequence import Reader
from AAV.Sequence import Trimmer
from AAV.Sequence import Control

class Anc81NewMapper:
    def __init__(self):
        self.barcode_array = []
        self.barcode_dict = defaultdict()
        self.barcode_indices = defaultdict()
        self.barcode_libName = ''
        self.barcode_libSize = 0
        # self.control_dict = defaultdict()
        self.anc81_len = 78
        # self.irregular_gap_index_list = [4, 5, 7, 8, 9, 10, 11, 12, 13, 14]
        self.barcode_position_index = [0, 6, 12, 18, 25, 28, 35, 42, 45, 52, 55, 62, 65, 72, 75]
        self.barcode_count_dict = defaultdict() # for results
        self.control_count_dict = defaultdict()
        self.fastq_seq_records = [] # raw data
        self.trimmed_seq_gen = []
        self.dec_code = 0b0 # every single read to decimal number

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
        j = 0 # current index of the entire read

        for i in range(bc_len):
            if (self.barcode_array[bc_len - 1 - i] + '_' +
                    seq[self.barcode_position_index[i] : self.barcode_position_index[i] + 3] in self.barcode_dict):
                bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' +
                    seq[self.barcode_position_index[i] : self.barcode_position_index[i] + 3]] << i
            else:
                bin_code = None
                break

        self.dec_code = bin_code

    '''
        for i in range(bc_len):
            if i not in self.irregular_gap_index_list:
                if (self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3] in self.barcode_dict):
                    bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3]] << i
                    j += 7
                else:
                    bin_code = None
                    break
            else:
                if self.irregular_gap_index_list.index(i) % 2 == 0:
                    if (self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3] in self.barcode_dict):
                        bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3]] << i
                        j += 3
                    else:
                        bin_code = None
                        break
                else:
                    if (self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3] in self.barcode_dict):
                        bin_code += self.barcode_dict[self.barcode_array[bc_len - 1 - i] + '_' + seq[j : j + 3]] << i
                        j += 7
                    else:
                        bin_code = None
                        break

        self.dec_code = bin_code
    '''

    def trim_seq(self, seq_gen, min_len, quality_score):
        # t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC') # old
        t = Trimmer.Trimmer('AAGCTT', 'GCGGCCGC') # new
        t.set_min_len(min_len)
        t.set_phred_threshold(quality_score)
        for seq in seq_gen:
            t.trim_anc81(seq)
            yield t.get_trimmed_seq()

    def reverse_trim_seq(self, seq_gen, min_len, quality_score):
        t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC')
        t.set_min_len(min_len)
        t.set_phred_threshold(quality_score)
        for seq in seq_gen:
            t.reverse_trim_anc81(seq)
            yield t.get_trimmed_seq()


    def count_barcode(self):
        if self.dec_code is not None:
            if (self.dec_code) in self.barcode_count_dict:
                self.barcode_count_dict[self.dec_code] += 1
            else:
                self.barcode_count_dict[self.dec_code] = 1


    def sort_barcode(self):
        for i in range(self.barcode_libSize):
            k = i
            # adding 0 count variants
            if k not in self.barcode_count_dict:
                self.barcode_count_dict[k] = 0
        self.barcode_count_dict = OrderedDict(sorted(self.barcode_count_dict.items()))
        # adding prefix to the key
        for j in range(self.barcode_libSize):
            self.barcode_count_dict[self.barcode_libName + str(j)] = self.barcode_count_dict.pop(j)



def main():
    anc81 = Anc81NewMapper()
    anc81.set_barcode_dict(81)
    # anc81.read_2_decimal('AGTaaccAGCcttgGTGagagAACagttGACCTTactaAGCGAGaaggCGGattaCAGAGAggacCACAACcacaAGAACG')
    anc81.read_2_decimal('AGTaaccGCAcaatGTGtggcAGTtttgGACCTTgtgaGACagcgACGCGGatatGAGAGAggttAGCAACcctgAAAAGC')
    print(anc81.dec_code)

if __name__ == '__main__':
    main()



