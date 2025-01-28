import os
import pandas as pd
import numpy as np
import json
import torch
from sentence_transformers import SentenceTransformer
import faiss
import logging

logging.basicConfig(level=logging.INFO)

def read_excel(file_path):
    df = pd.read_excel(file_path)
    text_data = []
    for index, row in df.iterrows():
        row_data = " ".join([str(item) for item in row if not pd.isnull(item)])
        text_data.append(row_data)
    return text_data

def text_to_vector(text_data, model):
    embeddings = model.encode(text_data, convert_to_tensor=False)
    return np.array(embeddings).astype('float32'), text_data

def store_in_faiss(vectors, text_chunks, output_index, content_path):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Flat index for exact search
    index.add(vectors)  # Add vectors to the index
    faiss.write_index(index, output_index)
    logging.info(f"FAISS index saved to {output_index}")

    content_data = {str(i): text_chunks[i] for i in range(len(text_chunks))}
    with open(content_path, 'w') as f:
        json.dump(content_data, f, indent=4)
    logging.info(f"Content data saved to {content_path}")

if __name__ == "__main__":
    excel_file = r"D:\Rag-Vector-DB\assets\RPP_Dataset - Copy.xlsx"
    output_index = r"D:\Rag-Vector-DB\DB_Storage\vectors_faiss.index"
    content_path = r"D:\Rag-Vector-DB\DB_Storage\content.json"

    model = SentenceTransformer('all-MiniLM-L6-v2')
    excel_text_data = read_excel(excel_file)
    vectors, text_chunks = text_to_vector(excel_text_data, model)
    store_in_faiss(vectors, text_chunks, output_index, content_path)
    logging.info("Process completed successfully!")
