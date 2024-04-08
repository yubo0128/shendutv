import os
import numpy as np
import pandas as pd
import re
import json

modules = ['DY', 'LB', 'ZZ', 'WH', 'BY', 'YY', 'CB', 'JY', 'JC', 'ZL', 'SS', 'YW', 'YF', 'HL']

def all_files(path):
    files = os.listdir(path)
    return files

def get_dfs_from_files(files):
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)
    return dfs

def process_row(row, dic):
    arr = row.to_list()
    # ignore video ID
    arr = arr[1:]
    # ignore nan
    arr = [x for x in arr if type(x) == str]

    # filter out string has number
    filtered_arr = []
    for s in arr:
        if re.search('\d', s):
            filtered_arr.append(s)

    # filter out string contains GD or TT
    filtered_arr = [x for x in filtered_arr if "GD" not in x.split('-')[1]]
    filtered_arr = [x for x in filtered_arr if "TT" not in x.split('-')[1]]

    # filter the arr that it only contains second element, and the element contains substring in modules
    filtered_arr = [x.split('-')[1] for x in filtered_arr]
    filtered_arr = [x for x in filtered_arr if (x in modules)]

    if len(filtered_arr) <= 2:
        return

    # extracted the 2nd part (split by '-')
    occured = set()
    # find key of this row
    row_key = filtered_arr[0]
    occured.add(row_key)
    if row_key not in dic.keys():
        dic[row_key] = [[], [], []]

    # extract row values, append first 2 values
    value = ''
    for i in range(1, min(len(filtered_arr), 3)):
        if filtered_arr[i] not in occured:
            value = value + filtered_arr[i] + '-'
            occured.add(filtered_arr[i])
    value = value[:-1]

    # if value == 'PTYF':
    #     print('debugging here')

    # update dict
    if value == '':
        return
    elif value in dic[row_key][0]:
        idx = dic[row_key][0].index(value)
        dic[row_key][1][idx] += 1
    else:
        dic[row_key][0].append(value)
        dic[row_key][1].append(1)

def cal_prob(dic):
    for key in dic.keys():
        total = sum(dic[key][1])
        for occ in dic[key][1]:
            dic[key][2].append(occ/total)


if __name__ == '__main__':
    '''
        dict{
        key(module:str) : list of 3 lists [[following modules], [appearance], [prob]]
        }
    '''
    statis = dict()

    path = './X版本'
    files = all_files(path)
    # dfs = get_dfs_from_files(files)

    for file in files:
        df = pd.read_excel('./X版本/' + file)
        for index, row in df.iterrows():
            process_row(row, statis)

    # calculating the probability
    cal_prob(statis)

    # save dictionary
    with open("B_statis.txt", "w") as fp:
        json.dump(statis, fp)  # encode dict into JSON
    print("Done writing dict into .txt file")

    # write satis in an excel




