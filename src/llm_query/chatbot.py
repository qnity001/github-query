import ollama
from src.retrieving import retriever

model_name = "deepseek-coder:6.7b-instruct"

def make_query(user_query, chunks):
    prompt = "You are an expert codebase assistant. Using the following code snippets: answer the user's question. The code might be entire file or a part of the file"
    prompt += f"User's question: {user_query} \n\n"
    prompt += "Code snippets: \n\n"

    for chunk in chunks:
        prompt += f"{chunk}\n\n-------\n\n"

    prompt += "Answer: \n"
    
    response = ollama.chat(
        model = model_name,
        messages=[
            {"role" : "user", "content" : prompt}
        ]
    )

    print(response["message"]["content"])

def run():
    user_query = input("Ask question from the codebase:")
    if not user_query.split():
        exit()
    input_chunks = retriever.run(user_query)
    make_query(user_query, input_chunks)
