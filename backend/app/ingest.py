from app.chunk import chunk_text
from app.embedding import generate_embedding
from app.qdrant_vectordb import create_collection, store_documents


def ingest_video_data(video_metadata, channel_metadata, transcript):

    views = int(video_metadata.get("views", 0))
    likes = int(video_metadata.get("likes", 0))
    comments = int(video_metadata.get("comments", 0))

    engagement = 0

    if views > 0:
        engagement = ((likes + comments) / views) * 100

    create_collection()

    metadata_text = f"""
Title: {video_metadata['title']}
Description: {video_metadata['description']}
Creator: {channel_metadata['channel_name']}
Subscribers: {channel_metadata['subscriber_count']}
Views: {views}
Likes: {likes}
Comments: {comments}
Engagement Rate: {engagement:.2f}
Duration: {video_metadata['duration']}
"""

    metadata_payload = {
        "text": metadata_text,
        "video_id": video_metadata["video_id"],
        "chunk_type": "metadata",
        "title": video_metadata["title"],
        "creator": channel_metadata["channel_name"],
        "subscribers": channel_metadata["subscriber_count"],
        "views": views,
        "likes": likes,
        "comments": comments,
        "engagement_rate": engagement
    }

    metadata_embedding = [
        generate_embedding(metadata_text)
    ]

    store_documents(
    [metadata_payload],
    metadata_embedding
)


    hook_text = transcript[:1000]

    hook_payload = {
        "text": hook_text,
        "video_id": video_metadata["video_id"],
        "chunk_type": "hook",
        "title": video_metadata["title"],
        "creator": channel_metadata["channel_name"]
    }

    hook_embedding = [
        generate_embedding(hook_text)
    ]

    store_documents(
        [hook_payload],
        hook_embedding
    )

    chunks = chunk_text(transcript)

    transcript_payloads = []

    for chunk in chunks:

        transcript_payloads.append(
            {
                "text": chunk,
                "video_id": video_metadata["video_id"],
                "chunk_type": "transcript",
                "title": video_metadata["title"],
                "creator": channel_metadata["channel_name"]
            }
        )

    embeddings = [
        generate_embedding(chunk)
        for chunk in chunks
    ]

    store_documents(
        transcript_payloads,
        embeddings
    )
    print("Metadata stored")
    print("Transcript chunks:", len(chunks))