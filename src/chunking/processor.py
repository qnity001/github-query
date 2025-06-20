from pathlib import Path
from src.chunking.controller import return_list
import json
from transformers import AutoTokenizer
from src.config import get_repo_path

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")
chunks = []

def read_and_chunk(file_list: list, priority: bool, repo_root):
    for file_path in file_list:
        chunk_number = -1
        path = repo_root / file_path
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        chunk = {
            "token_count": len(tokenizer.encode(content)),
            "chunk_id": f"{file_path}::{chunk_number + 1}",
            "file_path": str(path),
            "content": content,
            "priority": priority
        }
        chunks.append(chunk)
    json_chunks = json.dumps(chunks, indent = 4)
    with open("data/outputs/chunks.json", "w") as file:
        file.write(json_chunks)
    
def run():
    repo_root = get_repo_path()
    files = return_list()
    read_and_chunk(files[0], True, repo_root)
    read_and_chunk(files[1], False, repo_root)
