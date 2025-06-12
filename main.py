from src.return_path import save_directory
import json

user_input = input("Enter the root directory path or GitHub link: ")
folder_path = save_directory(user_input)

with open("data/outputs/meta.json", "w") as file:
    json.dump({"repo_path": str(folder_path)}, file)