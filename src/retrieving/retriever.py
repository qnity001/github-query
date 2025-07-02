import faiss
import json
from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy
import re
from src.retrieving.llm_classifier import predict_intent_llm

model = SentenceTransformer("BAAI/bge-code-v1")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

EXTENSIONS = ["py", "js", "php", "java", "ts", "html", "css", "cpp", "c"]

def extract_filenames(query):
    pattern = rf"\b[\w\-]+\.(?:{'|'.join(EXTENSIONS)})\b"
    return re.findall(pattern, query.lower())

def predict_intent(user_query):
    filenames = extract_filenames(user_query)
    if user_query.strip().lower() in filenames:
        return "file_search"
    else:
        return predict_intent_llm(user_query)

def get_chunks():
    with open("data/outputs/chunks.json") as file:
        return json.load(file)

def get_names():
    with open("data/outputs/name_chunks.json") as file:
        return json.load(file)

def search_names(query_vector, user_query, threshold=0.5, k=15):
    paths = []
    results = []
    names = get_names()
    index = faiss.read_index("data/outputs/faiss_names.index")

    D, I = index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]

    candidates = []
    for index, sim in zip(I[0], similarities):
        if sim >= threshold:
            name = names[index]
            candidates.append(name)

    rerank_inputs = [(user_query, name["name"]) for name in candidates]
    scores = reranker.predict(rerank_inputs)
    for chunk, score in zip(candidates, scores):
        chunk["rerank_score"] = score
    candidates = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    top_candidates = candidates[:3]

    paths = [chunk["file_path"] for chunk in top_candidates]
    results = get_chunk_content(paths)
    return results

def get_chunk_content(paths):
    chunks = get_chunks()
    results = []
    seen_chunks = set()
    for path in paths:
        for chunk in chunks:
            if chunk["file_path"] == path:
                chunk_id = chunk["chunk_id"]
                if chunk_id not in seen_chunks:
                    seen_chunks.add(chunk_id)
                    results.append(chunk["content"])
    return results

def search_chunks(query_vector, user_query, threshold=0.5, k=15):
    results = []
    chunks = get_chunks()
    index = faiss.read_index("data/outputs/faiss_chunks.index")

    D, I = index.search(numpy.array(query_vector), k)
    similarities = 1 - D[0]

    candidates = []
    for index, sim in zip(I[0], similarities):
        if sim >= threshold:
            chunk = chunks[index]
            candidates.append(chunk)

    rerank_inputs = [(user_query, chunk["content"]) for chunk in candidates]
    scores = reranker.predict(rerank_inputs)
    for chunk, score in zip(candidates, scores):
        chunk["rerank_score"] = score
    candidates = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    top_candidates = candidates[:3]

    seen_chunks = set()
    for chunk in top_candidates:
        if chunk["chunk_id"] not in seen_chunks:
            seen_chunks.add(chunk["chunk_id"])
            results.append(chunk["content"])

    return results

def run_search(user_query):
    intent = predict_intent(user_query)
    print(f"Intent: {intent}")
    query_vector = model.encode([user_query], normalize_embeddings=True)
    results = []

    if intent == "file_search":
        filenames = extract_filenames(user_query)
        names = get_names()

        if filenames:
            print(f"Detected filenames: {filenames}")

            for file in filenames:
                exact_matches = [n["file_path"] for n in names if file in n["file_path"]]
                results.extend(exact_matches)

            if not results:
                print("No exact matches found. Running fuzzy name search...")
                results = search_names(query_vector, user_query)

        else:
            print("No filenames detected. Running fuzzy name search...")
            results = search_names(query_vector, user_query)

    else:
        print("Running semantic search...")
        results = search_chunks(query_vector, user_query)

    return results

def run(user_query):
    results = run_search(user_query)
    return results
