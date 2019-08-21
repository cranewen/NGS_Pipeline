import pandas as pd
import numpy as np
from os import listdir
from os import path
from collections import defaultdict
from functools import reduce
import os

class Contamination:
    def __init__(self):
        self.file_path = ''
        self.contam_file_out_path = ''
        self.file_out_path = ''
        self.file_name_list = []
        self.file_name_dict = defaultdict()
        self.contam_single_lib_list = []
        self.contam_all_list = []

    def set_file_path(self, file_path):
        self.file_path = file_path

    # get a list of files's name in the file_path
    def get_file_names(self):
        for fname in os.listdir(self.file_path):
            self.file_name_list.append(fname)

    # A dictionary with {'anc80': [file_list], 'anc110': [file_list], ...} structure
    def get_file_names_dict(self):
        for fname in self.file_name_list:
            if fname.split('_')[-1].split('.')[0] in self.file_name_dict:
                self.file_name_dict[fname.split('_')[-1].split('.')[0]].append(fname)
            else:
                self.file_name_dict[fname.split('_')[-1].split('.')[0]] = []

    def concat_files_with_same_lib(self):
        for key, value in self.file_name_dict.items():
            df_list = [pd.read_csv(self.file_path + v) for v in value]
            concat_df = reduce(lambda left, right: pd.merge(left, right, on='barcode_index'), df_list)
            concat_df.to_csv('../data/SN0175493/all/contam_output/' + key + '_contamination.csv',
                             sep = ',', index = False )
            # concat_df.to_csv('../data/SN0172627/output/contam_output/' + key + '_contamination.csv',
            #                  sep = ',', index = False )
            total_contam_per_lib = pd.DataFrame
            # concat_df.sum().to_csv('../data/SN0172627/output/contam_output/' + key + '_contamination1.csv',
            #                  sep = ',', index = False )

            # print(concat_df.sum(axis = 0, skipna = True).values)
            # self.contam_single_lib_list = concat_df.sum(axis = 0, skipna = True).values


    # Combine all the individual library contamination to one single file
    def combine_contamination_files(self):
        self.contam_file_out_path = self.file_path + 'contam_output/'



def main():
    contam = Contamination()

    # contam.set_file_path('../data/NOVA_SN0167511/ASP92/contamination/')
    contam.set_file_path('../data/SN0175493/all/contamination/')
    contam.get_file_names()
    contam.get_file_names_dict()
    contam.concat_files_with_same_lib()
    print(contam.file_name_dict)


if __name__ == '__main__':
    main()


