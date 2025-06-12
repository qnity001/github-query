import json
from pathlib import Path

def get_repo_path():
    with open(Path(__file__).parent.parent / "data/outputs/meta.json", "r") as file:
        meta = json.load(file)
    return Path(meta["folder_path"])