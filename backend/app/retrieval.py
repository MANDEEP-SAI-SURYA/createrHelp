from app.embedding import generate_embedding
from app.qdrant_vectordb import client, COLLECTION_NAME


def retrieve_context(query):

    query_vector = generate_embedding(query)

    results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=5
    ).points
    print("Retrieved docs:", len(results))

    docs = []

    for hit in results:

        docs.append({
            "score": hit.score,
            **hit.payload
        })

    return docs