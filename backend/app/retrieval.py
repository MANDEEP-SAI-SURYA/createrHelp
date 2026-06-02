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
        
    
    for hit in results:
        print(
            "\nScore:", hit.score,
            "\nCreator:", hit.payload.get("creator"),
            "\nTitle:", hit.payload.get("title"),
            "\nChunk Type:", hit.payload.get("chunk_type"),
            "\nText:", hit.payload.get("text", "")[:150]
        )
    

    return docs