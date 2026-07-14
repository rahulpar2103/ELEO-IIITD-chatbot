import sys
from pathlib import Path

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


def _resource_groups_from_json(data: dict) -> list[dict]:
    resources = data.get("resources", [])
    if isinstance(resources, dict):
        groups = resources.get("groups")
        if isinstance(groups, list):
            return groups
        for key in ("items", "list", "resources"):
            maybe = resources.get(key)
            if isinstance(maybe, list):
                return [{
                    "id": "resources",
                    "name": "Resources",
                    "count": len(maybe),
                    "isMisc": False,
                    "items": maybe,
                }]
    if isinstance(resources, list):
        return [{
            "id": "resources",
            "name": "Resources",
            "count": len(resources),
            "isMisc": False,
            "items": resources,
        }]
    if isinstance(data.get("groups"), list):
        return data["groups"]
    return []


def _clean_text(value):
    if value is None:
        return ""
    text = str(value).replace("\u00a0", " ").strip()
    return "" if text.lower() == "nan" else " ".join(text.split())


def _format_item_line(item: dict) -> str:
    title = _clean_text(item.get("title") or item.get("Resources") or item.get("name") or "Unknown")
    original_type = _clean_text(item.get("originalType") or item.get("group") or "")
    quantity = item.get("quantity", item.get("qty"))
    quantity_text = _clean_text(quantity) if quantity is not None and _clean_text(quantity) else "unspecified"
    status = _clean_text(item.get("status")) or "unspecified"
    remark = _clean_text(item.get("remark") or item.get("note") or item.get("description"))
    link = _clean_text(item.get("link") or item.get("quickLink") or item.get("referenceLink"))

    details = [title]
    if original_type:
        details.append(original_type)
    details.append(f"Qty: {quantity_text}")
    details.append(f"Status: {status}")
    if remark:
        details.append(f"Remark: {remark}")
    if link:
        details.append(f"Link: {link}")
    return " | ".join(details)


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
    from ingestion.load_json import load_json, LAB_NAMES

    source = None
    query_lower = lab_name.lower().strip()
    for key, val in LAB_SOURCE_MAP.items():
        if key in query_lower:
            source = val
            break

    if not source:
        return f"Unknown lab '{lab_name}'. Valid options: be, dc, cil, rf, sho/shannon, ael."

    frontend_dir = Path("./frontend") if Path("./frontend").exists() else Path("../frontend")
    json_path = frontend_dir / "data" / source
    if not json_path.exists():
        return f"Data file not found for lab '{lab_name}'."

    data = load_json(str(json_path))
    groups = _resource_groups_from_json(data)

    if not groups:
        return f"No resources/equipment listed for {LAB_NAMES.get(source, lab_name)}."

    lab_display = LAB_NAMES.get(source, lab_name)
    total_items = sum(len(group.get("items", [])) for group in groups)
    lines = [f"{lab_display} resources ({total_items} total):"]

    for group in groups:
        group_name = _clean_text(group.get("name") or "Resources")
        items = group.get("items") or []
        if not items:
            continue
        group_count = group.get("count")
        if group_count is None:
            group_count = len(items)
        lines.append(f"\n{group_name} ({group_count})")
        for item in items:
            lines.append(f"- {_format_item_line(item)}")

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
