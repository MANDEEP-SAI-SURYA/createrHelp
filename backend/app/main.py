from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.youtube_service import process_youtube_url

app = FastAPI()


class YoutubeRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "message": "YouTube Extraction API Running"
    }


@app.post("/youtube")
def extract_youtube(data: YoutubeRequest):

    try:

        result = process_youtube_url(data.url)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        print("ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
    )