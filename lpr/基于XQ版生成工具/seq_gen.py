import numpy as np
import pandas as pd
import math
import random
import tqdm

letter_dic = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J'
}
sheets_name = ['element set', 'original sequences']
fixed_heads = ['序号', 'title', '封面编号', 'XQ版本A', 'XQ版本正文']

'''
    读取file_path.xlsx中指定的sheets
    
    @:param file_path: string
    @:param sheets_name: list of strings
    
    @:return: list of DataFrame
'''
def read_sheets(file_path, sheets_name):
    dfs = pd.read_excel(file_path, sheet_name=sheets_name)
    return dfs

'''
    检查该行中所有'模块X'包含Q版元素的个数，Q版元素少于2个时，不对该行进行生成
    
    @:param row: Series (one row of DataFrame)
    
    @:return: bool
'''
def is_Q_less_2(row):
    Q_count = 0
    for column_name, value in row.items():
        if column_name == '序号' or column_name == '封面编号':
            continue
        if pd.isna(value):
            break
        elif isinstance(value, str) and 'Q' in value:
            Q_count += 1
    if Q_count < 2:
        return True
    return False

'''
    检查该行共有多少'模块X'，'模块X'数量少于5时，不对改行进行生成
    
    @:param row: Series (one row of DataFrame)
    @:return: bool
'''
def is_module_less_5(row):
    num_module = 0
    for column_name, value in row.items():
        if pd.isna(value):
            break
        if '模块' in column_name:
            num_module += 1
    if num_module < 5:
        return True
    return False


'''
    已包含在is_Q_less_2, 不应使用该函数
    
    @:param row: Series (one row of DataFrame)
    @:return: bool
'''
def is_Q_equal_0(row):
    Q_count = 0
    for column_name, value in row.items():
        if column_name == '序号' or column_name == '封面编号':
            continue
        if pd.isna(value):
            break
        elif isinstance(value, str) and 'Q' in value:
            Q_count += 1
    if Q_count == 0:
        return True
    return False

'''
    new_df只包含一行数据，检查new_df包含的这行是否在ori_df中重复
    
    @:param new_df: DataFrame contains only one row
    @:param ori_df: DataFrame
    
    @:return: bool, true if repreated
'''
def is_repeat(new_df, ori_df):
    ori_df_comp = ori_df.drop(fixed_heads, axis=1)
    new_df_comp = new_df.drop(fixed_heads, axis=1)
    # Ensure the dtypes for the columns used in the merge are the same
    for c in new_df_comp.columns:
        new_df_comp[c] = new_df_comp[c].astype(ori_df_comp[c].dtype)

    # try:
    df_merged = new_df_comp.merge(ori_df_comp, on=list(new_df_comp.columns), how='left', indicator=True)
    # except:
    #     raise ValueError
    # Check if all rows in dfB are found in dfA
    all_rows_exist = (df_merged['_merge'] == 'both').all()
    if all_rows_exist:
        return True
    return False


'''
    根据row的内容，从element_set中选取替换项，生成10条新的内容，并去重
    
    @:param row: Series, generate contain based on this row
    @:param element_set: DataFrame, 包含所有替换项
    @:param tmp_df: DataFrame, 用来查重
    @:param heads: list of string, 包含row的所有column name
    
    @:return tmp_df: 随机生成的不重复序列
'''
def generate_rand_seq(row, element_set, tmp_df, heads):
    i = 1
    for _ in range(10):
        dict_tmp = {key: np.nan for key in heads}
        for key, value in row.items():
            if not isinstance(value, str):
                break
            # use the same 序号
            if key in fixed_heads:
                dict_tmp[key] = value
                continue

            indices = np.where(element_set.values == value)
            # Extracting row and column indices
            row_indices, col_indices = indices[0], indices[1]
            if len(row_indices) == 0:
                dict_tmp[key] = value
                continue
            matching_row = element_set.loc[[row_indices[0]]]
            candidates = matching_row.values.flatten().tolist()
            if len(candidates) <= 1:
                dict_tmp[key] = value
                continue
            candidates = [x for x in candidates if isinstance(x, str)]

            dict_tmp[key] = random.choice(candidates)


        # check if the row exists in constructed df
        new_df = pd.DataFrame([dict_tmp])
        idx, r = next(new_df.iterrows())
        if is_repeat(new_df, tmp_df) or is_Q_equal_0(r) or is_module_less_5(r):
            continue
        new_df.at[0, '序号'] = new_df.at[0, '序号'] + f'-{letter_dic[i]}'
        i += 1

        # append to constructed_df
        tmp_df = pd.concat([tmp_df, new_df])

    return tmp_df


'''
    生成内容主函数
    
    @:param input_file_path: string
    @:param output_file_path: string
    
    @:return: None, save to output_file_path
'''
def generate_new(input_file_path, output_file_path):
    dfs = read_sheets(input_file_path, sheets_name)

    element_set = dfs['element set']
    ori_sequences = dfs['original sequences']
    heads = ori_sequences.columns.tolist()

    constructed_df = pd.DataFrame(columns=heads)

    for index, row in ori_sequences.iterrows():
        # construct a tmp df
        tmp_df = pd.DataFrame(columns=heads)
        # save current row, delete first row at end
        tmp_df = pd.concat([tmp_df, row.to_frame().T])

        # check if Q>=2
        if is_Q_less_2(row):
            continue

        tmp_df = generate_rand_seq(row, element_set, tmp_df, heads)
        # delete first row of tmp_df
        if len(tmp_df) <= 1:
            continue
        # delete first row and concate
        tmp_df = tmp_df.iloc[1:, :]
        constructed_df = pd.concat([constructed_df, tmp_df])

    constructed_df.to_excel(output_file_path)


if __name__ == "__main__":
    input_file_path = '../filter 测试 2024 Feb/XQ版本（慢性）前列腺炎-扩增基础信息表-李慧-20240307.xlsx'
    output_file_path = '../filter 测试 2024 Feb/前列腺炎-扩增表-刘沛然-20240311.xlsx'

    generate_new(input_file_path, output_file_path)


