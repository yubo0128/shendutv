import json
import random
import re
import requests
import numpy as np
import pandas as pd


'''
    输入：B区标签，病种缩写
    输出：CD区拼接结果：开头+正文+结尾，标出CD区
    要求：1. 延展模块正文模块需要保证升序
         2. 选CD的模块通过概率抽
         3. 数字为9或者99的，不作为选项之一
         4. 单延展模块，总模块个数4-5随机
         5. 双延展模块，总模块6-8个随机
'''

modules = ['DY', 'LB', 'ZZ', 'WH', 'BY', 'YY', 'CB', 'JY', 'JC', 'ZL', 'SS', 'YW', 'YF', 'HL']
'''
    function get dataset of transition sentence
    module_name: 1 of 14 modules
    tag: 1 or 2, 1 is starting, 2 is ending
'''
def transition_modules(module_name, tag):
    url = f"http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-type-list?type={tag}&nameCode={module_name}"

    payload = {}
    response = requests.request("GET", url, data=payload)
    data = json.loads(response.text)
    if data['msg'] == '没有找到对应的数据':
        return ['']
    return data['data']


'''
    function get dataset of disease and its module
    module_name: 1 of 14 modules
'''
def main_modules(disease, module_name):
    payload = {}
    url = f"http://online-hc.shendutv.com/prod-api/sdgather/answer/answer-list/{disease}-{module_name}"
    response = requests.request("GET", url, data=payload)
    data = json.loads(response.text)
    data = [x for x in data['data'] if not (('99' in x) or ('9' in x))]
    return data


def draw_sample(B_module, B_stats):
    candidates, counts, _ = B_stats[B_module]
    # Calculate probabilities
    probabilities = np.array(counts) / sum(counts)

    sample_indices = np.random.choice(len(counts), size=1, replace=False, p=probabilities)
    return candidates[sample_indices[0]]


def generate_C(disease, CD):
    num_main = random.choice([2, 3])

    C_arr = []
    C_0 = random.choice(transition_modules(CD, 1))
    C_9 = random.choice(transition_modules(CD, 2))

    candidates = main_modules(disease, CD)

    # create candidates_dict
    candidates_dict = dict()
    for candidate in candidates:
        key = re.findall(r'\d+', candidate)[-1]         # AZB-YY-1, AZB-YY-Q1, key is 1

        if key not in candidates_dict.keys():
            candidates_dict[key] = []

        candidates_dict[key].append(candidate)

    # random sample
    randIndex = random.sample(range(len(candidates_dict.keys())), num_main)
    randIndex.sort()

    rand = []
    for i in randIndex:
        element_key = list(sorted(candidates_dict.keys()))[i]
        element = random.choice(candidates_dict[element_key])
        rand.append(element)

    # constract
    C_arr.append(C_0)
    C_arr.extend(rand)
    # not enough main module to sample
    if len(rand) < 2:
        return -1
    C_arr.append(C_9)

    C_arr = [item for item in C_arr if item != ""]

    return {'C': C_arr}

def generate_CD(disease, CD):
    C, D = CD.split('-')[0], CD.split('-')[1]

    C_arr = []
    D_arr = []
    C_0 = random.choice(transition_modules(C, 1))
    D_0 = random.choice(transition_modules(D, 1))
    D_9 = random.choice(transition_modules(D, 2))

    # selecting C main part -----------------------------------
    num_main = random.choice([2, 3])
    candidates = main_modules(disease, C)

    # create candidates_dict
    candidates_dict = dict()
    for candidate in candidates:
        key = re.findall(r'\d+', candidate)[-1]  # AZB-YY-1, AZB-YY-Q1, key is 1

        if key not in candidates_dict.keys():
            candidates_dict[key] = []

        candidates_dict[key].append(candidate)

    # random sample
    randIndex = random.sample(range(len(candidates_dict.keys())), num_main)
    randIndex.sort()

    rand = []
    for i in randIndex:
        element_key = list(sorted(candidates_dict.keys()))[i]
        element = random.choice(candidates_dict[element_key])
        rand.append(element)

    # constract
    C_arr.append(C_0)
    C_arr.extend(rand)
    # not enough main module to sample
    if len(rand) < 2:
        return -1

    C_arr = [item for item in C_arr if item != ""]

    # selecting D main part -----------------------------------
    num_main = random.choice([2, 3])
    candidates = main_modules(disease, D)

    # create candidates_dict
    candidates_dict = dict()
    for candidate in candidates:
        key = re.findall(r'\d+', candidate)[-1]  # AZB-YY-1, AZB-YY-Q1, key is 1

        if key not in candidates_dict.keys():
            candidates_dict[key] = []

        candidates_dict[key].append(candidate)

    # random sample
    randIndex = random.sample(range(len(candidates_dict.keys())), num_main)
    randIndex.sort()

    rand = []
    for i in randIndex:
        element_key = list(sorted(candidates_dict.keys()))[i]
        element = random.choice(candidates_dict[element_key])
        rand.append(element)

    # constract
    D_arr.append(D_0)
    D_arr.extend(rand)
    # not enough main module to sample
    if len(rand) < 2:
        return -1
    D_arr.append(D_9)
    D_arr = [item for item in D_arr if item != ""]

    return {'C': C_arr, 'D': D_arr}

'''
    generate CD sequence with disease, B module and B_sats
'''
def generate_CD_final(disease, B_module, B_stats):
    res = []
    # draw sample from B_stats
    CD = draw_sample(B_module, B_stats)
    num_module = len(CD.split('-'))
    if num_module == 0:
        raise NotImplemented
    elif num_module == 1:
        res = generate_C(disease, CD)
    elif num_module == 2:
        res = generate_CD(disease, CD)

    return res

def generate_CD_final_fix(disease, CD):
    res = []
    num_module = len(CD.split('-'))
    if num_module == 0:
        raise NotImplemented
    elif num_module == 1:
        res = generate_C(disease, CD)
    elif num_module == 2:
        res = generate_CD(disease, CD)

    return res

if __name__ == '__main__':
    x = generate_CD_final_fix('MXQLXY', 'YY')
    print(x)

    # rand = random.choice(list(range(15)))
    # print(str(rand) + '\n')
    #
    # disease = 'AZB'
    # CD_module = 'HL'
    # with open('B_statis.txt') as fh:
    #     B_stats = json.load(fh)


    # return -1 if not enough modules to sample, recall this function
    # otherwise, return a dictionary contains CD parts
    # raise exception if some modules do not enough samples, maybe try 10 times if still exception this indicating the disease does not have enough module
    # res = generate_CD_final(disease, B_module, B_stats)
    # print(res)
    # res = generate_CD_final_fix(disease, CD_module)
    #
    # print(res)