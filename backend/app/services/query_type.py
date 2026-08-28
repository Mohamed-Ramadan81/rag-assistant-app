def query_router(query, ollama_client, ollama_model):

    system_prompt = """
you are a query router for a Harry Potter RAG system.
you should understand the knowledge base well and then classify it.

Classify the user's query into exactly one label:

retrieve: any question related to the Harry Potter books, including characters, events, places, objects, or story details.

chat: casual conversation, greetings, thanks, or general conversation that does not require the Harry Potter knowledge base.

off_topic: The question is unrelated to Harry Potter and is not casual conversation.

Return exactly one label:
retrieve
chat
off_topic
"""

    response = ollama_client.chat(
        model=ollama_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ],
        options={
            "temperature": 0
        }
    )

    route = response["message"]["content"].strip().lower()

    if route not in ["retrieve", "chat", "off_topic"]:
        route = "off_topic"

    return route