from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from ingestion.load_pdf import load_pdf
    from ingestion.load_json import load_json, extract_lab_content, extract_index_content, items_to_documents
    from ingestion.clean import clean_documents
    from pathlib import Path

    raw_dir = Path("data/raw")

    pdf_docs = []
    for path in raw_dir.glob("*.pdf"):
        pdf_docs.extend(load_pdf(str(path)))

    lab_files = ["be.json", "dc.json", "cil.json", "rf.json", "sho.json", "ael.json"]
    all_items = []
    for filename in lab_files:
        data = load_json(f"data/raw/{filename}")
        all_items.extend(extract_lab_content(data, source=filename))
    index_data = load_json("data/raw/index.json")
    all_items.extend(extract_index_content(index_data, source="index.json"))
    json_docs = items_to_documents(all_items)

    all_docs = clean_documents(pdf_docs + json_docs)
    chunks = chunk_documents(all_docs)

    print("Original documents (PDF pages + JSON items):", len(all_docs))
    print("Chunks after splitting:", len(chunks))

    same_count = sum(1 for c in chunks if len(c.page_content) < 500)
    print("Chunks under 500 chars (likely untouched JSON items):", same_count)