import os
import json
import faiss
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)

# 1. Configure Gemini API
genai.configure(api_key="AIzaSyDkpThDru0IGU_xWDl1NU1hjszPnKqSc5Y")  # Replace with your actual API key

# Generation settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

# 2. Initialize the Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# File paths
FAISS_INDEX_PATH = r"D:\Rag-Vector-DB\DB_Storage\vectors_faiss.index"
CONTENT_JSON_PATH = r"D:\Rag-Vector-DB\DB_Storage\content.json"

# Load Sentence Transformer model
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

def initialize_system():
    """Initializes the system by loading necessary models and data."""
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CONTENT_JSON_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
    return sentence_model, content, index

def query_system(user_query, sentence_model, index, content):
    """Process the user query, search FAISS, and generate response."""
    query_vector = np.array(sentence_model.encode([user_query], convert_to_tensor=False)).astype("float32")
    D, I = index.search(query_vector, k=3)  # Use `k` instead of `top_k`
    relevant_info = get_relevant_info(I[0], content)
    response = generate_gemini_response(relevant_info)
    return response, I, D, relevant_info

def get_relevant_info(indices, content_data):
    """Retrieve structured data from `content.json` based on FAISS indices."""
    results = []
    for idx in indices:
        str_idx = str(idx)
        if str_idx in content_data:
            results.append(content_data[str_idx])
    return results

def generate_gemini_response(results):
    """Generate response using Gemini AI."""
    prompt = f"Provide a detailed explanation for the following veterinary conditions:\n{json.dumps(results, indent=2)}"
    try:
        response = model.generate_content(prompt)  # Using the updated method
        return response.text if response else "No response from Gemini."
    except Exception as e:
        logging.error(f"Error generating content with Gemini: {str(e)}")
        return "Error generating response."

# This block will only run if model.py is executed directly (i.e., not imported by app.py)
if __name__ == "__main__":
    user_query = input("Enter your query: ")

    # Load FAISS index and content data
    sentence_model, content, index = initialize_system()

    # Process the query
    response, indices, distances, relevant_info = query_system(user_query, sentence_model, index, content)

    # Print the FAISS index and distances, relevant content, and Gemini response
    print("\nFAISS Search Results:")
    print("Indices:", indices)
    print("Distances:", distances)

    print("\n🔍 **Search Results:**")
    for res in relevant_info:
        print(json.dumps(res, indent=2))

    print("\n🌿 **Veterinary Chatbot Response:**")
    print(response)