def retrieve(query, model_transformer, collection, top_k=3):

    embedding = model_transformer.encode(
        [f"query: {query}"],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=embedding,
        n_results=top_k
    )

    sources=[]
    context = ""
    for i in range(top_k):
        context += (
            f'id: {results["ids"][0][i]}\n'
            f'book_name: {results["metadatas"][0][i]["book_name"]}\n'
            f'pages: {results["metadatas"][0][i]["pages_number"]}\n'
            f'text: {results["documents"][0][i]}\n'
            '=========================================================\n'
        )

        sources.append(
            f'[{results["ids"][0][i]}, '
            f'{results["metadatas"][0][i]["book_name"]}, '
            f'{results["metadatas"][0][i]["pages_number"]}]'
        )

    return context,sources