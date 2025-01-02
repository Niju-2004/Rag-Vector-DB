import os
import hnswlib
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import google.generativeai as genai
import logging
import sys

logging.basicConfig(level=logging.ERROR, filename="chatbot_errors.log")

api_key = "AIzaSyB0ThmyIFEC5H3XdpKjsAs2I0-4g8tgOrs"
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)


def generate_response_with_gemini(query, relevant_content):
    try:
        veterinary_prompt = "You are a veterinary expert. Provide a helpful response with accurate veterinary information in English. "
        query_with_prompt = veterinary_prompt + query
        response = model.generate_content([query_with_prompt, relevant_content])
        return response.text
    except Exception as e:
        logging.error(f"Error generating content with Gemini: {e}")
        return f"Error generating content with Gemini: {e}"


def load_hnswlib_index(index_path, dim):
    """Load HNSWlib index from the given path."""
    try:
        index = hnswlib.Index(space='cosine', dim=dim)
        index.load_index(index_path)
        return index
    except Exception as e:
        logging.error(f"Error loading HNSWlib index: {e}")
        raise RuntimeError(f"Error loading HNSWlib index: {e}")


def load_content(json_path):
    """Load content from a JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading content JSON: {e}")
        raise RuntimeError(f"Error loading content JSON: {e}")


def format_retrieved_content(content_item):
    """Format retrieved content into a meaningful sentence."""
    if isinstance(content_item, dict):
        formatted_content = f"For treating {content_item.get('disease', 'the disease')}, a remedy includes {content_item.get('treatment', 'treatment details')}. "
        formatted_content += f"The recommended dosage is {content_item.get('dosage', 'dosage information')}."
        return formatted_content
    else:
        return content_item


def query_system(query, model, index, content, top_k=3):
    """Retrieve and display relevant information for the user's query."""
    try:
        # Generate embedding for the query
        query_embedding = model.encode([query])
        labels, distances = index.knn_query(query_embedding, k=top_k)

        # Fetch content from the database using the retrieved labels
        retrieved_content = []
        for label in labels[0]:
            content_item = content.get(str(label), "No relevant context found.")
            retrieved_content.append(format_retrieved_content(content_item))

        # Combine the retrieved content into a single string
        combined_content = " ".join(retrieved_content)

        # Generate a response using the Gemini API
        return generate_response_with_gemini(query, combined_content)

    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return f"Error processing query: {e}"


def initialize_system():
    """Initialize the system components (model, content, and index)."""
    sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # File paths
    content_path = r"D:\Rag-Vector-DB\DB_Storage\content.json"
    index_path = r"D:\Rag-Vector-DB\DB_Storage\vectors_hnswlib.bin"
    dim = 384

    content = load_content(content_path)
    index = load_hnswlib_index(index_path, dim)
    return sentence_model, content, index


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        try:
            sentence_model, content, index = initialize_system()
            result = query_system(query, sentence_model, index, content)
            print(result)
        except RuntimeError as e:
            print(e)
    else:
        print("Please provide a query as a command-line argument.")
