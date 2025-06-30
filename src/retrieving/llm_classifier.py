import ollama

PROMPT_TEMPLATE = """
You are an intelligent assistant designed to categorize user queries for code retrieval. Your task is to determine the user's primary intent based on their query.

Intent categories:
- file_search: The user mentions or refers to a specific filename or file path or folder.
- semantic_search: The user is looking for code based on functionality, content or a description, without specifying a particular file.

Instructions:
- Read the user's query carefully.
- If the query contains a mention of a filename (e.g., "my_script.py", "src/utils.js", "README.md", "config.xml", "main.cpp", "filter.php"), identify the intent as "file_search".
- For all other queries that do not specify a filename, identify the intent as "semantic_search".
- Respond with only the intent category name (either "file_search" or "semantic_search"). Do not include any other text or explanation.

Examples:
- Query: "Find the function calculate_total in orders.py"
Response: file_search
- Query: "Show me how to connect to a database in Python"
Response: semantic_search
- Query: "What are the common utility functions in helper_module.js?"
Response: file_search
- Query: "How do I implement a breadth-first search algorithm?"
Response: semantic_search
- Query: "Look for user_authentication.go"
Response: file_search
- Query: "Find code for user authentication"
Response: semantic_search

User Query: "{query}"
Intent:
"""

def predict_intent_llm(user_query):
    prompt = PROMPT_TEMPLATE.format(query = user_query)

    response = ollama.chat(
        model = "deepseek-coder:6.7b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    intent = response["message"]["content"].strip().lower()

    if intent not in ["file_search", "semantic_search"]:
        intent = "semantic_search"
    
    return intent