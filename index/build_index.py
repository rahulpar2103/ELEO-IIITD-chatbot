import sys
sys.path.append(".")

import time
import hashlib
import json as jsonlib
from pathlib import Path
from langchain_community.vectorstores import FAISS

from ingestion.load_pdf import load_pdf
from ingestion.load_json import load_json, extract_lab_content, extract_index_content, items_to_documents
from ingestion.clean import clean_documents
from ingestion.chunk import chunk_documents
from embeddings.embed import _get_embeddings


MANIFEST_PATH = "data/faiss_index_manifest.json"


def build_all_documents():
    frontend_dir = Path("../frontend")

    pdf_docs = []
    # Load PDFs from faq and policyandguidelines directories
    for path in (frontend_dir / "faq").glob("*.pdf"):
        pdf_docs.extend(load_pdf(str(path)))
    for path in (frontend_dir / "policyandguidelines").glob("*.pdf"):
        pdf_docs.extend(load_pdf(str(path)))

    lab_files = ["be.json", "dc.json", "cil.json", "rf.json", "sho.json", "ael.json"]
    all_items = []
    for filename in lab_files:
        data = load_json(str(frontend_dir / "data" / filename))
        all_items.extend(extract_lab_content(data, source=filename))
    index_data = load_json(str(frontend_dir / "data" / "index.json"))
    all_items.extend(extract_index_content(index_data, source="index.json"))
    json_docs = items_to_documents(all_items)

    all_docs = clean_documents(pdf_docs + json_docs)
    return chunk_documents(all_docs)


def compute_chunk_id(chunk, counters: dict) -> str:
    """Stable ID: source + a running count of chunks seen from that source."""
    source = chunk.metadata.get("source", "unknown")
    counters[source] = counters.get(source, -1) + 1
    return f"{source}::{counters[source]}"


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    path = Path(MANIFEST_PATH)
    if path.exists():
        return jsonlib.loads(path.read_text())
    return {}


def save_manifest(manifest: dict):
    Path(MANIFEST_PATH).write_text(jsonlib.dumps(manifest, indent=2))


if __name__ == "__main__":
    chunks = build_all_documents()
    print("Total chunks found:", len(chunks))

    manifest = load_manifest()
    new_or_changed = []
    counters = {}

    for chunk in chunks:
        chunk_id = compute_chunk_id(chunk, counters)
        chunk_hash = compute_hash(chunk.page_content)
        if manifest.get(chunk_id) != chunk_hash:
            new_or_changed.append((chunk_id, chunk_hash, chunk))

    print("Chunks needing embedding:", len(new_or_changed))

    if not new_or_changed:
        print("Nothing changed, index is up to date.")
    else:
        embeddings = _get_embeddings()
        index_path = Path("data/faiss_index")

        batch_size = 20
        vectorstore = None

        if index_path.exists():
            vectorstore = FAISS.load_local(
                "data/faiss_index", embeddings, allow_dangerous_deserialization=True
            )

        for i in range(0, len(new_or_changed), batch_size):
            batch_items = new_or_changed[i : i + batch_size]
            batch_docs = [c for (_, _, c) in batch_items]
            batch_ids = [chunk_id for (chunk_id, _, _) in batch_items]
            print(f"Embedding batch {i} to {i + len(batch_docs)}...")

            if vectorstore is None:
                vectorstore = FAISS.from_documents(batch_docs, embeddings, ids=batch_ids)
            else:
                stale_ids = [cid for cid in batch_ids if cid in manifest]
                if stale_ids:
                    vectorstore.delete(ids=stale_ids)
                vectorstore.add_documents(batch_docs, ids=batch_ids)

            if i + batch_size < len(new_or_changed):
                print("Pausing to respect rate limit...")
                time.sleep(15)

        vectorstore.save_local("data/faiss_index")

        for chunk_id, chunk_hash, _ in new_or_changed:
            manifest[chunk_id] = chunk_hash
        save_manifest(manifest)

        print("Index updated and saved.")