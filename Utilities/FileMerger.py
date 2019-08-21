import csv
from os import listdir
from os.path import join
import pandas as pd
import numpy as np
from functools import reduce


class FileMerger:
    def __init__(self):
        self.file_list = []
        self.df_list = []
        self.control_list = []
        self.concat_df = None
        self.concat_control = None
        self.concat_df_norm = None
        self.concat_df_with_control = None
        self.concat_df_norm_with_control = None
        self.avg_df = None
        self.avg_df_with_control = None
        self.avg_df_norm = None
        self.avg_df_norm_with_control = None

    # read files in a path and set self.file_list as a generator
    # argument lib_num_str is a string of anc library number, say anc80 should be '80'
    def readFiles(self, file_path, lib_num_str):
        self.file_list = [f for f in listdir(file_path) if f[-4 - len(lib_num_str):] == (lib_num_str +'.csv')]
        # if lib_num_str is not 'Control':
        #     self.df_list = [pd.read_csv(join(file_path, f), sep=',') for f in self.file_list]
        # else:
        #     self.control_list = [pd.read_csv(join(file_path, f), sep=',') for f in self.file_list]

        self.df_list = [pd.read_csv(join(file_path, f), sep=',') for f in self.file_list]

    def normalize(self, column_data):
        return np.log2((column_data + 0.5) / (sum(column_data) + 1) * 1000000)

    def concatenate_dataframe(self):
        concat_df = reduce(lambda left, right: pd.merge(left, right, on='barcode_index'), self.df_list)
        # concat_control = reduce(lambda left, right: pd.merge(left, right, on='barcode_index'), self.control_list)
        concat_df_len = len(concat_df.columns)
        # concat_control_len = len(concat_control.columns)
        self.concat_df = concat_df
        # self.concat_control = concat_control
        concat_df_norm = concat_df.copy()
        for i in range(1, concat_df_len):
            # using concat_df.copy() to prevent change original concat_df
            concat_df_norm[concat_df.copy().iloc[:, i].name] = self.normalize(concat_df.copy().iloc[:, i])
        self.concat_df_norm = concat_df_norm

        # concat_df_with_control = pd.concat(concat_df, concat_control)
        # self.concat_df_with_control = concat_df_with_control

        # self.concat_df['avg'] = self.concat_df.mean(axis=1)

    def avg_dataframe(self, col1_name, col2_name):
        self.avg_df = pd.DataFrame({col1_name : self.concat_df.iloc[:, 0], col2_name : self.concat_df.mean(axis=1)})

    # def concat_control(self):


    # def write_file_csv(self, file_path, normalized = True):
    #     if (normalized == True):
    #         self.concat_df_norm.to_csv()

    def write2csv(self, file_path):
        self.avg_df.to_csv(file_path, sep=',', index=False)

def main():
    fm = FileMerger()
    fm.readFiles('../data/solid_quads_liver/solid_asp102_liver/', '80')
    # fm.readFiles('../data/20180816/output/', 'control')
    fm.concatenate_dataframe()
    # print(fm.normalize(fm.concat_df.iloc[:, 1]))
    # print(fm.concat_df_norm.mean(axis=1))
    fm.avg_dataframe('barcode_index', 'solid_asp102_liver_anc80')
    print(fm.avg_df)
    fm.write2csv('../data/solid_quads_liver/solid_asp102_liver/solid_asp102_liver_anc80.csv')
    # print(fm.concat_df)



if __name__ == '__main__':
    main()


