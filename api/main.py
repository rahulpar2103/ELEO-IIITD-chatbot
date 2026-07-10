import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router)
