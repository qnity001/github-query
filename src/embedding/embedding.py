# Import sentence transformers
# Load the model

import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy

model = SentenceTransformer("BAAI/bge-code-v1")

def get_chunks():
    chunks_path = "data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)

def get_names():
    names_path = "data/outputs/name_chunks.json"
    with open(names_path) as file:
        return json.load(file)

def embed_chunks():
    chunks = get_chunks()
    texts = [chunk["content"] for chunk in chunks]
    index = store_chunks(texts)
    faiss.write_index(index, "data/outputs/faiss_chunks.index")

def embed_names():
    names = get_names()
    texts = [name["name"] for name in names]
    index = store_chunks(texts)
    faiss.write_index(index, "data/outputs/faiss_names.index")

def store_chunks(texts):
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(numpy.array(embeddings))
    return index

def run():
    embed_chunks()
    embed_names()
