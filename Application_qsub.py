from AAV.Sequence import Reader, SeqCounter, Trimmer, Writer, BarcodeMapper as bm
from AAV.Utilities import YamlReader as yr
import time
from collections import defaultdict
import glob
from os import listdir

class Application:
    def __init__(self, arg1, arg2):
        print("Application starts!")
        self.count_dict = defaultdict()
        self.control_count_dict = defaultdict()
        self.file_in_path = arg1
        self.file_out_path = arg2

    def read_file(self, file_path):
        r = Reader.Reader(file_path)
        return r.parse_fastq()
        # return r.parse_fastq_seq()

    def trim_seq(self, seq_gen, min_len):
        t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC')
        t.set_min_len(min_len)
        t.set_phred_threshold(30)
        for seq in seq_gen:
            t.trim(seq)
            yield t.get_trimmed_seq()

    def count_seq(self, seq_gen):
        c = SeqCounter.SeqCounter(seq_gen)
        # return c.count_unique()
        c.count_unique2()
        # return c.count_dict # testing
        # return c.count_unique3()
        # return c.count_unique4()
        self.count_dict = c.count_dict
        self.control_count_dict = c.control_count_dict

    def binary_conversion(self, seq_dict, lib_num):
        bar = bm.BarcodeMapper()
        reader = yr.YamlReader()
        data = reader.read_yaml(lib_num)


        for d in data:
            bar.set_barcode_dict(d[yr.BarcodeYaml.BARCODE_DICT.value])
            bar.set_barcode_array(d[yr.BarcodeYaml.BARCODE_ARRAY.value])
            bar.set_barcode_libName(d[yr.BarcodeYaml.LIBNAME.value])
            bar.set_barcode_libSize(d[yr.BarcodeYaml.LIBSIZE.value])


        # count_binary_dict= bar.sum_binary_count(seq_dict, bar.barcode_libName, bar.barcode_libSize)
        bar.sum_binary_count(seq_dict, bar.barcode_libName, bar.barcode_libSize)
        # count_binary_dict = bar.ordered_bin_seq_count_dict_log2
        count_binary_dict = bar.ordered_bin_seq_count_dict # raw counts
        return count_binary_dict

    def write_file(self, out_file, seq_dict, title_list):
        w = Writer.Writer()
        w.set_out_path(out_file)
        w.write_dict(seq_dict, title_list)

a = Application()

def init_args(arg1, arg2):
    a.set_file_in_path(arg1)
    a.set_file_out_path(arg2)

def main():
    # a = Application(file_in_path='', file_out_path='')
    '''
    seq_gen = a.read_file(a.file_in_path)
    trimmed_seq_gen = a.trim_seq(seq_gen, 0)
    time0 = time.time()


    count_seq_dict = a.count_seq(trimmed_seq_gen)
    count_binary_dict = a.binary_conversion(count_seq_dict)

    # print(count_binary_dict)
    # print(count_binary_dict['Anc80BC_1953'])
    a.write_file(a.file_out_path, count_binary_dict)
    # print(type(count_binary_dict))
    time1 = time.time() - time0
    print(time1)
    '''

    seq_gen = a.read_file(a.file_in_path)
    trimmed_seq_gen = a.trim_seq(seq_gen, 0)
    time0 = time.time()

    a.count_seq(trimmed_seq_gen)
    lib_list = [80]
    for l in lib_list:
        count_binary_dict = a.binary_conversion(a.count_dict, l)
        a.write_file(a.file_out_path + a.file_in_path.split('/')[-1] + 'Anc_' + str(l) + '.csv', count_binary_dict, \
                     ['Barcode_index', a.file_in_path.split('/')[-1][0:-6]])
    a.write_file(a.file_out_path + a.file_in_path.split('/')[-1] + '_Control.csv', a.control_count_dict, \
                 ['Barcode_index', a.file_in_path.split('/')[-1][0:-6]])
    # count_binary_dict = a.binary_conversion(count_seq_dict, 84)
    # a.write_file("data/20180926/output/Anc84-1Hamilton_S2_L001_R1_001_new_test_anc84.csv", count_binary_dict)
    time1 = time.time() - time0
    print(time1)

if __name__ == '__main__':
    main()
