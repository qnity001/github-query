from pathlib import Path
import sys
from load_filter import filter
import subprocess
import shutil
from display_tree import display

extensions, files, ignore = filter(Path(__file__).parent / "filters.json")

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

# Returns path to a temp directory
def parserepo():
    repo_root = Path(__file__).parent.parent
    temp_path = repo_root / "temp"
    temp_path.mkdir(exist_ok=True)
    temp_repo_path = temp_path / "temp_repo"
    temp_repo_path.mkdir(exist_ok=True)
    return Path(temp_repo_path)

# Error handling for shutil
def handle(func, path, exc_info):
    import stat
    import os
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

#### MAIN ####

# later argparse
user_input = input("Enter the root directory path or GitHub link: ")

temp_exists = False
if "github.com" in user_input:
    temp_exists = True
    temp_repo_path = parserepo() # received in Path format
    subprocess.run(["git", "clone", user_input, temp_repo_path])

else:
    folder_path = Path(user_input)
    if folder_path.exists() and folder_path.is_dir():
        print("User input is correct")

    else:
        print("User input is invalid")
        sys.exit(1)

if temp_exists:
    tree = create_tree(temp_repo_path)
    shutil.rmtree(str(temp_repo_path), onexc=handle)
else:
    tree = create_tree(Path(user_input))

display(tree)