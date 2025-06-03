import json

def load(filters):
    try:
        with open(filters, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The filter.json file is not present")
        return {
            "extensions" : [],
            "files" : []
        }
