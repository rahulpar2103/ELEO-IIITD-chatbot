import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(router)
