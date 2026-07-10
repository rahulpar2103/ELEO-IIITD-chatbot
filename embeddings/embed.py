import os
from typing import Optional
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

_embeddings_model: Optional[GoogleGenerativeAIEmbeddings] = None

def _get_embeddings() -> GoogleGenerativeAIEmbeddings:
    global _embeddings_model
    if _embeddings_model is not None:
        return _embeddings_model

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    model_name = os.environ.get("EMBEDDING_MODEL", "models/gemini-embedding-001")

    _embeddings_model = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=api_key,
    )
    return _embeddings_model

def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a batch of chunks going INTO the vector store."""
    embeddings = _get_embeddings()
    return embeddings.embed_documents(texts)

def embed_query(text: str) -> list[float]:
    """Embed a user's question at search time."""
    embeddings = _get_embeddings()
    return embeddings.embed_query(text)


if __name__ == "__main__":
    chunk_texts = ["Basic Electronics", "Digital Circuits"]
    vectors = embed_documents(chunk_texts)
    print(len(vectors))
    print(len(vectors[0]))

    query_vector = embed_query("What courses does the BE lab teach?")
    print(len(query_vector))