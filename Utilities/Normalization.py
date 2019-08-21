import pandas as pd
import numpy as np
from os import listdir
from os import path
import os
import math

class Normalization:
    def __init__(self):
        self.file_path = ''
        # read files from a folder and get a list of data frames
        self.df_list = []
        self.normalize_step = 0
        self.df_list_norm = []
        self.output_path = ''
        self.total_sum = 0

        # collecting sample files grouped by Control file as array of array of array[filename, df]
        self.anc_lib_sets = []

    def read_files_with_control(self):
        self.df_list = [[filename, pd.read_csv(self.file_path + filename)] for filename in os.listdir(self.file_path)
                        if filename[-4:] == ".csv" and os.path.isfile(self.file_path + filename)]
        temp_list = []
        for x in self.df_list:
            temp_list.append(x)
            if(x[0].rsplit('_', 1)[1] == "Control.csv" or x[0].rsplit('_', 1)[1] == "control.csv"):
                self.anc_lib_sets.append(temp_list)
                temp_list = []

    def read_files_without_control(self):
        self.df_list = [[filename, pd.read_csv(self.file_path + filename)] for filename in os.listdir(self.file_path)
                        if filename[-4:] == ".csv" and os.path.isfile(self.file_path + filename)]

        temp_list = []
        first_file_name = self.df_list[0][0].rsplit('_', 1)[0]
        for x in self.df_list:
            if(x[0].rsplit('_', 1)[0] == first_file_name):
                temp_list.append(x)
            else:
                self.anc_lib_sets.append(temp_list)
                temp_list = []
                temp_list.append(x)
                first_file_name = x[0].rsplit('_', 1)[0]


    def normalize_new(self):
        group_total_counts = 0
        counts_anc83_1 = 0
        for x in self.anc_lib_sets:
            df_norm = pd.DataFrame()
            for y in x:
                if (y[0].rsplit('_', 1) == 'Anc83_1.csv'):
                    count = 0
                    for z in y[1]:
                        temp = int(count / 8)
                        if temp % 2 == 1:
                            counts_anc83_1 += z
                        count += 1
                    group_total_counts += counts_anc83_1
                else:
                    group_total_counts += sum(y[1].iloc[:, 1])

            # creating normalized files
            for y in x:
                df_norm = y[1]
                df_norm.iloc[:, 1] = np.log2((df_norm.iloc[:, 1] + 0.5) / (group_total_counts + 1) * 1000000)
                df_norm.to_csv(self.file_path + self.output_path + "_norm.".join(y[0].split('.')),
                               sep=',', index=False)

            group_total_counts = 0
            counts_anc83_1 = 0


    # read files and detect the numbers of controls, so we can normalize them by groups
    def read_files(self):
        self.df_list = [[filename, pd.read_csv(self.file_path + filename)] for filename in os.listdir(self.file_path)
                        if filename[-4:] == ".csv" and os.path.isfile(self.file_path + filename)]


        num_of_controls = sum('Control' in x for x in listdir(self.file_path))
        num_of_files = len(self.df_list)
        if (num_of_controls != 0):
            if ((num_of_files % num_of_controls) == 0):
                self.normalize_step = int(num_of_files / num_of_controls)
        elif (num_of_controls == 0 and num_of_files != 0):
            print("Normalizing data without controls!")
        else:
            print("Please check the folder!")
            exit()

    def create_output_folder(self):
        if not path.exists(self.file_path + self.output_path):
            os.mkdir(self.file_path + self.output_path)

    def normalize(self):
        # total_counts = 0
        df_list_len = len(self.df_list)
        for i in range(0, df_list_len, self.normalize_step):
            group_total_counts = 0
            df_norm = pd.DataFrame()
            for j in range(self.normalize_step):
                group_total_counts += sum(self.df_list[i + j][1].iloc[:, 1])
            for k in range(self.normalize_step):
                df_norm = self.df_list[i + k][1]
                df_norm.iloc[:, 1] = np.log2((df_norm.iloc[:, 1] + 0.5) / (group_total_counts + 1) * 1000000)
                df_norm.to_csv(self.file_path + self.output_path + "_norm.".join(self.df_list[i + k][0].split('.')),
                               sep = ',', index = False)
                # print(df_norm)

    def normalize_no_control(self):
        df_list_len = len(self.df_list)
        for i in range(df_list_len):
            df_norm = pd.DataFrame()
            df_norm = self.df_list[i][1]
            df_norm.iloc[:, 1] = np.log2((df_norm.iloc[:, 1] + 0.5) / (sum(df_norm.iloc[:, 1])+ 1) * 1000000)
            df_norm.to_csv(self.file_path + self.output_path + "_norm.".join(self.df_list[i][0].split('.')),
                           sep = ',', index = False)

    # normalize each file individually in a folder
    def normalize_individual(self):
        df_list_len = len(self.df_list)
        for i in range(0, df_list_len):
            df_norm = self.df_list[i][1]
            df_norm.iloc[:, 1] = np.log2((df_norm.iloc[:, 1] + 0.5) / (sum(df_norm.iloc[:, 1]) + 1) * 1000000)
            df_norm.to_csv(self.file_path + self.output_path + "_norm.".join(self.df_list[i][0].split('.')),
                               sep = ',', index = False)

def main():
    norm = Normalization()
    norm.file_path = '../data/20190712/output/for_normalization/'
    norm.output_path = 'normalized_new/'
    norm.create_output_folder()
    # norm.file_path = '../data/20180816/output/'
    # norm.read_files()
    # norm.normalize()
    # norm.normalize_no_control()
    # norm.normalize_individual()
    norm.read_files_with_control()
    norm.normalize_new()

if __name__ == '__main__':
    main()
