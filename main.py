import os
import json
from src.tree import create_mermaid, repo_tree
from src.return_path import save_directory
from src.chunking import processor
from src.embedding import embedding
from src.llm_query import chatbot

def run(user_input):
    folder_path = save_directory(user_input)

    os.makedirs("data/outputs", exist_ok = True)
    with open("data/outputs/meta.json", "w") as file:
        json.dump({"folder_path": str(folder_path)}, file)

    repo_tree.run()
    create_mermaid.run()
    processor.run()
    embedding.run()
    chatbot.run("How is the code being retrieved?")