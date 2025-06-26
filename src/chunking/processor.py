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

def create_chunk(content, path, chunk_count, priority):
    chunk = {
        "token_count": token_count(content),
        "chunk_id": f"{path}:{chunk_count}",
        "file_path": str(path),
        "content": content,
        "priority": priority
    }
    chunks.append(chunk)

def read_and_chunk(file_list: list, priority: bool, repo_root):
    for file_path in file_list:
        path = repo_root / file_path
        with open(path, "r") as file:
            content = file.read()
        
        chunk_count = 0

        # If entire file is < 1000 tokens, create a chunk
        if token_count(content) <= 1000:
            create_chunk(content, file_path, chunk_count, priority)
            continue
        
        # Per file
        with open(path, "rb") as file:
            content = file.read()
            captures = return_chunks(content, None)

            accumulated = ""
            for nodes in captures.values():
                for node in nodes:
                    start, end = node.start_byte, node.end_byte
                    code_block = content[start:end].decode("utf-8", errors="ignore")

                    # Check for a node if its less than 1000 tokens
                    if token_count(code_block) < 1000:
                        if token_count(code_block) + token_count(accumulated) > 1000:
                            create_chunk(accumulated, path, chunk_count, priority)
                            chunk_count += 1
                            accumulated = ""
                        accumulated += code_block + "\n"
                        continue
                    
                    # Code block is more than 1000 chunks
                    mini_content = content[start:end]
                    accumulated_mini = ""
                    captures_mini = return_chunks(mini_content, node.type)

                    for nodes in captures_mini.values():
                        for node in nodes:
                            start, end = node.start_byte, node.end_byte
                            code_block = mini_content[start:end].decode("utf-8", errors="ignore")

                            if token_count(code_block) + token_count(accumulated_mini) > 1000:
                                create_chunk(accumulated_mini, path, chunk_count, priority)
                                chunk_count += 1
                                accumulated_mini = ""

                            accumulated_mini += code_block + "\n"
                            
                    if accumulated_mini.strip():
                        create_chunk(accumulated_mini, path, chunk_count, priority)
                        chunk_count += 1

            if accumulated.strip():
                create_chunk(accumulated, path, chunk_count, priority)


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
