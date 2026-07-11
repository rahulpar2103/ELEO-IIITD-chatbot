# ECE Labs Chatbot (ELEO) - IIIT Delhi

A RAG-based chatbot for the ECE Labs website at IIIT Delhi. Uses FAISS for retrieval and Gemini as the LLM, orchestrated via LangGraph.

## Project structure

```
ingestion/       parse JSON and PDF sources into chunks
embeddings/      embed chunks using Gemini embedding model
index/           build the FAISS index
data/            stores the built FAISS index and processed data
retrieval/       load the vector store, expand lab abbreviations, fetch announcements
tools/           LangChain tools that the agent can call
generation/      LangGraph agent graph with memory and LLM fallback chain
api/             FastAPI layer (schemas, rate limiter, service, router, app)
```

## Setup

Copy `.env.example` to `.env` and fill in your keys:

```
GEMINI_API_KEY=your_key_here
EMBEDDING_MODEL=models/gemini-embedding-2
LLM_MODEL=gemini-flash-lite-latest
```

*Note: The chatbot utilizes a native LangChain fallback chain. If the primary model `LLM_MODEL` (e.g., `gemini-flash-lite-latest`) fails due to rate limits or transient errors, it will automatically fallback to `gemini-2.5-flash` followed by `gemini-3.5-flash` using the same `GEMINI_API_KEY` without any extra charges.*

The FAISS index needs to be built once before running the API. Run the ingestion and indexing scripts in order if starting fresh.

## Running with Docker (recommended)

Make sure Docker Desktop is open and running, then:

```bash
docker-compose up --build
```

API will be at `http://localhost:8000`. On subsequent runs, `docker-compose up` is enough.

To stop: `docker-compose down`

## Running locally without Docker

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

## API

`POST /chat`

Request:
```json
{
  "message": "What is the BE lab about?",
  "session_id": "some-unique-id"
}
```

Response:
```json
{
  "response": "The Basic Electronics lab ..."
}
```

Rate limit is 10 messages per session per hour. Exceeding it returns a 429.

Memory is in-process only and resets on server restart.
