from pathlib import Path
import json

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as fileread:
        return json.load(fileread)
    
# Split the directory on the basis of their priority and save their paths
# to two different lists
splitter = [], []
def split_files(tree: dict):
    for name, meta_data in tree.items():
        if meta_data["type"] == "folder":
            split_files(meta_data["children"])
        elif meta_data["type"] == "file":
            if meta_data["priority"] == "True":
                splitter[0].append(Path(meta_data["path"]))
            else:
                splitter[1].append(Path(meta_data["path"]))
    return splitter 

def return_names():
    names = []
    files = return_list()
    all_files = list(set(files[0] + files[1]))
    for path in all_files:
        name_chunk = {
            "name" : path.name,
            "file_path" : str(path)
        }    
        names.append(name_chunk)
    json_chunks = json.dumps(names, indent = 4)
    with open("data/outputs/name_chunks.json", "w") as file:
        file.write(json_chunks)

def return_list():
    tree = get_tree()
    files = split_files(tree)
    return files