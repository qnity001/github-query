import json
from pathlib import Path

def create_json(tree: dict):
    #output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "outputs"
   # output_dir.mkdir(parents=True, exist_ok=True)

  #  output = output_dir / "repo_tree.json"
    json_tree = json.dumps(tree, indent=4)

    with open("json_tree.json", "w") as file:
        file.write(json_tree)