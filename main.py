from src.return_path import save_directory
from src.tree import repo_tree
from src.chunking import chunking
import json

user_input = input("Enter the root directory path or GitHub link: ")
folder_path = save_directory(user_input)

with open("data/outputs/meta.json", "w") as file:
    json.dump({"folder_path": str(folder_path)}, file)

repo_tree.run()
chunking.run()