from pathlib import Path
from src.chunking.controller import return_list
import json
from transformers import AutoTokenizer
from src.config import get_repo_path
from tree_sitter_language_pack import get_parser

python_parser = get_parser("python")

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")
chunks = []
code_block = ""

def read_and_chunk(file_list: list, priority: bool, repo_root):
    for file_path in file_list:
        chunk_number = -1

        path = repo_root / file_path
        with open(path, "r") as file:
            content = file.read()
        
        # If the tokens are less than 1000, create a chunk
        if len(tokenizer(content)) < 1000:
            chunk = {
                "token_count": len(tokenizer.encode(content)),
                "chunk_id": f"{file_path}::{chunk_number + 1}",
                "file_path": str(path),
                "content": content,
                "priority": priority
            }
            chunks.append(chunk)
        
        # Else, call tree-sitter and find classes and functions
        else:
            with open(path, "rb") as file:
                content = file.read()
            tree = python_parser.parse(content)
            root = tree.root_node
            for child in root.children:
                if child.type in ["function definition", "class_definition"]:
                    start, end = child.byte_range
                    code_block = content[start:end].decode("utf-8", errors="ignore")
                    chunk = {
                        "token_count": len(tokenizer.encode(code_block)),
                        "chunk_id": f"{file_path}::{chunk_number + 1}",
                        "file_path": str(path),
                        "content": code_block,
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
