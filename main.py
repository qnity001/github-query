from src.return_path import save_directory
from src.tree import repo_tree
from src.chunking import processor
from src.embedding import embedding
from src.retrieving import retriever
import json
import sys

user_input = sys.argv[1]
folder_path = save_directory(user_input)

with open("data/outputs/meta.json", "w") as file:
    json.dump({"folder_path": str(folder_path)}, file)

repo_tree.run()
processor.run()
embedding.run()
retriever.run()