from src.config import get_repo_path
from pathlib import Path
import json
from transformers import AutoTokenizer

priority = []
non_priority = []
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as fileread:
        return json.load(fileread)
    
def split_files(tree: dict):
    for name, meta in tree.items():
        if meta["type"] == "folder":
            split_files(meta["children"])
        elif meta["type"] == "file":
            if meta["priority"] == "True":
                priority.append(Path(meta["path"]))
            else:
                non_priority.append(Path(meta["path"]))

def process_files(files: list, root, priority: bool):
    test_chunks = []
    for file_path in files:
        path = root / file_path
        with open(path, "r", encoding="utf-8") as fileread:
            content = fileread.read()
            tokens = tokenizer.encode(content, truncation = False)
            if len(tokens) < 8192 and priority:
                test_chunks.append(content)
            elif len(tokens) < 4096 and not priority:
                test_chunks.append(content)
            else:
                print(f"{file_path} = Chunking required")
    return test_chunks

def run():
    repo_root = Path(get_repo_path())
    tree = get_tree()
    split_files(tree)
    print(priority)
    print(non_priority)
    print(process_files(priority, repo_root, True))
    print(process_files(non_priority, repo_root, False))