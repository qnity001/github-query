from pathlib import Path
from rich.tree import Tree
from rich.console import Console
import sys
from load_filter import filter

extensions, files = filter("filters.json")

##### FUNCTIONS ######

# Creates a tree and returns a dictionary
def create_tree(path):
    tree = {}
    for element in path.iterdir():
        if element.is_dir(): # if the item is a folder
            tree[element.name] = create_tree(element)
        elif element.is_file():
            if element.name not in files:
                for ex in extensions:
                    if element.name.endswith(ex):
                        tree[element.name] = None
                continue
            tree[element.name] = None
    return tree

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
folder_path = Path(input("Enter the root directory path: "))

if folder_path.exists() and folder_path.is_dir():
    print("User input is correct")

else:
    print("User input is invalid")
    sys.exit(1)

console = Console()
console.print(display_tree(create_tree(folder_path)))