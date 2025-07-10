import_statement = '''
(import_statement) @imported
'''

import_from_statement = '''
(import_from_statement) @import.from_stmt
'''

import_words = '''
(import_from_statement
    module_name: (dotted_name) @from_module
    (dotted_name) @imported_item
)
'''