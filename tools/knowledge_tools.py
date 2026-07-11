import sys
sys.path.append(".")
from langchain_core.tools import tool
from retrieval.retriever import load_vectorstore, expand_query
from retrieval.announcements import get_recent_announcements as _get_recent_announcements


@tool
def search_knowledge_base(query: str) -> str:
    """Search the ECE Labs knowledge base.

    Use this for any question about labs (BE, AEL, CIL, DC, RF, SHO),
    courses, equipment, facilities, team members, policies, and FAQs.
    Returns the most relevant text chunks from the knowledge base.
    """
    vectorstore = load_vectorstore()
    expanded = expand_query(query)
    results = vectorstore.similarity_search(expanded, k=4)
    return "\n\n".join(doc.page_content for doc in results)


@tool
def get_recent_announcements(limit: int = 5) -> str:
    """Fetch the latest announcements from the ECE Labs website.

    Use this when the user asks what is new, recent notices, latest updates,
    or anything time-sensitive. Returns date and title for each announcement.
    """
    announcements = _get_recent_announcements(limit)
    return "\n".join(f"{a['date']} - {a['title']}" for a in announcements)


if __name__ == "__main__":
    print(search_knowledge_base.invoke("What is the BE lab about?"))
    print("---")
    print(get_recent_announcements.invoke({"limit": 3}))