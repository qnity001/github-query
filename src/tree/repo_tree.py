from pathlib import Path
from src.tree.filters.load_filter import filter
from src.tree.display_tree import display
from src.tree.create_tree_json import create_json
from src.config import get_repo_path

#### IMPORT FILTERS ###########

filters = filter(Path(__file__).parent / "filters" / "filters.json")
extensions = filters["extensions"]
files = filters["files"]
ignore = filters["ignore"]
priority = filters["priority_files"]

##### FUNCTIONS ######

# Creates a tree and returns a dictionary
def create_tree(path, repo_root):
    tree = {}

    for element in path.iterdir():
        if element.name in ignore or (element.name).startswith("."):
            continue
        
        if element.is_dir(): # if the item is a folder
            subtree = create_tree(element, repo_root)
            if subtree:
                tree[element.name] = {
                    "type": "folder", 
                    "path": str(element.relative_to(repo_root)),
                    "children": subtree
                }

        elif element.is_file() and include(element.name):
            tree[element.name] = {
                "type": "file",
                "priority": str(element.name in priority),
                "path": str(element.relative_to(repo_root))
            }
    return tree

# Checks for validity against filters.json
def include(name):
    if name in ignore:
        return False
    if name not in files:
        for ex in extensions:
            if name.endswith(ex):
                return True
        return False
    return True

def run():
    folder_path = get_repo_path()
    tree = create_tree(folder_path, folder_path)
    #display(tree)
    create_json(tree)