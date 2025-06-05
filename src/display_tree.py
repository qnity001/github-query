# This program inputs a dictionary and displays it in a tree form

from rich.tree import Tree
from rich.console import Console

def display(tree: dict, print = None):
    # Print the root
    if print is None:
        print = Tree(f"[bold]Root Directory")

    for name, subtree in tree.items():
        if isinstance(subtree, dict):
            new = print.add(f"[blue]{name}")
            display(subtree, new)
        else:
            print.add(name)
    return print

def dis(tree: dict):
    console = Console()
    console.print(display(tree))