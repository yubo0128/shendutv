import json
import requests
import numpy as np
import torch
import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity


# Function to encode sentences using BERT
def encode_sentence(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


# Function to group queries based on similarity threshold
def group_queries(queries, tokenizer, model, threshold=0.8):
    # Encode all queries
    embeddings = [encode_sentence(query, tokenizer, model) for query in queries]

    # Compute the pairwise cosine similarity matrix
    similarity_matrix = cosine_similarity(np.vstack(embeddings))

    # Group queries based on the similarity threshold
    groups = []
    used_indices = set()

    for i, query in enumerate(queries):
        if i in used_indices:
            continue
        group = [query]
        used_indices.add(i)
        for j in range(i + 1, len(queries)):
            if j not in used_indices and similarity_matrix[i][j] > threshold:
                group.append(queries[j])
                used_indices.add(j)
        groups.append(group)

    return groups


# Main function to read input, group queries, and save to Excel
if __name__ == '__main__':
    # Load pre-trained BERT model and tokenizer for Chinese
    model_name = 'bert-base-chinese'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Read queries from Excel file
    input_file = '基础表数据未做的-1770条-20240627.xlsx'  # Path to the input Excel file
    df = pd.read_excel(input_file)
    queries = df['title'].tolist()

    # Group the queries
    groups = group_queries(queries, tokenizer, model, threshold=0.98)

    # Prepare the output DataFrame
    max_group_size = max(len(group) for group in groups)
    output_data = [group + [''] * (max_group_size - len(group)) for group in groups]
    output_df = pd.DataFrame(output_data, columns=[f'query{i + 1}' for i in range(max_group_size)])

    # Save the output to an Excel file
    output_file = 'result.xlsx'
    output_df.to_excel(output_file, index=False)

    print(f'Grouped queries have been saved to {output_file}')
