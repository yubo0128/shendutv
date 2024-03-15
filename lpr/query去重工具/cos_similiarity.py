import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ..utils import *

'''
    使用LLM将questions转为sentence embedding，用cosine_similarity计算sentence embedding的相似度，
    相似度大于threshold的query为重复问题，输出所有不重复的问题
'''
def cos_sim(questions, threshold, model_name):
    # 加载预训练的sentence transformer模型
    model = SentenceTransformer(model_name)

    # 使用模型计算所有问题的embeddings
    embeddings = model.encode(questions, show_progress_bar=True)

    # 计算所有问题之间的cosinesimilarity
    cosine_sim = cosine_similarity(embeddings)

    unique_questions = []

    similar_indices = set()

    for i in range(len(questions)):
        if i in similar_indices:
            continue  # 如果这个问题已经与其他问题相似，则跳过
        # 将当前问题添加到唯一问题列表中
        unique_questions.append(questions[i])
        for j in range(i + 1, len(questions)):
            if cosine_sim[i, j] > threshold:
                similar_indices.add(j)  # 记录相似问题的索引

    return unique_questions

'''
    筛选逻辑与cos_sim一致，用于测试threshold
'''
def threshold_tune(thresholds, model_name, questions_file, output_file):
    questions = excel2questions(questions_file)
    df = pd.DataFrame(questions, columns=['original questions'])

    for threshold in thresholds:
        unique_questions = cos_sim(questions, threshold, model_name)

        df[f'threshold={threshold}'] = np.nan

        # Create a set for faster lookup
        set_B = set(unique_questions)

        # Update 'B_aligned' based on matches with 'A'
        for idx, row in df.iterrows():
            if row['original questions'] in set_B:
                df.at[idx, f'threshold={threshold}'] = row['original questions']

    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    '''threshold tuning'''
    # questions_file = '../filter 测试 2024 Feb/高血压query.xlsx'
    # thresholds = [0.9, 0.92, 0.94, 0.96, 0.98]
    # model_name = 'all-MiniLM-L6-v2'
    # # model_name = 'all-mpnet-base-v2'
    # output_file = '../filter 测试 2024 Feb/高血压filtered.xlsx'
    #
    # threshold_tune(thresholds, model_name, questions_file, output_file)

    model_name = 'all-MiniLM-L6-v2'
    questions_file = '../filter 测试 2024 Feb/高血压query.xlsx'
    output_file = '../filter 测试 2024 Feb/高血压filtered.xlsx'
    questions = excel2questions(questions_file)
    filtered_question = cos_sim(questions, 0.96, model_name)
    quetions2excel(filtered_question, output_file)








