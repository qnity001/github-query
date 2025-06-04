from pathlib import Path
from rich.tree import Tree
from rich.console import Console
import sys
from load_filter import filter
import subprocess
import tempfile
import shutil

extensions, files, ignore = filter(Path(__file__).parent / "filters.json")

##### FUNCTIONS ######

# Creates a tree and returns a dictionary
def create_tree(path):
    tree = {}
    for element in path.iterdir():
        if element.is_dir(): # if the item is a folder
            if element.name in ignore:
                continue
            tree[element.name] = create_tree(element)
        elif element.is_file():
            if include(element.name):
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

# Display logic for testing only
def display_tree(tree: dict, print = None):
    # Print the root
    if print is None:
        print = Tree(f"[bold]Root Directory")

    for name, subtree in tree.items():
        if isinstance(subtree, dict):
            new = print.add(f"[blue]{name}")
            display_tree(subtree, new)
        else:
            print.add(name)
    return print

#### MAIN ####

# later argparse
user_input = input("Enter the root directory path or GitHub link: ")

if user_input.startswith("https://github.com/"):
    temp_path = tempfile.mkdtemp()
    subprocess.run(["git", "clone", user_input, temp_path])
    folder_path = Path(temp_path)

else:
    folder_path = Path(user_input)

if folder_path.exists() and folder_path.is_dir():
    print("User input is correct")

else:
    print("User input is invalid")
    sys.exit(1)

console = Console()
console.print(display_tree(create_tree(folder_path)))

shutil.rmtree(temp_path)