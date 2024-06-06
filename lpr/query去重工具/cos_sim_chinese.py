from transformers import BertModel, BertTokenizer
import torch
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
    # Load pre-trained Chinese-BERT model
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertModel.from_pretrained('bert-base-chinese')

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

    # Tokenize and encode the queries
    inputs = tokenizer(queries, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

    # Calculate cosine similarity
    cosine_similarity_matrix = cosine_similarity(embeddings)

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

    # Add a "group" prefix with an index to each inner list
    data_with_group = [['group' + str(index + 1)] + sublist for index, sublist in enumerate(groups)]

    # Create a pandas DataFrame from the modified list of lists
    df = pd.DataFrame(data_with_group)

    # Save the DataFrame to an Excel file
    df.to_excel('output_with_groups.xlsx', index=False, header=False, engine='openpyxl')
