import json

counter = 1
id_map = {}
labels = {}
node_declarations = []
edge_declarations = []

def get_tree():
    with open("../../data/outputs/repo_tree.json", "r") as fileread:
        return json.load(fileread)
    
def walk_tree(name, node, parent_id = None):
    global counter
    global id_map

    current_id = f"A{counter}"
    counter += 1
    id_map[node["path"]] = current_id # This path node has this ID basically
    labels[current_id] = name # This ID has this name basically
    
    line = f'{current_id}["{name}"]' # Create node declaration
    node_declarations.append(line) # Add node to list of nodes

    if parent_id:
        edge_declarations.append(f"{parent_id} --> {current_id}")

    if node["type"] == "folder":
        for child_name, child_node in node["children"].items():
            walk_tree(child_name, child_node, current_id)

def run():
    tree = get_tree()
    for name, node in tree.items():
        walk_tree(name, node)
    mermaid_lines = ["flowchart TD"]
    mermaid_lines += node_declarations
    mermaid_lines += edge_declarations
    mermaid_code = "\n".join(mermaid_lines)
    with open("../../data/outputs/graph.mmd", "w") as file:
        file.write(mermaid_code)
run()

