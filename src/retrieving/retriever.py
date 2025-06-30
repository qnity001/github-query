import faiss
import json
import re
import joblib
import numpy
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-code-v1")

EXTENSIONS = ["py", "js", "php", "java", "ts", "html", "css", "cpp", "c"]

def extract_filenames(query):
    pattern = rf"\b[\w\-]+\.(?:{'|'.join(EXTENSIONS)})\b"
    return re.findall(pattern, query.lower())

def predict_intent(user_query):
    pipeline = joblib.load("data/intents.joblib")
    return pipeline.predict([user_query])[0]

def get_chunks():
    with open("data/outputs/chunks.json") as file:
        return json.load(file)

def get_names():
    with open("data/outputs/name_chunks.json") as file:
        return json.load(file)

def search_names(query_vector, threshold=0.75, k=6):
    paths = []
    names = get_names()
    index = faiss.read_index("data/outputs/faiss_names.index")

    D, I = index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]

    for idx, sim in zip(I[0], similarities):
        if sim >= threshold:
            paths.append(names[idx]["path"])

    return paths

def search_chunks(query_vector, threshold=0.5, k=6):
    paths = []
    chunks = get_chunks()
    index = faiss.read_index("data/outputs/faiss_chunks.index")

    D, I = index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]

    for idx, sim in zip(I[0], similarities):
        if sim >= threshold:
            paths.append(chunks[idx]["file_path"])

    return paths

def run_search(user_query):
    intent = predict_intent(user_query)
    query_vector = model.encode([user_query], normalize_embeddings=True)
    paths = []

    if intent == "file_search":
        filenames = extract_filenames(user_query)
        names = get_names()

        if filenames:
            print(f"Detected filenames: {filenames}")

            for file in filenames:
                exact_matches = [n["path"] for n in names if file in n["path"]]
                paths.extend(exact_matches)

            if not paths:
                print("No exact matches found. Running fuzzy name search...")
                paths = search_names(query_vector)

        else:
            print("No filenames detected. Running fuzzy name search...")
            paths = search_names(query_vector)

    else:
        print("Running semantic search...")
        paths = search_chunks(query_vector)

    return paths

def run():
    while True:
        user_query = input("Ask your query from codebase: ")
        if not user_query.strip():
            break

        paths = run_search(user_query)
        if paths:
            print("Results:")
            for path in paths:
                print(path)
        else:
            print("No relevant results found.")
