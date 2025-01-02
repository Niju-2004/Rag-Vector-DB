Rag-VetBot
Empowering Farmers through a Bilingual Chatbot: Integrating NLP for Access to Traditional Herbal Treatment Practices for Livestock Management

Introduction:
This project aims to develop a bilingual chatbot that provides veterinary solutions using Natural Language Processing (NLP) for farmers. It leverages Retrieval-Augmented Generation (RAG) models to dynamically retrieve relevant content and ensure accurate responses.

Features:
1.NLP-based query understanding and response generation.
2.Uses a database of ethnoveterinary practices for remedies.
3.Easy-to-use web interface for non-technical users.

Folder Structure:
Rag-Vector-DB/
├── assets/                  # Datasets and reference materials
│   └── RPP_Dataset - Copy.xlsx
├── DB_Storage/              # Vector storage and indices
│   ├── content.json         # Automatically generated while running "vectorDB.py"
│   ├── vectors.hnsw         # Automatically generated while running "vectorDB.py"
│   ├── vectors.index        # Automatically generated while running "vectorDB.py"
│   └── vectors_hnswlib.bin  # Automatically generated while running "vectorDB.py"
├── src/                     # Source code
│   ├── app.py               # Main application file
│   ├── model.py             # RAG model logic
│   ├── vectorDB.py          # Vector database handler
│   ├── chatbot_errors.log   # Log file for errors
│   └── templates/           # HTML templates for web interface
│       └── index.html
├── .gitattributes           # Git attributes file
├── README.md                # Project documentation
└── requirements.txt         #requirements to be installed


Dataset:
Location: assets/RPP_Dataset - Copy.xlsx
Description: Contains information on various animal diseases, symptoms, herbal remedies, and treatments.

Key Files and Folders:
1) app.py: The main application script for running the chatbot server.
2) model.py: Core logic for query processing and response generation using embeddings.
3) vectorDB.py: Handles vector database operations like indexing and retrieval.
4) index.html: The web interface for user interaction.

Running the Project:
There are two ways to run the project:

1) Hosting on a Website:
Follow these steps to host the RAG-Veterinary chatbot on a website:
* Install the dependencies: pip install -r requirements.txt
* Run python src/vectorDB.py to initialize the vector database.
* Update the LLM API key in src/model.py.
* Run python src/app.py (this will automatically execute src/model.py).
* Access the chatbot at the generated localhost link.

2) Running in the Terminal:
Follow these steps to run the RAG-Veterinary chatbot in the terminal:
* Install the dependencies: pip install -r requirements.txt
* Run python src/vectorDB.py to initialize the vector database.
* Update the LLM API key in src/model.py.
* Run python src/model.py and provide the command line input.
* Responses will be generated in the terminal.
