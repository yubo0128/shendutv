import requests
import json

from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_closest_query(new_query, queries_dict, model):
    # Prepare pairs of the new query and each value in the dictionary
    query_pairs = [[new_query, value] for value in queries_dict.values()]

    # Compute similarity scores for each pair
    similarities = model.predict(query_pairs)

    # Find the index of the highest similarity
    closest_index = np.argmax(similarities)

    # Get the key of the closest matching query
    closest_key = list(queries_dict.keys())[closest_index]
    closest_value = queries_dict[closest_key]

    return closest_key, closest_value, similarities[closest_index]

def find_closest_query_cos_sim(new_query, queries_dict, model):

    # Compute embeddings for the values in the dictionary
    queries = list(queries_dict.values())
    query_embeddings = model.encode(queries)

    # Compute the embedding for the new query
    new_query_embedding = model.encode([new_query])

    # Compute cosine similarity between the new query embedding and all the stored query embeddings
    similarities = cosine_similarity(new_query_embedding, query_embeddings).flatten()

    # Find the index of the highest similarity
    closest_index = np.argmax(similarities)

    # Get the key of the closest matching query
    closest_key = list(queries_dict.keys())[closest_index]
    closest_value = queries_dict[closest_key]

    return closest_key, closest_value, similarities[closest_index]

if __name__ == '__main__':
    '''
    查询肩周炎列表 k:v
    '''
    payload = {}
    url = "http://online-hc.shendutv.com/prod-api/sdgather/syntheticModule/readExcle"
    response = requests.request("GET", url, data=payload)
    data = json.loads(response.text)

    # Load the pre-trained Cross-Encoder model
    # model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Compute embeddings for the values in the dictionary
    queries_dict = data['data']

    # Example usage
    new_query = "轻微肩周炎的症状"
    # closest_key, closest_value, similarity = find_closest_query(new_query, queries_dict, model)
    closest_key, closest_value, similarity = find_closest_query_cos_sim(new_query, queries_dict, model)

    print(f"Closest key: {closest_key}")
    print(f"Closest value: {closest_value}")
    print(f"Similarity: {similarity}")