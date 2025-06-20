# Import sentence transformers
# Load the model

import json
from sentence_transformers import SentenceTransformer

#model = SentenceTransformer("all-MiniLM-L6-v2")

def get_chunks():
    chunks_path = "../../data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)

chunks = get_chunks()
print(chunks)