import json
import requests
import numpy as np
import torch
from transformers import BertTokenizer, BertModel

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
    return closest_key, closest_value

if __name__ == '__main__':

    # Load pre-trained BERT model and tokenizer for Chinese
    model_name = 'bert-base-chinese'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Sample input JSON data
    queries_json = '{"1": "2mm肾结石多久排出", "2": "排肾结石好的方法有哪些", "3": "肾结石会引起腹胀吗"}'      # 入参
    incoming_queries_json = '{"incoming queries": ["肾结石5mm多久排出", "肾结石会出现恶心吗"]}'            # 入参

    # Parse the JSON data
    queries_dict = json.loads(queries_json)
    incoming_queries_list = json.loads(incoming_queries_json)["incoming queries"]

    # Compute embeddings for the queries
    query_embeddings = {key: encode_sentence(value, tokenizer, model) for key, value in queries_dict.items()}

    # Match each incoming query to the closest query
    results = {}

    for query in incoming_queries_list:
        closest_key, closest_value = find_closest_query(query, queries_dict, query_embeddings, tokenizer, model)
        results[query] = {'unique code': closest_key, 'match query': closest_value}

    # Output the results as a JSON string
    result_json = json.dumps(results, ensure_ascii=False, indent=4)
    print(result_json)



