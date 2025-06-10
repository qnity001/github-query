from pathlib import Path
from return_path import save_directory, delete_link_repo
from filters.load_filter import filter
from display_tree import display
from create_tree_json import create_json

#### IMPORT FILTERS ###########

filters = filter(Path(__file__).parent / "filters" / "filters.json")
extensions = filters["extensions"]
files = filters["files"]
ignore = filters["ignore"]
priority = filters["priority_files"]

##### FUNCTIONS ######

# Creates a tree and returns a dictionary
def create_tree(path):
    tree = {}
    for element in path.iterdir():
        if element.is_dir(): # if the item is a folder
            if element.name in ignore or (element.name).startswith("."):
                continue
            tree[element.name] = create_tree(element)
        elif element.is_file():
            if include(element.name):
                tree[element.name] = False
                if element.name in priority:
                    tree[element.name] = True
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

#### MAIN ####

# later argparse
user_input = input("Enter the root directory path or GitHub link: ")
folder_path = save_directory(user_input)

tree = create_tree(folder_path)
display(tree)
create_json(tree)

delete_link_repo(user_input, folder_path)