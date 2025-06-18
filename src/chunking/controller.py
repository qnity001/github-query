from pathlib import Path
import json

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as fileread:
        return json.load(fileread)
    
# Split the directory on the basis of their priority and save their paths
# to two different lists
def split_files(tree: dict):
    splitter = [], []
    for name, meta_data in tree.items():
        if meta_data["type"] == "folder":
            split_files(meta_data["children"])
        elif meta_data["type"] == "file":
            if meta_data["priority"] == "True":
                splitter[0].append(Path(meta_data["path"]))
            else:
                splitter[1].append(Path(meta_data["path"]))
    return splitter 

def return_list():
    tree = get_tree()
    files = split_files(tree)
    return files