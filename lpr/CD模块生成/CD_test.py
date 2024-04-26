import json
import random
import re
import requests
import numpy as np
import pandas as pd
from CD_generator import generate_CD_final_fix

head = ['label', '序号', 'title', 'A', '正文', '模块1', '模块2', '模块3', '模块4', '模块5', '模块6', '模块7', '模块8', '模块9',
        '模块10', '模块11', '模块12', '模块13', '模块14', '模块15', '模块16', '模块17', '模块18', '模块19', '模块20']
def test_file(file_name, B_statis_file, B_module):
    df = pd.DataFrame(columns=head)
    query_df = pd.read_excel(file_name)

    # add one column named 'B_module - CD module'
    with open(B_statis_file) as fh:
        B_stats = json.load(fh)

    CD_candidates = B_stats[B_module]

    for i in range(len(CD_candidates[0])):
        CD = CD_candidates[0][i]

        sampled_queries = query_df.sample(n=3)

        CD_df = df_one_CD(sampled_queries, B_module, CD)
        df = pd.concat([df, CD_df], ignore_index=True)

    # write to file
    df.to_excel(f'{B_module}测试.xlsx')

def index_B(row_list):

    for i in range(len(row_list)-1, -1, -1):
        if isinstance(row_list[i], str) and (row_list[i] != ''):
            return i

    return -1

def df_one_CD(sampled_queries, B_module, CD_module):
    df = pd.DataFrame(columns=head)

    for index, row in sampled_queries.iterrows():
        row_list = row.tolist()
        row_list.insert(0, ' ')
        if len(row_list) < len(df.columns):
            # Extend the list with empty strings to match the DataFrame's number of columns
            row_list.extend([''] * (len(df.columns) - len(row_list)))
        df.loc[len(df)] = row_list

        # extract disease
        disease = row_list[1].split('-')[1]
        # extract index of B
        B_index = index_B(row_list)

        name_dict = {0:'A', 1:'B', 2:'C'}
        for i in range(3):
            # construct a row
            new_row = row_list[1:B_index+1]
            # add serial number
            new_row[0] = new_row[0] + '-' + name_dict[i]
            # insert B-C-D at begin
            new_row.insert(0, B_module + '-' + CD_module)

            # append CD at end
            try:
                CD = generate_CD_final_fix(disease, CD_module)
            except:
                new_row = new_row[:5]
                new_row.append('no enough samples')
                if len(new_row) < len(df.columns):
                    # Extend the list with empty strings to match the DataFrame's number of columns
                    new_row.extend([''] * (len(df.columns) - len(new_row)))
                df.loc[len(df)] = new_row
                continue

            for key in CD.keys():
                new_row.extend(CD[key])

            # concat the row to df
            if len(new_row) < len(df.columns):
                # Extend the list with empty strings to match the DataFrame's number of columns
                new_row.extend([''] * (len(df.columns) - len(new_row)))

            # Adding the list as a new row to the DataFrame
            # Method 1: Using loc with a new index
            df.loc[len(df)] = new_row

    return df

if __name__ == '__main__':
    test_file('ZL问题.xlsx', 'B_statis.txt', 'ZL')
