import pandas as pd
import numpy as np
import xlsxwriter

if __name__ == '__main__':

    # 创建一个新的Excel文件并添加一个工作表
    workbook = xlsxwriter.Workbook('./example.xlsx')
    worksheet = workbook.add_worksheet()

    # 定义格式
    red_format = workbook.add_format({'color': 'red'})
    normal_format = workbook.add_format()  # 默认的格式

    # 使用write_rich_string()方法写入具有不同格式的文本
    # 第一个参数是行号，第二个参数是列号，后面的参数是交替的文本和格式
    worksheet.write_rich_string(0, 0, 'This is ', red_format, 'red', normal_format, ' text.')

    # 关闭工作簿，释放内存
    workbook.close()