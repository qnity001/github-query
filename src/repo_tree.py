from pathlib import Path

# Creates a tree and returns a dictionary
def create_tree(path):
    tree = {}
    for element in path.iterdir():
        if element.is_dir(): # if the item is a folder
            tree[element.name] = create_tree(element)
        elif element.is_file():
            tree[element.name] = None
    return tree

# later argparse
folder_path = Path(input("Enter the root directory path: "))

if folder_path.exists() and folder_path.is_dir():
    print("User input is correct")

else:
    print("User input is invalid")

print(create_tree(folder_path))