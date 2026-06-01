import os
import uuid

from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "youtube_rag"


def create_collection():

    collections = [
        c.name
        for c in client.get_collections().collections
    ]

    print("Existing collections:", collections)

    if COLLECTION_NAME not in collections:

        print("Creating collection...")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Collection created!")


def store_documents(chunks, embeddings):

    points = []

    for chunk, vector in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )