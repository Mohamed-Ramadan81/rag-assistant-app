import ollama
from app.services.retrieval import retrieve


def prompt_template(query, context):
    system_prompt = """
    you are an helpful assistant for Harry Potter RAG system.
    your task is answering the user's questions using only the information contained in retrieved context.
    If the answer is not there, say you do not know.

    rules:
        Do not use outside knowledge.
        If the answer is not there, say you do not know.
        Be concise and answer directly.
    """

    user_prompt = f"Context: {context}\nQuestion: {query}"

    return system_prompt, user_prompt


def get_answer(query, model_transformer, collection, ollama_client, ollama_model, top_k=3):

    context,sources = retrieve(query, model_transformer, collection, top_k)

    system_prompt, user_prompt = prompt_template(query, context)

    answer = ollama_client.chat(
        model=ollama_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return answer["message"]["content"], sources