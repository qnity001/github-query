import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy
import joblib
import re

model = SentenceTransformer("all-MiniLM-L6-v2") 

def extract_filenames(query):
    EXTENSIONS = ["py", "js", "php", "java", "ts", "html", "css", "cpp", "c"]
    pattern = rf"\b[\w\-]+\.(?:{'|'.join(EXTENSIONS)})\b"
    return re.findall(pattern, query.lower())

def predict_intent(user_query):
    pipeline = joblib.load("data/intents.joblib")
    predicted_intent = pipeline.predict([user_query])[0]
    return predicted_intent

def get_chunks():
    chunks_path = "data/outputs/chunks.json"
    with open(chunks_path) as file:
        return json.load(file)

def get_names():
    names_path = "data/outputs/name_chunks.json"
    with open(names_path) as file:
        return json.load(file)
    
# Search name index in FAISS
def search_names(query_vector):
    paths = []
    names = get_names()
    name_index = faiss.read_index("data/outputs/faiss_names.index")

    threshold = 0.75
    k = 6

    D, I = name_index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]
    for index, sim in zip(I[0], similarities):
        if sim >= threshold:
            chunk = names[index]
            paths.append(chunk["path"])
    return paths

# Search chunks semantically in FAISS
def search_chunks(query_vector):
    paths = []
    chunks = get_chunks()
    name_index = faiss.read_index("data/outputs/faiss_chunks.index")

    threshold = 0.5
    k = 6

    D, I = name_index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]

    for index, sim in zip(I[0], similarities):
        print(sim)
        if sim >= threshold:
            chunk = chunks[index]
            paths.append(chunk["file_path"])
    return paths

def run():
    while True:
        user_query = input("Ask your query from codebase: ")
        if user_query == "":
            break
        intent = predict_intent(user_query)
        print(intent)
        query_vector = model.encode([user_query], normalize_embeddings = True)

        if intent == "file_search":
            names = get_names()
            filenames = extract_filenames(user_query)
            if filenames:
                for file in filenames:
                    paths = [n["path"] for n in names if file in n["path"]]

                    if not paths:
                        print("No exact match for filename, running fuzzy name search")
                        new_paths = search_names(query_vector)
                        paths.extend(new_paths)
        else:
            print("No file name match found. Running semantic search..")
            paths = search_chunks(query_vector)
        for path in paths:
            print(path)
