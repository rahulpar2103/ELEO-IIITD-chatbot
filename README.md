# ECE Labs Chatbot (ELEO) - IIIT Delhi

A RAG-based chatbot and content management system for the ECE Labs website at IIIT Delhi. Uses FAISS for retrieval and Gemini as the LLM, orchestrated via LangGraph, with direct GitHub content sync capabilities.

## Project Structure

```
content/         ContentStore interface, local and GitHub sync implementations
ingestion/       parse JSON and PDF sources into chunks
embeddings/      embed chunks using Gemini embedding model
index/           build the FAISS index
data/            stores the built FAISS index, manifest, and content JSON files
portal_public/   static files for the web-based JSON Editor Portal
retrieval/       load the vector store, expand lab abbreviations, fetch announcements
tools/           LangChain tools that the agent can call
generation/      LangGraph agent graph with memory and LLM fallback chain
api/             FastAPI layer (routers, rate limiter, chat & content routes)
```

## Architecture & Content Synchronization

All website text data (notices, lab descriptions, team members, gallery items) is stored inside the Git repository as JSON files under `backend/data/content/`.

1. **Production Flow:** 
   - Edits in the **Editor Portal** send a `PUT` request to the backend.
   - The backend directly commits the updated JSON file to the GitHub repository using the GitHub REST API.
   - Render detects this commit, automatically rebuilds the Docker container, and runs `index/build_index.py` at startup to refresh the chatbot's knowledge base.
   - The live ECE Labs website fetches its data from the backend's `/content/{filename}` endpoint at load time.

2. **Optimistic Concurrency Control:**
   - The API uses Git blob SHAs to prevent concurrent edits from clobbering each other. If two users try to save modifications to the same file simultaneously, the second user will receive a clear conflict alert and will be prevented from overwriting the first user's changes.

## Setup

1. Copy `.env.example` to `.env` and fill in your keys:
   ```env
   GEMINI_API_KEY=your_key_here
   EMBEDDING_MODEL=models/gemini-embedding-2
   LLM_MODEL=gemini-flash-lite-latest

   # Required for GitHub sync in production (leave empty for local dev disk fallback)
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPO_OWNER=rahulpar2103
   GITHUB_REPO_NAME=ELEO-IIITD-chatbot
   GITHUB_BRANCH=master
   ```

2. *Note: The chatbot utilizes a native LangChain fallback chain. If the primary model `LLM_MODEL` fails, it automatically falls back to `gemini-2.5-flash` followed by `gemini-3.5-flash` using the same `GEMINI_API_KEY`.*

## Running locally

You can run the entire system (FastAPI backend + admin editor portal) with a single command. 

Double-click or run **`portal/run-portal.bat`** from the terminal. This will:
1. Start the FastAPI backend server on `http://localhost:8000`.
2. Automatically launch your default browser to the JSON Editor Portal at `http://localhost:8000/admin`.

*If `GITHUB_TOKEN` is not set in `.env`, the system automatically runs in local development mode, saving edits directly to `backend/data/content/` on your computer.*

## Running with Docker

Make sure Docker Desktop is open and running, then:

```bash
docker-compose up --build
```

API will be at `http://localhost:8000` and the Editor Portal will be at `http://localhost:8000/admin`. The FAISS index is built automatically inside the container during server startup.

To stop: `docker-compose down`

## API Endpoints

- `POST /chat` — Chatbot interaction route.
- `GET /content` — Lists all editable JSON content files.
- `GET /content/{filename}` — Returns the raw content of the JSON file with ETag/X-Content-SHA headers.
- `PUT /content/{filename}` — Updates the JSON file. Requires the header `If-Match` or `X-Content-SHA` to match the current file version on the server.

## Administrative Workflow (Non-Technical)

For the non-technical supervisor managing the ECE Labs website:
1. **Accessing the Portal:** Open the editor page (hosted at the Render backend's `/admin` path).
2. **Editing Content:** Select the file (e.g., `index.json` for announcements, labs, or gallery; or `be.json`, `dc.json` for specific labs) and select the section you want to modify.
3. **Saving Changes:** Click "Save File". The changes will be pushed directly to GitHub behind the scenes.
4. **Automatic Update:** Once saved, Render automatically builds and redeploys the backend (taking ~2-3 minutes). When finished, both the chatbot's knowledge and the live website's text are updated automatically. No technical commands, GitHub accounts, or server access are needed.
