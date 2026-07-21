import logging
import os
import sys

# Ensure backend root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.router import router as chat_router
from api.content_router import router as content_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https://(.*\.)?iiitd\.ac\.in",
    allow_methods=["GET", "POST", "PUT", "HEAD", "OPTIONS"],
    allow_headers=["Content-Type", "If-Match", "X-Content-SHA"],
    expose_headers=["ETag", "X-Content-SHA"],
)

app.include_router(chat_router)
app.include_router(content_router)

@app.get("/")
async def root():
    return {"message": "ELEO Chatbot & Content API is running", "health": "/health", "admin": "/admin"}

@app.get("/health")
@app.head("/health")
async def health_check():
    return {"status": "ok"}

# Serve the portal UI at /admin
portal_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "portal_public"))
if os.path.exists(portal_dir):
    app.mount("/admin", StaticFiles(directory=portal_dir, html=True), name="portal")

