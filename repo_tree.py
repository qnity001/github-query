import os
import sys

# later argparse
folder_path = input("Enter the root directory path: ")

if not os.path.isdir(folder_path):
    print("Invalid folder path. Please try again.")
    sys.exit(1)

else:
    print("The input is correct")
