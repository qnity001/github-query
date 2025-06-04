import json

def filter(path):
    with open(path) as file:
        data = file.read()
    filters = json.loads(data)
    return filters["extensions"], filters["files"]
