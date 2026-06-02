import os
import re

from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from app.audio_service import download_audio
from app.assembly_service import transcribe_audio

from app.ingest import ingest_video_data

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


def extract_video_id(url: str):
    """
    Supports:
    https://www.youtube.com/watch?v=xxxx
    https://youtube.com/shorts/xxxx
    https://youtu.be/xxxx
    """

    patterns = [
        r"v=([^&]+)",
        r"shorts/([^/?]+)",
        r"youtu\.be/([^/?]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


def get_video_metadata(video_id: str):

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )

    response = request.execute()

    if not response.get("items"):
        return None

    item = response["items"][0]

    snippet = item["snippet"]
    statistics = item.get("statistics", {})
    content_details = item.get("contentDetails", {})

    return {
        "video_id": video_id,
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channel_title": snippet.get("channelTitle"),
        "channel_id": snippet.get("channelId"),
        "published_at": snippet.get("publishedAt"),
        "tags": snippet.get("tags", []),
        "category_id": snippet.get("categoryId"),
        "views": statistics.get("viewCount"),
        "likes": statistics.get("likeCount"),
        "comments": statistics.get("commentCount"),
        "duration": content_details.get("duration")
    }


def get_channel_metadata(channel_id: str):

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )

    response = request.execute()

    if not response.get("items"):
        return None

    item = response["items"][0]

    return {
        "channel_name": item["snippet"].get("title"),
        "subscriber_count": item["statistics"].get("subscriberCount"),
        "total_views": item["statistics"].get("viewCount"),
        "total_videos": item["statistics"].get("videoCount")
    }


def get_transcript(video_id: str):

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        full_text = " ".join(
            chunk["text"]
            for chunk in transcript
        )

        return {
            "transcript": full_text,
            "segments": transcript
        }

    except Exception as e:
        return {
            "transcript": "",
            "segments": [],
            "error": str(e)
        }


def process_youtube_url(url: str):

    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    video_metadata = get_video_metadata(video_id)

    if not video_metadata:
        raise ValueError("Video not found")

    channel_metadata = get_channel_metadata(
        video_metadata["channel_id"]
    )

    transcript = get_transcript_with_fallback(
            video_id,
            url
        )
    
    ingest_video_data(video_metadata,channel_metadata,transcript, platform="youtube")

    return {
    "video_metadata": video_metadata,
    "channel_metadata": channel_metadata,
    "transcript": transcript,
    "segments": []
}
    

def get_transcript_with_fallback(video_id, youtube_url):

    try:

        print("Trying YouTube Transcript API...")

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join(
            snippet.text
            for snippet in transcript
        )

        print("YouTube transcript found!")

        return text

    except Exception as e:

        print(f"Transcript unavailable: {e}")

        print("Using AssemblyAI fallback...")

        audio_file = download_audio(youtube_url)

        transcript = transcribe_audio(audio_file)

        return transcript