import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self):
        self.df_list = []

    def set_df_list(self, df_list):
        self.df_list = df_list

    # horizontal concatenate
    def column_concat(self, df_list):
        result = pd.concat(df_list, axis=1)
        return result

    # vertical concatenate
    def row_concat(self, df_list):
        result = pd.concat(df_list)
        return result

    # converting a dictionary to dataframe
    def convert_df(self, dict_data, header_list):
        df = pd.DataFrame.from_dict(dict_data, orient='index', columns=header_list)
        return df
