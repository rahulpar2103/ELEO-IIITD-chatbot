import sys
sys.path.append(".")

from langchain_community.vectorstores import FAISS
from embeddings.embed import _get_embeddings

LAB_ABBREVIATIONS = {
    "be": "Basic Electronics Lab",
    "dc": "Digital Circuits Lab",
    "cil": "Circuits & Innovation Lab",
    "rf": "RF & Applied Electromagnetics Lab",
    "sho": "Shannon Lab",
    "ael": "Advanced ECE Lab",
}


def expand_query(query: str) -> str:
    words = query.lower().split()
    expanded = [LAB_ABBREVIATIONS.get(w, w) for w in words]
    return " ".join(expanded)
def load_vectorstore() -> FAISS:
    """Load the FAISS index that build_index.py created."""
    embeddings = _get_embeddings()
    return FAISS.load_local(
        "data/faiss_index", embeddings, allow_dangerous_deserialization=True
    )


if __name__ == "__main__":
    vs = load_vectorstore()
    results = vs.similarity_search("What is the BE lab about?", k=2)
    for r in results:
        print(r.page_content[:100])