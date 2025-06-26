# Create basic dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

queries = [
    "Where are all the PHP files located?",
    "Explain what the function does.",
    "Explain what the file does.",
    "What is the architecture of the project?", 
    "Where is the tree being created?",
    "What is the role of retriever.py?"
]

labels = [
    "file_search",
    "semantic_search", 
    "file_search", 
    "semantic_search",
    "semantic_search",
    "file_search"
]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2))),
    ('clf', LogisticRegression())
])

pipeline.fit(queries, labels)
joblib.dump(pipeline, "intents.joblib")
