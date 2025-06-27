# Create basic dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

queries = [
    "Where are all the PHP files located?",
    "Find all Python files in the utils folder.",
    "List every file with a .js extension.",
    "Show me where login.php is located.",
    "Is there a file named database.py?",
    "Locate retriever.py for me.",
    "How many HTML files are in the project?",
    "Where is app.module.ts defined?",
    "Where is create_tree.py?"

    "Explain what the function does.",
    "Explain what the file does.",
    "What is the architecture of the project?",
    "Where is the tree being created?",
    "What is the role of retriever.py?",
    "Help me understand the flow of the project.",
    "Explain how main.py interacts with other files.",
    "Describe how the modules connect.",
    "Walk me through the logic inside retriever.py.",
    "What happens when the project starts?",
    "How does data flow between these files?",
    "Explain the control flow of this project.",
    "How do the services interact in the codebase?"
]

labels = [
    "file_search",
    "file_search",
    "file_search",
    "file_search",
    "file_search",
    "file_search",
    "file_search",
    "file_search",

    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search",
    "semantic_search"
]


pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2))),
    ('clf', LogisticRegression())
])

pipeline.fit(queries, labels)
joblib.dump(pipeline, "../../data/intents.joblib")
print("Classifier trained")