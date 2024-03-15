import xlsxwriter
import openpyxl
import copy
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义常量
BASIC_DATA = ["一、", "二、", "三、", "四、", "五、", "六、", "七、", "八、", "九、", "十、"]

# 返回比较的值
# 1.0 是全匹配  0 是全不匹配
def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


# 计算数据
def computes(c, string):
    rag = 0
    out = c[0:2]
    if out in string:
        rag = 2
    print(rag)
    if len(c) > 15:
        couA = c[rag:15]
    else:
        couA = c[rag:10]
    return couA


# 处理数据
def main(sh, arr):
    # 读取excel并组装数据
    for cases in list(sh.rows)[1:]:
        a = cases[4].value
        b = cases[5].value
        # print(b)
        # 把数据转换成A（左列）和B（右列）
        arr.append({
            "a": "\n".join([s for s in a.split("\n") if s]),
            "b": "\n".join([s for s in b.split("\n") if s])
        })
    # print(arr)
    index = 0
    for itemss in arr:
        s = itemss['a']
        n = itemss["b"]
        # if index == 0:
        #     index += 1
        #     continue
        for st in BASIC_DATA:
            logging.info('查询当前循环的数据'+ st)
            if st in s:
                i = s.index(st)
                sub_str = s[int(i):i + 15]
                # 第一种情况
                if sub_str in n:  # 带BASIC_DATAg的情况
                    print("查询到了111")
                    wz = n.index(sub_str)
                    ss = list(n)
                    ss.insert(wz, '\n')  # 在索引位置插入一个空格
                    n = ''.join(ss)
                    print("-------ssss---")
                    print(n)
                    print("-------ssss---")
                else:  # 不带一二三的情况
                    sub_str = s[int(i):i + 15]
                    print("查询出2222222")
                    print(sub_str)
                    sp = sub_str.split("。")
                    sub_str2 = s[int(i) + 2: (i + 2 + len(sp[0]))]
                    print("输出sub_str2sub_str2sub_str2")
                    print(sub_str2)
                    print("输出sub_str2sub_str2sub_str2")
                    print(n)
                    print(sub_str in n)
                    print("第几次" + str(index))
                    print(sub_str in "\n")
                    # 第二种情况
                    if sub_str in n:
                        wz = n.index(sub_str)
                        character = n[0:wz]
                        print("输出：")
                        character_list = [s for s in character.split("\n") if s]
                        print(character_list)
                        if len(character_list) != 1:
                            wz = wz-2
                        print(wz)
                        print("-------")
                        print(n[0:wz])
                        print("-------")
                        print("数字")
                        ss = list(n)
                        ss.insert(wz, '\n' + st)  # 在索引位置插入一个空格
                        n = ''.join(ss)
                        print("-------查询到了---")
                        print(n)
                        print("-------查询到了---")
                        continue
                    # 第三种情况
                    elif sub_str2 in n:
                        logging.info("是什么" + n)
                        logging.error('第三种情况')
                        # wz = n.index(sub_str2)
                        # ss = list(n)
                        # print(ss)
                        # ss.insert(wz, '\n')  # 在索引位置插入一个空格
                        # n = ''.join(ss)
                        # print(n)
            else:
                logging.error('不存在')
        nl = [s for s in n.split("\n") if s]
        print("000000000000000000")
        print(nl)
        itemss["b"] = "\n".join(nl)
        index += 1

    # 第四种情况
    for i in arr:
        # 把字符串拆分成数组
        a = i['a'].split("\n")
        b = i['b'].split("\n")
        bs = i['b']
        print("进入进入进入进入进入进入")
        if len(a) != len(b):
            print("------------_________--------")
            logging.info("BBBBB" + b[0])
            logging.info("AAAAA" + a[1])
            if a[1] in b[0]:
                wz = bs.index(a[1])
                ss = list(bs)
                ss.insert(wz, '\n')  # 在索引5的位置插入一个空格
                bs = ''.join(ss)
                print("1111111")
                print(bs)
                i['b'] = bs
            else:
                print("进入进入进入进入进入进入2222222222222")
                if a[0] in b[0]:
                    print("走包含了111111")
                    print(len(a[0]))
                    wz = bs.index(a[0])
                    ss = list(bs)
                    ss.insert(wz + len(a[0]), '\n')
                    bs = ''.join(ss)
                    print(bs)
                    i['b'] = bs
            print("输出BBBB")
            print(i['b'].split("\n"))
            a = [s for s in i['b'].split("\n") if s]
            i['b'] = '\n'.join(a)
        else:
            if a[0] in b[0]:
                print("AAAAAAAAA1111:" + a[1])
                print("BBBBBBBBB1111:" + b[0])
                print("CCCCCCCCC:" + str(len(a[0])))
                ss = list(bs)
                ss.insert(int(len(a[0])), '\n')  # 在索引5的位置插入一个空格
                bs = ''.join(ss)
                print(bs)
                i['b'] = bs
                print("8888888888888888888888888")
            else:
                print("99999999999999999999999999999999999")
            a = [s for s in i['b'].split("\n") if s]
            i['b'] = '\n'.join(a)

    # 第五种情况有些带了一二三有些没带说明前面的字符串不配需拼接上一二三
    for item in arr:
        a = item["a"].split("\n")
        b = item["b"].split("\n")
        for aa in a:
            for i in range(0, len(b)):
                # 截取后面10个字符或者15个字符超过95% 就加编号
                deep_copy_list = copy.deepcopy(aa)
                cou_a = computes(deep_copy_list, BASIC_DATA)
                cou_b = computes(b[i], BASIC_DATA)
                print("查询条数")
                logging.info("BBBBB" + cou_a)
                logging.info("AAAAA" + cou_b)
                print(jaccard_similarity(cou_a, cou_b))
                if jaccard_similarity(cou_a, cou_b) > 0.70:
                    sindex = aa[0:2]
                    print(sindex)
                    if sindex in BASIC_DATA:
                        if sindex in b[i]:
                            b[i] = b[i]
                        else:
                            b[i] = sindex + b[i]
                        print("进；来了")
        item["b"] = "\n".join(b)


