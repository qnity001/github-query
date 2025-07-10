import json

counter = 1
id_map = {}
labels = {}
subgraph_declarations = []
edge_declarations = []

def get_tree():
    with open("../../data/outputs/repo_tree.json", "r") as file:
        return json.load(file)

def walk_tree(name, node, parent_id = None):
    global counter
    global id_map

    current_id = f"A{counter}"
    counter += 1
    id_map[node["path"]] = current_id
    labels[current_id] = name

    #if node["type"] == "file":
    subgraph_declarations.append(f'\t{current_id}["{name}"]')

    if parent_id:
        edge_declarations.append(f"\t{parent_id} --> {current_id}")

    if node["type"] == "folder":
        #subgraph_declarations.append(f'\tsubgraph "{name}"\n\tdirection TB')
    
        for child_name, child_node in node["children"].items():
            walk_tree(child_name, child_node, current_id)
        
        #subgraph_declarations.append("\tend")

def run():
    tree = get_tree()
    for name, node in tree.items():
        walk_tree(name, node)

    mermaid_lines = ["flowchart TD"]
    mermaid_lines += subgraph_declarations
    mermaid_lines += edge_declarations
    mermaid_code = "\n".join(mermaid_lines)
    with open("../../data/outputs/graph.mmd", "w") as file:
        file.write(mermaid_code)

run()