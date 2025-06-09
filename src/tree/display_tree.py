# This program inputs a dictionary and displays it in a tree form

from rich.tree import Tree
from rich.console import Console

def save_display(tree: dict, print = None):
    # Print the root
    if print is None:
        print = Tree(f"[bold]Root Directory")

    for name, subtree in tree.items():
        if isinstance(subtree, dict):
            new = print.add(f"[blue]{name}")
            save_display(subtree, new)
        else:
            print.add(name)
    return print

def display(tree: dict):
    console = Console()
    console.print(save_display(tree))