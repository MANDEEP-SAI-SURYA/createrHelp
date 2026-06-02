# CreaterHelp

An AI powered Retrieval Augmented Generation (RAG) platform that helps YouTube and Instagram creators analyze their content, understand audience engagement and discover actionable growth opportunities.

The system automatically extracts video and post metadata, creator information, transcripts and audience comments from social media content.This information is transformed into vector embeddings and stored in Qdrant, enabling creators to interact with their content through natural language conversations.

Using semantic retrieval and Large Language Models, the platform provides creator focused insights such as:

* Performance analysis
* Content comparison
* Engagement improvement suggestions
* Growth recommendations

---

## Key Features

### YouTube Intelligence

* Video metadata extraction
* Channel information extraction
* Transcript generation
* Comment ingestion
* Content summarization
* Engagement analysis
* Semantic search across videos

### Instagram Intelligence

* Reel/Post metadata extraction
* Creator profile extraction
* transcript extraction
* Comment analysis
* Content understanding

### AI Powered Creator Assistant

* Retrieval Augmented Generation (RAG)
* Context aware conversations
* Semantic search
* Creator focused recommendations
* Growth opportunity identification

---

## Tech Stack

### Frontend

* React
* Vite

### Backend

* FastAPI
* Python

### Vector Database

* Qdrant Cloud

### Embedding Model

BAAI/bge-small-en-v1.5

### Large Language Model

* Groq
* Llama 3.3 70B Versatile

### Data Sources

#### YouTube

* YouTube Data API
* AssemblyAI (Transcription)

#### Instagram

* CreatorCrawl API

---

## Required APIs
* YOUTUBE_API_KEY=your_youtube_api_key_here
* ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
* GROQ_API_KEY=your_groq_api_key_here
* QDRANT_URL=your_qdrant_url
* QDRANT_API_KEY=your_qdrant_api_key
* CREATORCRAWL_API_KEY=your_creatorcrawl_api_key_here

## Core AI Pipeline

1. User submits a YouTube or Instagram URL
2. Metadata, transcripts and comments are extracted
3. Content is chunked and embedded
4. Embeddings are stored in Qdrant Cloud
5. User asks a question
6. Relevant context is retrieved using semantic search
7. Groq hosted Llama generates grounded responses
8. Creator receives actionable insights

## Environment Setup

* Create a .env file inside backend.

## Installation
# Backend

* Create virtual environment: python -m venv venv

* Activate

* Windows: venv\Scripts\activate

* Install dependencies: pip install -r requirements.txt

* Run backend: uvicorn app.main:app --reload

# Frontend

* Install dependencies: npm install

* Run frontend: npm run dev