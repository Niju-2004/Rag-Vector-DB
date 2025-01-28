import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import google.generativeai as genai
import logging
import sys
from googletrans import Translator
import asyncio

logging.basicConfig(level=logging.ERROR, filename="chatbot_errors.log")

<<<<<<< HEAD
api_key = "AIzaSyDi2qr4oWGqnwgQlbqeY9xgd-4R9_o2Myo"
=======
api_key = "hasdfghjkoijhvergnuygfd"
>>>>>>> 994542bb863e54f3d290bfe760b0ed9ba1dd9e9d
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

def load_faiss_index(index_path):
    try:
        index = faiss.read_index(index_path)
        return index
    except Exception as e:
        logging.error(f"Error loading FAISS index: {e}")
        raise RuntimeError(f"Error loading FAISS index: {e}")

def load_content(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading content JSON: {e}")
        raise RuntimeError(f"Error loading content JSON: {e}")

def format_retrieved_content(content_item):
    if isinstance(content_item, dict):
        formatted_content = f"For treating {content_item.get('disease', 'the disease')}, a remedy includes {content_item.get('treatment', 'treatment details')}. "
        formatted_content += f"The recommended dosage is {content_item.get('dosage', 'dosage information')}."
        return formatted_content
    else:
        return content_item

async def detect_language(text):
    translator = Translator()
    detection = await translator.detect(text)
    return detection.lang

async def query_system(query, model, index, content):
    original_query = query
    # Check if the query is in Tamil
    lang = await detect_language(query)
    if lang == 'ta':
        # Translate the query from Tamil to English
        translator = Translator()
        query = await translator.translate(query, dest='en')
        query = query.text

    # Tokenize the query
    query_embedding = model.encode([query]).astype('float32')
    D, I = index.search(query_embedding, k=3) # Search for the top 3 nearest neighbors
    retrieved_content = []
    for label in I[0]:
        content_item = content.get(str(label), "No relevant context found.")
        retrieved_content.append(format_retrieved_content(content_item))
    combined_content = " ".join(retrieved_content)
    response = generate_response_with_gemini(query, combined_content)

    # If the original query was in Tamil, translate the response back to Tamil
    if lang == 'ta':
        response = await translator.translate(response, dest='ta')
        response = response.text

    return response

def initialize_system():
    sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    content_path = r"D:\Rag-Vector-DB\DB_Storage\content.json"
    index_path = r"D:\Rag-Vector-DB\DB_Storage\vectors_faiss.index"
    content = load_content(content_path)
    index = load_faiss_index(index_path)
    return sentence_model, content, index

async def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
        try:
            sentence_model, content, index = initialize_system()
            result = await query_system(query, sentence_model, index, content)
            print(result)
        except RuntimeError as e:
            print(e)
    else:
        print("Please provide a query as a command-line argument.")

if __name__ == "__main__":
    asyncio.run(main())