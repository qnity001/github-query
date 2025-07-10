import json
from tree_sitter_language_pack import get_parser
from tree_sitter import Query
from src.config import get_repo_path
from src.chunking.queries import python_queries as queries

############################### GLOBAL DECLARATIONS ##########################################################################

counter = 1
id_map = {}
labels = {}
dependencies = {}
subgraph_declarations = []
edge_declarations = []
class_declarations = ["\tclassDef file fill:#e0f7fa, stroke:#00796b, stroke-width:2px", 
                      "\tclassDef folder fill:#eeeeee, stroke:#424242, stroke-width:1px"]

####################################### HELPER FUNCTIONS ##########################################################################

def get_tree():
    with open("data/outputs/repo_tree.json", "r") as file:
        return json.load(file)
    
def extract_from_import(line):
    if line.startswith("from ") and " import " in line:
        parts = line.strip().split()
        if len(parts) >= 4:
            from_module = parts[1]
            imported = parts[3]
            return [f"{from_module}", f"{from_module}.{imported}"]
    return None
    
def extract_imports(path):
    if not path.endswith(".py"):
        return None
    
    repo_root = get_repo_path()
    with open(f"{repo_root}/{path}", "rb") as file:
        content = b"".join([file.readline() for line in range(10)])
    parser = get_parser("python")
    tree = parser.parse(content)
    root = tree.root_node

    imports = []

    # For normal
    query = Query(parser.language, queries.import_statement)
    captures = query.captures(root)
    for nodes in captures.values():
        for node in nodes:
            start, end = node.start_byte, node.end_byte
            imports.append(content[start:end].decode("utf-8", errors="ignore"))
    
    
    # For from import 
    query = Query(parser.language, queries.import_from_statement)
    captures = query.captures(root)
    for nodes in captures.values():
        for node in nodes:
            start, end = node.start_byte, node.end_byte
            statement = content[start:end].decode("utf-8", errors="ignore")
            imports += extract_from_import(statement)
    
    return imports

# Receive path and check if it exists in the map
def convert_to_path(path):
    candidate = path.replace(".", "\\") + ".py"
    if candidate in id_map:
        return id_map[candidate]
    else:
        return None

####################################### MAIN FUNCTIONS #####################################################################

def walk_tree(name, node, parent_id = None):
    global counter
    global id_map
    global dependencies

    current_id = f"A{counter}"
    counter += 1

    # Add node to id_map if its file, folders have their own subgraphs
    if node["type"] == "file":
        id_map[node["path"]] = current_id 
        labels[current_id] = name
        class_declarations.append(f"\tclass {current_id} file")
        subgraph_declarations.append(f'\t{current_id}["{name}"]')
        dependencies[node["path"]] = extract_imports(node["path"])

    if node["type"] == "folder":
        class_declarations.append(f"\tclass {current_id} folder")
        subgraph_declarations.append(f'\tsubgraph "{name}"\n\tdirection TB')
    
        for child_name, child_node in node["children"].items():
            walk_tree(child_name, child_node, current_id)
        
        subgraph_declarations.append("\tend")

def create_edges():
    for path, imports in dependencies.items():
        if imports:
            for value in imports:
                # Create a path out of the imports and add .py to end because we are doing it for just python
                current_id_for_import = convert_to_path(value)
                if current_id_for_import:
                    edge_declarations.append(f"\t{id_map[path]} -->|imports| {current_id_for_import}")

def run():
    tree = get_tree()
    for name, node in tree.items():
        walk_tree(name, node)
    create_edges()

    mermaid_lines = ["flowchart TD"]
    mermaid_lines += subgraph_declarations
    mermaid_lines += edge_declarations
    mermaid_lines += class_declarations
    mermaid_code = "\n".join(mermaid_lines)

    with open("data/outputs/graph.mmd", "w") as file:
        file.write(mermaid_code)
