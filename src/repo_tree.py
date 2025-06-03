from pathlib import Path

# Creates a tree and returns a dictionary
def create_tree(path):
    tree = {}
    for root, dirs, files in os.walk(path):
        root_name = os.path.basename(root)
        if root_name not in tree:  # Checks if a folder is there in tree or not  ## A folder is always a dict  
            tree[root_name] = {} # Create an empty dict for starters
        for file in files:
            print(file)

# later argparse
folder_path = Path(input("Enter the root directory path: "))

if folder_path.exists() and folder_path.is_dir():
    print("User input is correct")

else:
    print("User input is invalid")