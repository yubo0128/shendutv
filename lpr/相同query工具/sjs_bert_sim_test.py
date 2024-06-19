import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import random
import json

# Function to encode sentences using BERT
def encode_sentence(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Function to find the closest query
def find_closest_query(new_query, queries_dict, query_embeddings, tokenizer, model):
    new_query_embedding = encode_sentence(new_query, tokenizer, model)
    similarities = {key: np.dot(new_query_embedding, embedding.T) / (np.linalg.norm(new_query_embedding) * np.linalg.norm(embedding)) for key, embedding in query_embeddings.items()}
    closest_key = max(similarities, key=similarities.get)
    closest_value = queries_dict[closest_key]
    return closest_key, closest_value, similarities[closest_key]

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
queries_669 = df_669['标题'].tolist()

# Randomly select 100 queries from 肾结石X版本-669条.xlsx
random.seed(42)
random_queries = random.sample(queries_669, 100)

# Compute embeddings for the 2000 queries
queries_dict_2000 = {i: query for i, query in enumerate(queries_2000)}

print('='*25 + 'START ENCODING QUERY' + '='*25)
query_embeddings_2000 = {key: encode_sentence(value, tokenizer, model) for key, value in queries_dict_2000.items()}

# Match each random query to the closest query in 肾结石待匹配-2000多条xlsx.xlsx
results = []

print('='*25 + 'START MARCHING QUERY' + '='*25)
for query in random_queries:
    closest_key, closest_value, similarity = find_closest_query(query, queries_dict_2000, query_embeddings_2000, tokenizer, model)
    results.append([query, closest_value])

# Write the results to a new Excel file
result_df = pd.DataFrame(results, columns=['Random Selected Query', 'Matched Query'])
result_df.to_excel('result.xlsx', index=False)

print("Matching completed. Results saved to 'result.xlsx'.")
