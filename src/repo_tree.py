import os
import sys

def create_tree(path):
    for root, dirs, files in os.walk(path):
        print(os.path.basename(root))
        for file in files:
            print(file)

# later argparse
folder_path = input("Enter the root directory path: ")

if not os.path.isdir(folder_path):
    print("Invalid folder path. Please try again.")
    sys.exit(1)

else:
    print("The input is correct")

create_tree(folder_path)