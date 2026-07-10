import sys
sys.path.append(".")

from retrieval.retriever import load_vectorstore

vectorstore = load_vectorstore()

results = vectorstore.similarity_search_with_score("BE lab", k=8)

for doc, score in results:
    print(round(score, 4), "-", doc.metadata.get("source"), "-", doc.page_content[:80])