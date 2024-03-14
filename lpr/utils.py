import numpy as np
import pandas as pd

def excel2questions(file_path):
    df = pd.read_excel(file_path)

    questions = df['head'].to_list()

    return questions

def quetions2excel(questions, file_path):
    df = pd.DataFrame(questions, columns=['head'])

    df.to_excel(file_path, index=False)

def read_sheets(file_path, sheets_name):
    dfs = pd.read_excel(file_path, sheet_name=sheets_name)
    return dfs
