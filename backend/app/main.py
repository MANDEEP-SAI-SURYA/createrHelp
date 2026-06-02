from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.youtube_service import process_youtube_url
from app.retrieval import retrieve_context
from app.groq_llm import ask_groq
from fastapi.responses import StreamingResponse
from app.groq_llm import stream_groq
from app.instagram import extract_instagram_data
from app.ingest import ingest_video_data, ingest_instagram_data


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YoutubeRequest(BaseModel):
    url: str


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Social Media RAG API Running"
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

@app.post("/chat")
def chat(data: ChatRequest):

    try:

        docs = retrieve_context(
            data.question
        )

        answer = ask_groq(
            data.question,
            docs
        )

        return {
            "success": True,
            "answer": answer,
            "sources": docs
        }

    except Exception as e:

        print("CHAT ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/chat-stream")
def chat_stream(data: ChatRequest):

    docs = retrieve_context(data.question)

    return StreamingResponse(
        stream_groq(data.question, docs),
        media_type="text/plain"
    )
    
    
class InstagramRequest(BaseModel):
    url: str


@app.post("/instagram")
def process_instagram(data: InstagramRequest):

    (
        video_metadata,
        channel_metadata,
        transcript,
        comments
    ) = extract_instagram_data(data.url)

    ingest_instagram_data(
        video_metadata,
        channel_metadata,
        transcript,
        comments
    )

    return {
        "message": "Instagram processed"
    }