"""
from src.return_path import delete_link_repo
from src.return_path import save_directory
from src.tree import repo_tree, create_mermaid
from src.chunking import processor
from src.embedding import embedding
from src.llm_query import chatbot
import json
import sys
import os

user_input = sys.argv[1]
folder_path = save_directory(user_input)

os.makedirs("data/outputs", exist_ok = True)
with open("data/outputs/meta.json", "w") as file:
    json.dump({"folder_path": str(folder_path)}, file)

repo_tree.run()
processor.run()
embedding.run()
chatbot.run()
delete_link_repo(user_input, folder_path)
"""

from src.tree import create_mermaid
create_mermaid.run()