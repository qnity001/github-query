import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"
chunks_path = data_dir / "outputs" / "chunk_output.json"

def get_repo_path():
    with open(data_dir / "outputs/meta.json", "r") as file:
        meta = json.load(file)
    return Path(meta["folder_path"])