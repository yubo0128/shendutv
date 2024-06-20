import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import random

# Function to encode sentences using BERT
def encode_sentence(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Function to find the closest query
def find_closest_query(new_query, queries_dict, query_embeddings, tokenizer, model):
    new_query_embedding = encode_sentence(new_query, tokenizer, model)
    similarities = {key: np.dot(new_query_embedding, embedding.T) / (np.linalg.norm(new_query_embedding) * np.linalg.norm(embedding)) for key, embedding in query_embeddings.items()}
    closest_key = max(similarities, key=similarities.get)
    closest_value = queries_dict[closest_key]
    return closest_key, closest_value

# Load pre-trained BERT model and tokenizer for Chinese
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Load the data from both Excel files
file_2000 = '肾结石待匹配-2000多条xlsx.xlsx'
file_669 = '肾结石X版本-669条.xlsx'

df_2000 = pd.read_excel(file_2000)
df_669 = pd.read_excel(file_669)

queries_2000 = df_2000['title'].tolist()
queries_669 = df_669[['序号', '标题']]

# Randomly select 500 queries from 肾结石待匹配-2000多条.xlsx
random.seed(42)
random_queries_2000 = random.sample(queries_2000, 1)

# Compute embeddings for the 500 random queries
queries_dict_2000 = {i: query for i, query in enumerate(random_queries_2000)}

print('='*25 + 'START ENCODING QUERY' + '='*25)
query_embeddings_2000 = {key: encode_sentence(value, tokenizer, model) for key, value in queries_dict_2000.items()}

# Prepare a dictionary to hold the matched results
matched_results = {row['序号']: [] for _, row in queries_669.iterrows()}

print('='*25 + 'START MATCHING QUERY' + '='*25)
for query in random_queries_2000:
    closest_key, closest_value = find_closest_query(query, {row['序号']: row['标题'] for _, row in queries_669.iterrows()},
                                                    {row['序号']: encode_sentence(row['标题'], tokenizer, model) for _, row in queries_669.iterrows()},
                                                    tokenizer, model)
    matched_results[closest_key].append(query)

# Prepare results for saving
results = []
for _, row in queries_669.iterrows():
    unique_code = row['序号']
    query = row['标题']
    matched_queries = matched_results.get(unique_code, [])
    result_row = [unique_code, query] + matched_queries
    results.append(result_row)

# Define column names dynamically based on the number of matched queries
max_matches = max(len(row) for row in results) - 2
columns = ['Unique Code', 'Query'] + [f'Matched Query {i+1}' for i in range(max_matches)]

# Write the results to a new Excel file
result_df = pd.DataFrame(results, columns=columns)
result_df.to_excel('result.xlsx', index=False)

print("Matching completed. Results saved to 'result.xlsx'.")
