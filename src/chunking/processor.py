import json
from transformers import AutoTokenizer
from src.config import get_repo_path
from src.chunking.controller import return_list, return_names
from src.chunking.chunking import return_chunks

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")
chunks = []
code_block = ""

def token_count(text: str):
    return len(tokenizer.encode(text))

def read_and_chunk(file_list: list, priority: bool, repo_root):
    for file_path in file_list:
        path = repo_root / file_path
        with open(path, "r") as file:
            content = file.read()
        
        # If the tokens are less than 1000, create a chunk
        if token_count(content) < 1000:
            chunk = {
                "token_count": token_count(content),
                "chunk_id": f"{file_path}:0",
                "file_path": str(file_path),
                "content": content,
                "priority": priority
            }
            chunks.append(chunk)
        
        else:
            print("High token count. Chunking...")
            with open(path, "rb") as file:
                content = file.read()
            captures = return_chunks(content, None)
            #create_chunk(captures, path, priority)
            for capture_name, nodes in captures.items():
                for node in nodes:
                    start, end = node.start_byte, node.end_byte
                    code_block = content[start:end].decode("utf-8", errors="ignore")
                    if token_count(code_block) < 1000:
                        chunk = {
                            "token_count": token_count(code_block),
                            "chunk_id": f"{file_path}:{1}",
                            "file_path": str(path),
                            "content": code_block,
                            "priority": priority
                        }
                        chunks.append(chunk)
                    
                    else:
                        captures_mini = return_chunks(content[start:end], node.type)
                        for capture_name, nodes in captures_mini.items():
                            for node in nodes:
                                start, end = node.start_byte, node.end_byte
                                code_block = content[start:end].decode("utf-8", errors="ignore")
                                chunk = {
                                    "token_count": token_count(code_block),
                                    "chunk_id": f"{file_path}:{1}",
                                    "file_path": str(path),
                                    "content": code_block,
                                    "priority": priority
                                }
                                chunks.append(chunk)


def create_chunk_json():
    json_chunks = json.dumps(chunks, indent = 4)
    with open("data/outputs/chunks.json", "w") as file:
        file.write(json_chunks)
    
def run():
    repo_root = get_repo_path()
    files = return_list()
    read_and_chunk(files[0], True, repo_root)
    read_and_chunk(files[1], False, repo_root)
    return_names()
    create_chunk_json()
