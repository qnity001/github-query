from tree_sitter_language_pack import get_parser
from tree_sitter import Query
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")

language_extensions = {
    ".py" : "python", 
    ".php" : "php",
    ".js" : "javascript",
    ".html" : "html",
    ".css" : "css"
}

php_query_top_level = """
(
  (comment)* @comment
  (class_declaration) @class
) @class_chunk

(
  (comment)* @comment
  (trait_declaration) @trait
) @trait_chunk

(
  (comment)* @comment
  (interface_declaration) @interface
) @interface_chunk

(
  (comment)* @comment
  (function_definition) @global_function
  (#not-inside? class_declaration)
  (#not-inside? trait_declaration)
  (#not-inside? interface_declaration)
) @global_function_chunk
"""

php_query_function = '''
(
  (comment)* @comment
  (expression_statement) @expression
) @expression_chunk

(
  (comment)* @comment
  (return_statement) @return
) @return_chunk

(
  (comment)* @comment
  (if_statement) @if
) @if_chunk

(
  (comment)* @comment
  (switch_statement) @switch
) @switch_chunk

(
  (comment)* @comment
  (while_statement) @while
) @while_chunk

(
  (comment)* @comment
  (for_statement) @for
) @for_chunk

(
  (comment)* @comment
  (foreach_statement) @foreach
) @foreach_chunk

(
  (comment)* @comment
  (function_definition) @nested_function
) @nested_function_chunk
'''

php_query_not_function = '''
(
  (comment)* @comment
  (method_declaration) @method
) @method_chunk

(
  (comment)* @comment
  (property_declaration) @property
) @property_chunk

(
  (comment)* @comment
  (const_declaration) @constant
) @constant_chunk
'''

def find_parser(extension):
    language = language_extensions[extension]
    if language:
        return get_parser(language)
    return None

def return_chunks(content, node):
    parser = find_parser(".php")
    tree = parser.parse(content)
    root = tree.root_node
    if node == None:
        query = Query(parser.language, php_query_top_level)
    elif node == "function":
        query = Query(parser.language, php_query_function)
    else:
        query = Query(parser.language, php_query_not_function)
    captures = query.captures(root)
    return captures