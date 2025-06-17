from src.config import get_repo_path
from pathlib import Path
import json

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as fileread:
        return json.load(fileread)
    
# Split the directory on the basis of their priority and save their paths
# to two different lists
def split_files(tree: dict):
    splitter = [], []
    for name, meta in tree.items():
        if meta["type"] == "folder":
            split_files(meta["children"])
        elif meta["type"] == "file":
            if meta["priority"] == "True":
                splitter[0].append(Path(meta["path"]))
            else:
                splitter[1].append(Path(meta["path"]))
    return splitter 

if __name__ == "__main__":
    repo_root = Path(get_repo_path())
    tree = get_tree()
    split_files(tree)
    priority, non_priority = split_files()
    