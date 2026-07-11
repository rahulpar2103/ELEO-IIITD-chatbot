import sys
sys.path.append(".")
from langchain_core.tools import tool
from retrieval.retriever import load_vectorstore, expand_query
from retrieval.announcements import get_recent_announcements as _get_recent_announcements

LAB_SOURCE_MAP = {
    "be": "be.json",
    "basic electronics": "be.json",
    "dc": "dc.json",
    "digital circuits": "dc.json",
    "cil": "cil.json",
    "circuits and innovation": "cil.json",
    "rf": "rf.json",
    "applied electromagnetics": "rf.json",
    "sho": "sho.json",
    "shannon": "sho.json",
    "ael": "ael.json",
    "advanced ece": "ael.json",
}


@tool
def search_knowledge_base(query: str) -> str:
    """Search the ECE Labs knowledge base.

    Use this for any question about labs (BE, AEL, CIL, DC, RF, SHO),
    courses, equipment, facilities, team members, policies, and FAQs.
    Returns the most relevant text chunks from the knowledge base.
    """
    vectorstore = load_vectorstore()
    expanded = expand_query(query)
    results = vectorstore.similarity_search(expanded, k=20)
    return "\n\n".join(doc.page_content for doc in results)


@tool
def search_lab_resources(lab_name: str) -> str:
    """Get the complete list of all equipment and resources for a specific lab.

    Use this when the user asks for ALL equipment, resources, or instruments
    in a specific lab. lab_name can be: 'be', 'dc', 'cil', 'rf', 'sho'/'shannon', 'ael'.
    Returns EVERY resource entry for that lab directly from the source data.
    """
    from pathlib import Path
    from ingestion.load_json import load_json, LAB_NAMES

    source = None
    query_lower = lab_name.lower().strip()
    for key, val in LAB_SOURCE_MAP.items():
        if key in query_lower:
            source = val
            break

    if not source:
        return f"Unknown lab '{lab_name}'. Valid options: be, dc, cil, rf, sho/shannon, ael."

    # Read directly from the JSON file — guaranteed complete, no FAISS ranking cutoff
    frontend_dir = Path("./frontend") if Path("./frontend").exists() else Path("../frontend")
    json_path = frontend_dir / "data" / source
    if not json_path.exists():
        return f"Data file not found for lab '{lab_name}'."

    data = load_json(str(json_path))
    resources = data.get("resources", [])

    if not resources:
        return f"No resources/equipment listed for {LAB_NAMES.get(source, lab_name)}."

    lab_display = LAB_NAMES.get(source, lab_name)
    lines = [f"{lab_display} has the following resources ({len(resources)} total):"]
    for r in resources:
        title = r.get("title", "Unknown")
        category = r.get("category", "")
        subtitle = r.get("subtitle", "")
        lines.append(f"- {title} ({category}): {subtitle}")

    return "\n".join(lines)


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