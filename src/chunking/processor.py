from pathlib import Path
from src.chunking.controller import return_list
import json
from transformers import AutoTokenizer
from src.config import get_repo_path

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")

def read_and_chunk(file_list: list, priority: bool, repo_root):
    for file_path in file_list:
        chunk_number = -1
        path = repo_root / file_path
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        chunk = {
            "chunk_id": f"{file_path}::{chunk_number + 1}",
            "file_path": path,
            "content": content,
            "token_count": len(tokenizer.encode(content)),
            "priority": priority
        }
        print(chunk)
    
def run():
    repo_root = get_repo_path()
    files = return_list()
    print(files)
    print(repo_root)
