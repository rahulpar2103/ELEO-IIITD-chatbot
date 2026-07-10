from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load()

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    pdf_paths = list(raw_dir.glob("*.pdf"))

    all_pdf_docs = []
    for path in pdf_paths:
        docs = load_pdf(str(path))
        all_pdf_docs.extend(docs)

    for doc in all_pdf_docs:
        print(doc.metadata["source"], "-> page", doc.metadata["page"], "->", len(doc.page_content), "characters")

    print("Total documents:", len(all_pdf_docs))