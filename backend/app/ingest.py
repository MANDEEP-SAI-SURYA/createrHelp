from app.chunk import chunk_text
from app.embedding import generate_embedding
from app.qdrant_vectordb import create_collection, store_documents


def ingest_video_data(video_metadata,channel_metadata,transcript,platform,comments=None):

    print("Platform:", platform)
    print("Comments type:", type(comments))
    print("Comments:", comments)
    
    
    views = int(video_metadata.get("views", 0))
    likes = int(video_metadata.get("likes", 0))
    comments = int(video_metadata.get("comments", 0))

    engagement = 0

    if views > 0:
        engagement = ((likes + comments) / views) * 100

    create_collection()

    metadata_text = f"""
Platform: {platform}
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
        "platform": platform,
        "video_id": video_metadata["video_id"],
        "video_ref": f"{channel_metadata['channel_name']} - {video_metadata['title'][:60]}",
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

    # Hook chunk
    hook_text = transcript[:1000]

    hook_payload = {
        "text": hook_text,
        "platform": platform,
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

    # Transcript chunks
    chunks = chunk_text(transcript)

    transcript_payloads = []

    for chunk in chunks:

        transcript_payloads.append(
            {
                "text": chunk,
                "platform": platform,
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
    
    if comments:

        comment_payloads = []

        for comment in comments:

            comment_payloads.append(
                {
                    "text": comment,
                    "video_id": video_metadata["video_id"],
                    "chunk_type": "comment",
                    "title": video_metadata["title"],
                    "creator": channel_metadata["channel_name"],
                    "platform": platform
                }
            )

        comment_embeddings = [
            generate_embedding(comment)
            for comment in comments
        ]

        store_documents(
            comment_payloads,
            comment_embeddings
        )

        print("Comments stored:", len(comments))

    print("Platform:", platform)
    print("Metadata stored")
    print("Transcript chunks:", len(chunks))
    
    




def ingest_instagram_data(video_metadata,channel_metadata,transcript,comments=None):

    create_collection()

    views = int(
        video_metadata.get("views", 0)
    )

    likes = int(
        video_metadata.get("likes", 0)
    )

    comment_count = int(
        video_metadata.get("comments", 0)
    )

    engagement = 0

    if views > 0:
        engagement = ((likes + comment_count)/ views) * 100

    metadata_text = f"""
    Platform: Instagram
    Title: {video_metadata['title']}
    Description: {video_metadata['description']}
    Creator: {channel_metadata['channel_name']}
    Followers: {channel_metadata['subscriber_count']}
    Views: {views}
    Likes: {likes}
    Comments: {comment_count}
    Engagement Rate: {engagement:.2f}
    Duration: {video_metadata['duration']}
    """

    metadata_payload = {
        "text": metadata_text,
        "platform": "instagram",
        "video_id": video_metadata["video_id"],
        "video_ref": f"{channel_metadata['channel_name']} - {video_metadata['title'][:60]}",
        "chunk_type": "metadata",
        "title": video_metadata["title"],
        "creator": channel_metadata["channel_name"],
        "followers": channel_metadata[
            "subscriber_count"
        ],
        "views": views,
        "likes": likes,
        "comments": comment_count,
        "engagement_rate": engagement
    }

    store_documents(
        [metadata_payload],
        [generate_embedding(metadata_text)]
    )

    # Transcript Hook
    hook_text = transcript[:1000]

    hook_payload = {
        "text": hook_text,
        "platform": "instagram",
        "video_id": video_metadata["video_id"],
        "chunk_type": "hook",
        "title": video_metadata["title"],
        "creator": channel_metadata["channel_name"]
    }

    store_documents(
        [hook_payload],
        [generate_embedding(hook_text)]
    )

    # Transcript Chunks
    chunks = chunk_text(transcript)

    transcript_payloads = []

    for chunk in chunks:

        transcript_payloads.append(
            {
                "text": chunk,
                "platform": "instagram",
                "video_id": video_metadata["video_id"],
                "chunk_type": "transcript",
                "title": video_metadata["title"],
                "creator": channel_metadata[
                    "channel_name"
                ]
            }
        )

    transcript_embeddings = [
        generate_embedding(chunk)
        for chunk in chunks
    ]

    store_documents(
        transcript_payloads,
        transcript_embeddings
    )

    # Comments
    if comments and len(comments) > 0:

        comment_payloads = []

        for comment in comments:

            if not comment.strip():
                continue

            if "instagram.com" in comment.lower():
                continue

            if "http" in comment.lower():
                continue

            if len(comment.strip()) < 5:
                continue

            comment_payloads.append(
                {
                    "text": comment,
                    "platform": "instagram",
                    "video_id": video_metadata[
                        "video_id"
                    ],
                    "chunk_type": "comment",
                    "title": video_metadata[
                        "title"
                    ],
                    "creator": channel_metadata[
                        "channel_name"
                    ]
                }
            )

        if comment_payloads:

            comment_embeddings = [
                generate_embedding(
                    payload["text"]
                )
                for payload in comment_payloads
            ]

            store_documents(
                comment_payloads,
                comment_embeddings
            )

            print(
                "Instagram comments stored:",
                len(comment_payloads)
            )

    print("Instagram metadata stored")
    print(
        "Instagram transcript chunks:",
        len(chunks)
    )