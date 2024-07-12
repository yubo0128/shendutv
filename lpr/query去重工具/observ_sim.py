import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel


# Function to encode sentences using BERT
def encode_sentence(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()


# Function to compute similarity between a new query and a list of queries
def compute_similarity(income_query, queries, tokenizer, model):
    # Encode the income query
    income_embedding = encode_sentence(income_query, tokenizer, model)

    # Encode all queries from the list
    embeddings = [encode_sentence(query, tokenizer, model) for query in queries]

    # Compute similarities
    similarities = [cosine_similarity(income_embedding, embedding).flatten()[0] for embedding in embeddings]

    # Prepare the DataFrame
    data = {'Query': queries, 'Similarity': similarities}
    df = pd.DataFrame(data)

    return df


# Main function to read input, compute similarities, and save to Excel
if __name__ == '__main__':
    # Load pre-trained BERT model and tokenizer for Chinese
    model_name = 'bert-base-chinese'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Read queries from Excel file
    input_file = ''  # Path to the input Excel file
    df = pd.read_excel(input_file)
    queries = df['title'].tolist()

    # New income query
    income_query = ''  # Replace with your actual new query

    # Compute similarities
    similarity_df = compute_similarity(income_query, queries, tokenizer, model)

    # Save the output to an Excel file
    output_file = f'{income_query}comparison.xlsx'
    similarity_df.to_excel(output_file, index=False)

    print(f'Similarity comparison has been saved to {output_file}')
