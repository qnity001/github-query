from src.config import get_repo_path
from pathlib import Path
import json

priority = []
non_priority = []

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as file:
        return json.load(file)
    
def split_files(tree: dict):
    for name, meta in tree.items():
        if meta["type"] == "folder":
            split_files(meta["children"])
        elif meta["type"] == "file":
            if meta["priority"] == "True":
                priority.append(Path(meta["path"]))
            else:
                non_priority.append(Path(meta["path"]))


def run():
    repo_root = get_repo_path()
    tree = get_tree()
    split_files(tree)
    print(priority)
    print(non_priority)