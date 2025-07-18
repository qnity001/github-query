import os
import json
from tree_sitter_language_pack import get_parser
from tree_sitter import Query
from src.config import get_repo_path
from src.chunking.queries import python_queries as queries

############################### GLOBAL DECLARATIONS ##########################################################################

counter = 1
file_id_map = {}
file_labels = {}
folder_id_map = {}
folder_labels = {}
dependencies = {}
boilerplate = ["flowchart TD"]
subgraph_declarations = []
edge_declarations = []
class_declarations = ["\tclassDef file fill:#e0f7fa, stroke:#00796b, stroke-width:2px", 
                      "\tclassDef folder fill:#eeeeee, stroke:#424242, stroke-width:1px"]

####################################### HELPER FUNCTIONS ##########################################################################

# Get the tree json
def get_tree():
    with open("data/outputs/repo_tree.json", "r") as file:
        return json.load(file)
    
# Get dependencies from "import from"
def extract_from_import(line):
    if line.startswith("from ") and " import " in line:
        parts = line.strip().split()
        if len(parts) >= 4:
            from_module = parts[1]
            imported = parts[3]
            return [f"{from_module}", f"{from_module}.{imported}"]
    return None
    
# Get file to file dependencies
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
def verify_import(path):
    # Create a path out of the imports and add .py to end because we are doing it for just python
    candidate = path.replace(".", "/") + ".py"
    if candidate in file_id_map:
        return candidate
    else:
        return None
    
# Return parent dir of the input files
def declare_edge(path1, path2):
    dir1 = os.path.dirname(path1)
    dir2 = os.path.dirname(path2)

    # If parent folders are same, then current ids will be for the files
    if dir1 == dir2:
        res1 = file_id_map[path1]
        res2 = file_id_map[path2]

    else:
        res1 = folder_id_map[dir1] if dir1 in folder_id_map else "A1"
        res2 = folder_id_map[dir2] if dir2 in folder_id_map else "A1"
    
    if not res1 == res2:
        declaration = f"\t{res1} --> |imports|{res2}"
        if declaration not in edge_declarations:
            edge_declarations.append(declaration)
    
####################################### MAIN FUNCTIONS #####################################################################

def walk_tree(name, node):
    global counter
    global id_map
    global dependencies

    current_id = f"A{counter}"
    counter += 1

    # Add node to id_map if its file, folders have their own subgraphs
    if node["type"] == "file":

        # Add file to node id map
        file_id_map[node["path"]] = current_id 
        file_labels[current_id] = name

        class_declarations.append(f"\tclass {current_id} file")
        subgraph_declarations.append(f'\t{current_id}["{name}"]')
        dependencies[node["path"]] = extract_imports(node["path"])

    if node["type"] == "folder":

        # Add folder to folder id map
        folder_id_map[node["path"]] = current_id
        folder_labels[current_id] = name

        class_declarations.append(f"\tclass {current_id} folder")
        subgraph_declarations.append(f'\tsubgraph {current_id} ["{name}"]\n\tdirection TB')
    
        for child_name, child_node in node["children"].items():
            walk_tree(child_name, child_node)
        
        subgraph_declarations.append("\tend")

# Create edge declarations from intra file dependencies
def verify_dependencies():
    for path, imports in dependencies.items():
        if imports:
            for value in imports:
                imported_path = verify_import(value)
                if imported_path:
                    declare_edge(path, imported_path)

def run():
    tree = get_tree()
    for name, node in tree.items():
        walk_tree(name, node)
    verify_dependencies()

    mermaid_lines = boilerplate
    mermaid_lines += subgraph_declarations
    mermaid_lines += edge_declarations
    mermaid_lines += class_declarations
    mermaid_code = "\n".join(mermaid_lines)

    with open("data/outputs/graph.mmd", "w") as file:
        file.write(mermaid_code)

    with open("data/outputs/graph.mmd", "r") as file:
        content = file.read()

    with open("data/outputs/graph.html", "w") as file:
        file.write("<html><body>\n")
        file.write("<h3>Dummy Mermaid Diagram</h3>\n")
        file.write('<div class="mermaid">\n')
        file.write(content+"\n")
        file.write('</div>\n<script type="module">\n')
        file.write("import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';\n")
        file.write("mermaid.initialize({startOnLoad:true});\n")
        file.write("</script>\n</body></html>\n")
