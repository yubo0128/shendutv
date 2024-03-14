import pandas as pd

# return index contains a str
def index_contains(str_list, string):
    i = 0
    for i in range(len(str_list)):
        if string in str_list[i]:
            return i
    return -1

def find_comma(string):
    for i in range(len(string)):
        if i >= 20:
            return -1
        if string[i] == '，' or string[i] == '。' or string[i] == '（':
            return i
    return -1

def add_serial_and_newline(input_file_path, output_file_path):
    audit_columns = ['XQ版本正文', 'XQ版本扩增正文-20240307']
    serial_num = ['一、', '二、', '三、', '四、']

    # read excel with two columns need to audit
    df = pd.read_excel(input_file_path, sheet_name=['XQ版本扩增拼接+正文 374条'])
    df = df['XQ版本扩增拼接+正文 374条']
    df = df[audit_columns]

    for index, row in df.iterrows():
        # ori_para = row['XQ版本正文']
        # auditing_para = row['XQ版本扩增正文-20240307']
        # loop through serial_number
        for serial in serial_num:
            if serial not in row['XQ版本正文']:
                break
            if serial in row['XQ版本扩增正文-20240307']:
                break
            # extract substring between serial and first comma
            start_index = row['XQ版本正文'].find(serial)
            end_index = find_comma(row['XQ版本正文'][start_index:])
            if end_index == -1:
                # mark red
                row['XQ版本扩增正文-20240307'] = '@' + row['XQ版本扩增正文-20240307']
                break
            end_index = start_index + end_index

            # substring need looking
            sub_str = row['XQ版本正文'][start_index + 2:end_index + 1]

            idx_in_auditing = row['XQ版本扩增正文-20240307'].find(sub_str)
            if idx_in_auditing == -1:
                row['XQ版本扩增正文-20240307'] = '@' + row['XQ版本扩增正文-20240307']
                break
            if row['XQ版本扩增正文-20240307'][start_index - 1] != '\n':
                # insert new line
                row['XQ版本扩增正文-20240307'] = row['XQ版本扩增正文-20240307'][:idx_in_auditing] + '\n' + serial \
                                                 + row['XQ版本扩增正文-20240307'][idx_in_auditing:]
                continue

            row['XQ版本扩增正文-20240307'] = row['XQ版本扩增正文-20240307'][:idx_in_auditing] + serial \
                                             + row['XQ版本扩增正文-20240307'][idx_in_auditing:]

    df.to_excel(output_file_path)

def mark_diff_para(input_file_path, output_file_path):


if __name__ == '__main__':
    input_file_path = '../filter 测试 2024 Feb/阳痿.xlsx'
    output_file_path = '../filter 测试 2024 Feb/audited.xlsx'



