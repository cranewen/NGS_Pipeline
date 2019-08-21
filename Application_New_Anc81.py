from AAV.Sequence import Anc81NewMapper
from AAV.Sequence import Writer
from AAV.Sequence import Reader
from AAV.Sequence import Trimmer
from AAV.Sequence import Control
from collections import defaultdict
import time
from os import listdir
import os

class ApplicationAnc81:
    def __init__(self):
        print('Application anc81 starts!')
        self.anc81 = Anc81NewMapper.Anc81NewMapper()

    def read_file(self, file_path):
        self.record_gen = self.anc81.read_file(file_path)

    def write_file(self, out_file, seq_dict, title_list):
        w = Writer.Writer()
        w.set_out_path(out_file)
        w.write_dict(seq_dict, title_list)

    def read_2_dec(self, seq):
        self.anc81.read_2_decimal(seq)

    def trim_anc81(self, seq_records, min_len, quality_threshold):
        self.anc81.trimmed_seq_gen = self.anc81.trim_seq(seq_records, min_len, quality_threshold)

    def reverse_trim_anc81(self, seq_records, min_len, quality_threshold):
        self.anc81.trimmed_seq_gen = self.anc81.reverse_trim_seq(seq_records, min_len, quality_threshold)

    def count_seq(self):
        self.anc81.count_barcode()

    def sort_barcode(self):
        self.anc81.sort_barcode()


def main():
    app = ApplicationAnc81()
    app.anc81.set_barcode_dict(81)
    ctrl = Control.Control('control_20180322')
    input_data_path = 'data/20190712/'
    output_data_path = 'data/20190712/output/anc81_redesign/'
    file_list = listdir(input_data_path)
    # check if the output directory exists, if not, create it
    if output_data_path.split('/')[-1][0:-2] not in file_list:
        os.makedirs(output_data_path)
        for f in file_list:
            if f[-6:] == '.fastq':
                app.anc81.barcode_count_dict = defaultdict()
                app.anc81.control_count_dict = defaultdict()
                app.read_file(input_data_path + f)
                app.trim_anc81(app.anc81.fastq_seq_records, 0, 30)
                # app.reverse_trim_anc81(app.anc81.fastq_seq_records, 0, 30)
                time0 = time.time()
                for anc81_seq in app.anc81.trimmed_seq_gen:
                    app.read_2_dec(anc81_seq)
                    app.count_seq()
                    ctrl.count_controls(anc81_seq)
                    app.anc81.control_count_dict = ctrl.control_count_dict
                app.sort_barcode()
                app.write_file(output_data_path + f[0:-6] + '_Anc81' + '.csv', app.anc81.barcode_count_dict, ['barcode_index', f[0:-6]])
                app.write_file(output_data_path + f[0:-6] + '_Control.csv', app.anc81.control_count_dict, ['barcode_index', f[0:-6]])
                time1 = time.time() - time0
                print(time1)



if __name__ == '__main__':
    main()
