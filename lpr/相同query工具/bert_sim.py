from transformers import BertTokenizer, BertModel
import torch
import numpy as np

import json
import requests

# Load pre-trained BERT model and tokenizer for Chinese
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

payload = {}
url = "http://online-hc.shendutv.com/prod-api/sdgather/syntheticModule/readExcle"
response = requests.request("GET", url, data=payload)
data = json.loads(response.text)
queries_dict = data['data']

# Encode sentences
def encode_sentence(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Compute embeddings for the dictionary values
query_embeddings = {key: encode_sentence(value, tokenizer, model) for key, value in queries_dict.items()}

def find_closest_query(new_query, queries_dict, query_embeddings, tokenizer, model):
    # Encode the new query
    new_query_embedding = encode_sentence(new_query, tokenizer, model)

    # Compute cosine similarities
    similarities = {key: np.dot(new_query_embedding, embedding.T) / (np.linalg.norm(new_query_embedding) * np.linalg.norm(embedding)) for key, embedding in query_embeddings.items()}

    # Find the key with the highest similarity
    closest_key = max(similarities, key=similarities.get)
    closest_value = queries_dict[closest_key]

    return closest_key, closest_value, similarities[closest_key]

# Example usage
new_query = "轻微肩周炎的症状"
closest_key, closest_value, similarity = find_closest_query(new_query, queries_dict, query_embeddings, tokenizer, model)
print(f"Closest key: {closest_key}")
print(f"Closest value: {closest_value}")
print(f"Similarity: {similarity}")
