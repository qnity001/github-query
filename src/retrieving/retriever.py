import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy

def get_chunks():
    chunks_path = "../../data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)

model = SentenceTransformer("all-MiniLM-L6-v2")

user_query = input("Ask your query from codebase: ")
query_vector = model.encode([user_query], normalize_embeddings = True)

chunks = get_chunks()

# Search FAISS
index = faiss.read_index("../../data/outputs/faiss.index")
k = 2
D, I = index.search(numpy.array(query_vector), k)

# Print top chunks
top_chunks = [chunks[i] for i in I[0]]
for chunk in top_chunks:
    print(chunk["file_path"])