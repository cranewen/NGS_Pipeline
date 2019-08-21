import os
from os import path
import csv
import pandas as pd
import numpy as np

class Writer:
    def __init__(self):
        self.out_path = ''
        self.in_path = ''

    def set_out_path(self, out_path):
        self.out_path = out_path

    def set_in_path(self, in_path):
        self.in_path = in_path

    # writing file from a dictionary
    # arg headers is a string list
    def write_dict(self, seq_dict, headers=None):
        if not path.exists(self.out_path):
            with open(self.out_path, 'w') as f:
                w = csv.writer(f, delimiter=',', lineterminator='\n')
                if (headers != None):
                    w.writerow(headers)
                for k, v in seq_dict.items():
                    w.writerow([k, v])

    def write_data_frame(self, df):
        df.to_csv(self.out_path, sep=',', index=False)


