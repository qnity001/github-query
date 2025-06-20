# Import sentence transformers
# Load the model

import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy
from sklearn.preprocessing import normalize

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_chunks():
    chunks_path = "../../data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)
    
def embed():
    chunks = get_chunks()
    texts = [chunk["content"] for chunk in chunks]
    vectors = model.encode(texts, show_progress_bar = True) # Vectors from all the chunks
    normalized_vectors = normalize(numpy.array(vectors), axis = 1)
    
    # Store in FAISS Database as index
    dimension = normalized_vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(normalized_vectors)
    faiss.write_index(index, "../../data/outputs/faiss.index")

embed()