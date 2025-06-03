import json

with open("filters.json") as file:
    data = file.read()

filters = json.loads(data)
print(filters)