# print(arr)
# exit()
# 导出和飘红
def output(arr, output_name):
    # 创建工作簿对象
    workbook = openpyxl.Workbook()
    # 选取默认的活动表格（sheet）
    sheet = workbook.active
    workbook.save(output_name)
    workbook = xlsxwriter.Workbook(output_name)
    worksheet = workbook.add_worksheet()

    # 定义格式
    red_format = workbook.add_format({'color': 'red'})
    normal_format = workbook.add_format()  # 默认的格式
    worksheet.write(0, 0, 'XQ版本正文')
    worksheet.write(0, 1, 'XQ版本扩增正文-20240307')

    # 循环
    for item in range(0, len(arr)):
        z = arr[item]
        a = z['a'].split("\n")
        b = z['b'].split("\n")
        print(b)
        final_data = []
        print("a循环匹配b 如果b")
        id = 0
        index_id = []
        for aStr in a:
            for i in range(0, len(b)):
                print(jaccard_similarity(aStr, b[i]))
                if jaccard_similarity(aStr, b[i]) > 0.85:
                    print("进入记录成功匹配的")
                    print("aaa:" + aStr)
                    print("bbb:" + str(id) +"内部循环id"+ str(i)+ "值：" + b[i])
                    #必须要得到B列的key值
                    index_id.append(i)
                    break
            id += 1
        print(index_id)
        # 组装数据并设置飘红
        for k in range(0, len(b)):
            if k in index_id:
                final_data.append(normal_format)
                if (k + 1) == len(b):
                    final_data.append(b[k])
                else:
                    final_data.append(b[k] + "\n")
            else:
                final_data.append(red_format)
                if (k + 1) == len(b):
                    final_data.append(b[k])
                else:
                    final_data.append(b[k] + "\n")
        print(final_data)
        # 输出并飘红
        # # 第一个参数是行号，第二个参数是列号，后面的参数是交替的文本和格式
        worksheet.write_rich_string(int(item + 1), 0, "\n".join(a), normal_format, " ")
        worksheet.write_rich_string(int(item + 1), 1, " ", *final_data)
    # 关闭工作簿，释放内存
    workbook.close()


if __name__ == '__main__':
    # 全数据测试
    # wb = openpyxl.load_workbook("/Users/yubo/Desktop/未命名文件夹/子宫肌瘤-扩增XQ版本拼接+正文-1037条20240313.xlsx")
    # 部分数据测试
    wb = openpyxl.load_workbook("./工作簿115.xlsx")
    sh = wb.worksheets[0]
    arr = []
    # 处理数据
    main(sh, arr)
    # 导出数据 参数一数据 参数二是导出文件名称
    output(arr, "output.xlsx")

