import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy

def get_chunks():
    chunks_path = "../../data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)

def get_names():
    names_path = "../../data/outputs/name_chunks.json"
    with open(names_path) as file:
        return json.load(file)
    
# Search name index in FAISS
def search_names(query_vector):
    names = get_names()
    name_index = faiss.read_index("../../data/outputs/faiss_names.index")
    k = 2
    D, I = name_index.search(numpy.array(query_vector), k)
    top_chunks = [names[i] for i in I[0]]
    for chunk in top_chunks:
       print(chunk["path"])

# Search chunks semantically in FAISS
def search_chunks(query_vector):
    chunks = get_chunks()
    name_index = faiss.read_index("../../data/outputs/faiss_chunks.index")
    k = 2
    D, I = name_index.search(numpy.array(query_vector), k)
    top_chunks = [chunks[i] for i in I[0]]
    for chunk in top_chunks:
        print(chunk["file_path"])

def run():
    model = SentenceTransformer("all-MiniLM-L6-v2") 
    user_query = input("Ask your query from codebase: ")
    query_vector = model.encode([user_query], normalize_embeddings = True)
    search_names(query_vector)
    search_chunks(query_vector)