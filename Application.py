from AAV.Sequence import Reader, SeqCounter, Trimmer, Writer, BarcodeMapper as bm
from AAV.Utilities import YamlReader as yr
import time
from collections import defaultdict
import glob
from os import listdir
import os

class Application:
    def __init__(self):
        print("Application starts!")
        self.count_dict = defaultdict()
        self.control_count_dict = defaultdict()

    def read_file(self, file_path):
        r = Reader.Reader(file_path)
        return r.parse_fastq()
        # return r.parse_fastq_seq()

    def trim_seq(self, seq_gen, min_len, quality_score):
        # t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC')
        t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'CGCATCCCGTG') # Anc83
        # t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC') # Anc83 redesigned trimmer
        # t.set_min_len(min_len)
        t.set_phred_threshold(quality_score)
        for seq in seq_gen:
            t.trim(seq)
            yield t.get_trimmed_seq()

    def reverse_trim_seq(self, seq_gen, min_len, quality_score):
        # t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC')
        t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'CGCATCCCGTG') # Anc83
        # t = Trimmer.Trimmer('CAGATCCTGCATGAAGCTT', 'GCGGCCGC') # Anc83 redesigned trimmer
        t.set_min_len(min_len)
        t.set_phred_threshold(quality_score)
        for seq in seq_gen:
            t.reverse_trim(seq)
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

def main():
    a = Application()
    # file_list = glob.glob()

    input_data_path = 'data/20190712/'
    output_data_path = 'data/20190712/output_anc83/'
    # output_data_path = 'data/20190213HamiltonrepNovaseq/output/contamination_check/anc83/'
    file_list = listdir(input_data_path)
    # check if the output directory exists, if not, create it
    if output_data_path.split('/')[-1][0:-2] not in file_list:
        os.makedirs(output_data_path)
    for f in file_list:
        if f[-6:] == '.fastq':
            seq_gen = a.read_file(input_data_path + f)
            ### if run reversed compliment seq, change it to reverse_trim_seq ###
            trimmed_seq_gen = a.trim_seq(seq_gen, 0, 30)
            # trimmed_seq_gen = a.reverse_trim_seq(seq_gen, 0, 30)
            time0 = time.time()

            a.count_seq(trimmed_seq_gen)
            # lib_list = [80, 110, 126]
            # lib_list = [80]
            lib_list = [83, '83_1']
            # lib_list = [80, 82, 84, 110, 113, 126, 127]
            for l in lib_list:
                count_binary_dict = a.binary_conversion(a.count_dict, l)
                a.write_file(output_data_path + f[0:-6] + '_Anc' + str(l) + '.csv', count_binary_dict, ['barcode_index', f[0:-6]])
            a.write_file(output_data_path + f[0:-6] + '_Control.csv', a.control_count_dict, ['barcode_index', f[0:-6]])
            time1 = time.time() - time0
            print(time1)


if __name__ == '__main__':
    main()
