import sys
sys.path.append(".")
from langchain_core.tools import tool
from retrieval.retriever import load_vectorstore, expand_query
from retrieval.announcements import get_recent_announcements as _get_recent_announcements


@tool
def search_knowledge_base(query: str) -> str:
    """Search the ECE Labs knowledge base for info about labs, courses, projects, FAQs, team, and policies."""
    vectorstore = load_vectorstore()
    expanded = expand_query(query)
    results = vectorstore.similarity_search(expanded, k=4)
    return "\n\n".join(doc.page_content for doc in results)


@tool
def get_recent_announcements(limit: int = 5) -> str:
    """Get the most recent announcements from the ECE Labs website. Use this for questions about what's new or recent."""
    announcements = _get_recent_announcements(limit)
    return "\n".join(f"{a['date']} - {a['title']}" for a in announcements)


if __name__ == "__main__":
    print(search_knowledge_base.invoke("What is the BE lab about?"))
    print("---")
    print(get_recent_announcements.invoke({"limit": 3}))