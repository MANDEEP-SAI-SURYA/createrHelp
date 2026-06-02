import os
import requests
from dotenv import load_dotenv

load_dotenv()

CREATORCRAWL_API_KEY = os.getenv("CREATORCRAWL_API_KEY")

BASE_URL = "https://creatorcrawl.com/api"

HEADERS = {
    "x-api-key": CREATORCRAWL_API_KEY
}


def get_post_info(url):

    response = requests.get(
        f"{BASE_URL}/instagram/post",
        params={"url": url},
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()


def get_transcript(url):

    response = requests.get(
        f"{BASE_URL}/instagram/media/transcript",
        params={"url": url},
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()


def get_comments(url):

    response = requests.get(
        f"{BASE_URL}/instagram/post/comments",
        params={"url": url},
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()


def get_basic_profile(user_id):

    response = requests.get(
        f"{BASE_URL}/instagram/basic-profile",
        params={"user_id": user_id},
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()


def extract_instagram_data(url):

    # Post Metadata
    post_response = get_post_info(url)
    post_data = post_response.get("data", {})

    creator = post_data.get(
        "author",
        {}
    )

    # Transcript
    transcript = post_data.get(
        "text",
        ""
    )

    try:

        transcript_response = get_transcript(url)

        transcript_data = (
            transcript_response.get(
                "data",
                {}
            )
        )

        transcript = transcript_data.get(
            "transcript",
            transcript
        )

    except Exception as e:

        print(
            "Transcript fetch failed:",
            e
        )

    # Comments
    comments = []
    try:
        comments_response = get_comments(url)
        comments = [
            comment.get(
                "text",
                ""
            )
            for comment in comments_response.get(
                "data",
                []
            )

        ]

    except Exception as e:
        print("Comments fetch failed:",e)

    # Creator Profile
    profile_data = {}
    try:
        creator_id = creator.get("id")
        if creator_id:
            profile_response = (
                get_basic_profile(
                    creator_id
                )
            )
            profile_data = (
                profile_response.get(
                    "data",
                    {}
                )
            )

    except Exception as e:

        print("Profile fetch failed:",e)

    # Build Metadata
    video_metadata = {

        "video_id":
            post_data.get("id",""),

        "title":
            post_data.get("text","")[:100],

        "description":
            post_data.get("text",""),

        "views":
            post_data.get("view_count",0),

        "likes":
            post_data.get("like_count",0),

        "comments":
            post_data.get("comment_count",0),

        "duration":
            post_data.get("duration_seconds",0),

        "platform":
            "instagram"
    }

    channel_metadata = {

        "channel_name":

            profile_data.get("handle")

            or creator.get("handle")

            or creator.get("name",""),

        "subscriber_count":

            profile_data.get("followers_count",0)
    }

    # Debug Logs
    print("Instagram Video:",video_metadata)

    print("Instagram Creator:",channel_metadata)

    print("Transcript Length:",len(transcript))

    print("Comments Count:",len(comments))

    return (
        video_metadata,
        channel_metadata,
        transcript,
        comments
    )