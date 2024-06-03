import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# from ..utils import *

'''
    使用LLM将questions转为sentence embedding，用cosine_similarity计算sentence embedding的相似度，
    相似度大于threshold的query为重复问题，输出所有不重复的问题
    
    @:param questions: list of strings
    @:param threshold: float [0, 1]
    @:param model_name: string (model in SentenceTransformer pkg)
    
    @:return: list of unique questions
'''
# def cos_sim(questions, threshold, model_name):
#     # 加载预训练的sentence transformer模型
#     model = SentenceTransformer(model_name)
#
#     # 使用模型计算所有问题的embeddings
#     embeddings = model.encode(questions, show_progress_bar=True)
#
#     # 计算所有问题之间的cosinesimilarity
#     cosine_sim = cosine_similarity(embeddings)
#
#     unique_questions = []
#
#     similar_indices = set()
#
#     for i in range(len(questions)):
#         if i in similar_indices:
#             continue  # 如果这个问题已经与其他问题相似，则跳过
#         # 将当前问题添加到唯一问题列表中
#         unique_questions.append(questions[i])
#         for j in range(i + 1, len(questions)):
#             if cosine_sim[i, j] > threshold:
#                 similar_indices.add(j)  # 记录相似问题的索引
#
#     return unique_questions
#
# '''
#     筛选逻辑与cos_sim一致，用于测试threshold
#
#     @:param thresholds: list of float in [0, 1]
#     @:param model_name: string (model in SentenceTransformer pkg)
#     @:param questions_file: string, file name that contains questions to be filtered
#     @:param output_file: string, file name that you want unique questions to be saved
#
#     @:return: None
# '''
# def threshold_tune(thresholds, model_name, questions_file, output_file):
#     questions = excel2questions(questions_file)
#     df = pd.DataFrame(questions, columns=['original questions'])
#
#     for threshold in thresholds:
#         unique_questions = cos_sim(questions, threshold, model_name)
#
#         df[f'threshold={threshold}'] = np.nan
#
#         # Create a set for faster lookup
#         set_B = set(unique_questions)
#
#         # Update 'B_aligned' based on matches with 'A'
#         for idx, row in df.iterrows():
#             if row['original questions'] in set_B:
#                 df.at[idx, f'threshold={threshold}'] = row['original questions']
#
#     df.to_excel(output_file, index=False)

if __name__ == '__main__':
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    import pandas as pd

    # List of queries
    queries = [
        '推拿可以治颈椎病吗', '按摩推拿能治疗颈椎病吗', '推拿能治颈椎病吗', '推拿对颈椎病管用吗',
        '颈椎病可以推拿治疗吗', '颈椎病推拿有用吗', '推拿能治疗颈椎病吗', '推拿可以治疗颈椎病吗',
        '推拿对颈椎病有什么用', '推拿治疗颈椎病的作用及原理是什么', '颈椎病可以推拿按摩吗',
        '颈椎病推拿治疗管用吗', '颈椎病做推拿有效吗', '按摩推拿对颈椎病的治疗有效吗',
        '推拿治疗颈椎病需要几个疗程', '颈椎病推拿几次能缓解', '颈椎病推拿一般一周几次',
        '有颈椎病能推拿吗', '椎动脉型颈椎病能推拿吗', '中医推拿可以治疗颈椎病吗',
        '推拿治疗颈椎病对手法有什么要求', '如何推拿治疗颈椎病手麻'
    ]

    # models: multi-qa-mpnet-base-dot-v1, all-mpnet-base-v2
    # Load pre-trained SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Convert queries to embeddings
    embeddings = model.encode(queries)

    # Calculate cosine similarity
    cosine_similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    # Set similarity threshold
    threshold = 0.98


    # Function to group similar queries
    def group_similar_queries(queries, cosine_similarity_matrix, threshold):
        groups = []
        visited = set()

        for i in range(len(queries)):
            if i not in visited:
                group = [queries[i]]
                visited.add(i)
                for j in range(i + 1, len(queries)):
                    if j not in visited and cosine_similarity_matrix[i][j] > threshold:
                        group.append(queries[j])
                        visited.add(j)
                groups.append(group)

        return groups


    # Group similar queries
    groups = group_similar_queries(queries, cosine_similarity_matrix, threshold)

    # Display the groups
    # for idx, group in enumerate(groups):
    #     print(f"Group {idx + 1}: {group}")


    # Add a "group" prefix with an index to each inner list
    data_with_group = [['group' + str(index + 1)] + sublist for index, sublist in enumerate(groups)]

    # Create a pandas DataFrame from the modified list of lists
    df = pd.DataFrame(data_with_group)

    # Save the DataFrame to an Excel file
    df.to_excel('output_with_groups.xlsx', index=False, header=False, engine='openpyxl')









