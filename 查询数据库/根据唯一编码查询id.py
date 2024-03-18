from pypinyin import lazy_pinyin, Style
import time, os, json, pymysql, openpyxl

'''
数据合并
'''
def readData(sh):
    dataList = []
    for cases in list(sh.rows)[1:]:
        dataList.append([
                    cases[1].value,
                    cases[2].value,
                    ])
    return dataList

'''
数据查询
'''
def main(data):
    db = pymysql.connect(
        host='',
        user='',
        password='',
        db='shendu_new',
        charset='utf8mb4',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    cursor = db.cursor()
    print(data)
    for item in data:
        print(item)
        sqli = "select id from sd_douyin where aliyun_file = '%s'" % (item[0]+".mp4")
        print(sqli)
        cursor.execute(sqli)
        resultGroup = cursor.fetchone()
        print(resultGroup)
        if resultGroup != None:
            item.insert(0, resultGroup[0])
        else:
            item.insert(0, "")
    print(data)
    # 创建工作簿对象
    workbook = openpyxl.Workbook()
    # 选取默认的活动表格（sheet）
    sheet = workbook.active
    for i in data:
        sheet.append(i)
    workbook.save("./data/out.xlsx")



if __name__ == '__main__':
    wb = openpyxl.load_workbook("./data/表1-早泄-合成视频信息总表-20240315.xlsx")
    sh = wb.worksheets[0]
    data = readData(sh)
    main(data)
