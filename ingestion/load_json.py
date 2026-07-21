import json
from typing import Any, Iterable

from langchain_core.documents import Document


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


LAB_NAMES = {
    "be.json": "Basic Electronics Lab",
    "dc.json": "Digital Circuits Lab",
    "cil.json": "Circuits & Innovation Lab",
    "rf.json": "RF & Applied Electromagnetics Lab",
    "sho.json": "Shannon Lab",
    "ael.json": "Advanced ECE Lab",
}


def _normalize_resource_groups(data: dict) -> list[dict]:
    """Return resource groups from either the new grouped schema or the older flat one."""
    resources = data.get("resources", [])

    # New schema:
    # {
    #   "resources": {
    #       "total": ...,
    #       "groupCount": ...,
    #       "groups": [ ... ]
    #   }
    # }
    if isinstance(resources, dict):
        groups = resources.get("groups")
        if isinstance(groups, list):
            return groups
        # Some intermediate variants may store a direct flat list under resources.items/resources.list.
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

    # Another possible grouped shape: {"groups": [...]}
    if isinstance(data.get("groups"), list):
        return data["groups"]

    # Older flat schema: [{"title": ..., "category": ...}, ...]
    if isinstance(resources, list):
        return [{
            "id": "resources",
            "name": "Resources",
            "count": len(resources),
            "isMisc": False,
            "items": resources,
        }]

    return []


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\u00a0", " ").strip()
    return "" if text.lower() == "nan" else " ".join(text.split())


def _resource_item_text(lab_name: str, group_name: str, item: dict[str, Any]) -> str:
    title = _clean_text(item.get("title") or item.get("Resources") or item.get("name") or "Untitled resource")
    original_type = _clean_text(item.get("originalType") or item.get("group") or group_name)
    quantity = item.get("quantity", item.get("qty"))
    quantity_text = _clean_text(quantity) if quantity is not None and _clean_text(quantity) else "unspecified"
    status = _clean_text(item.get("status")) or "unspecified"
    remark = _clean_text(item.get("remark") or item.get("note") or item.get("description"))
    link = _clean_text(item.get("link") or item.get("quickLink") or item.get("referenceLink"))

    parts = [
        f"{lab_name} resource",
        f"Group: {group_name}",
        f"Item: {title}",
    ]
    if original_type and original_type != group_name:
        parts.append(f"Original type: {original_type}")
    parts.append(f"Quantity: {quantity_text}")
    parts.append(f"Status: {status}")
    if remark:
        parts.append(f"Remark: {remark}")
    if link:
        parts.append(f"Reference: {link}")
    return " | ".join(parts)


def _resource_group_text(lab_name: str, group: dict[str, Any]) -> str:
    group_name = _clean_text(group.get("name") or "Resources")
    count = group.get("count")
    items = group.get("items") or []
    titles = [
        _clean_text(item.get("title") or item.get("Resources") or item.get("name") or "")
        for item in items
    ]
    titles = [t for t in titles if t]
    summary = ", ".join(titles[:20])
    text = f"{lab_name} resource group | Group: {group_name} | Count: {count if count is not None else len(items)}"
    if summary:
        text += f" | Items: {summary}"
        if len(titles) > 20:
            text += f", and {len(titles) - 20} more"
    return text


def extract_lab_content(data: dict, source: str) -> list[dict]:
    items = []
    lab_name = LAB_NAMES.get(source, source)

    for course in data.get("courses", []):
        title = course.get("title")
        if title:
            text = f"{title} is a course taught in {lab_name}."
            items.append({"text": text, "source": source, "section": "courses"})

    for project in data.get("projects", []):
        title = project.get("title", "")
        date = project.get("date", "")
        description = project.get("description", "")
        text = f"{title} ({date}): {description}".strip()
        if text:
            items.append({"text": text, "source": source, "section": "projects"})

    for highlight in data.get("highlights", []):
        title = highlight.get("title", "")
        names = [n for n in highlight.get("names", []) if n and n != "-"]
        if title and names:
            text = f"{title}: {', '.join(names)}"
            items.append({"text": text, "source": source, "section": "highlights"})

    # Resource extraction supports both the older flat array and the new grouped inventory.
    for group in _normalize_resource_groups(data):
        group_name = _clean_text(group.get("name") or "Resources")
        group_text = _resource_group_text(lab_name, group)
        items.append({"text": group_text, "source": source, "section": "resources_group"})

        group_items = group.get("items") or []
        for item in group_items:
            text = _resource_item_text(lab_name, group_name, item)
            items.append({"text": text, "source": source, "section": "resources"})

    return items


def extract_index_content(data: dict, source: str) -> list[dict]:
    items = []

    for a in data.get("announcements", []):
        text = f"{a.get('title', '')} ({a.get('date', '')}): {a.get('description', '')}".strip()
        if text:
            items.append({"text": text, "source": source, "section": "announcements"})

    for lab in data.get("labs", []):
        text = f"{lab.get('name', '')} ({lab.get('room', '')}): {lab.get('description', '')}".strip()
        if text:
            items.append({"text": text, "source": source, "section": "labs"})

    for project in data.get("projects", []):
        title = project.get("title", "")
        date = project.get("date", "")
        description = project.get("description", "")
        text = f"{title} ({date}): {description}".strip()
        if text:
            items.append({"text": text, "source": source, "section": "projects"})

    for faq_block in data.get("faq", []):
        topic = faq_block.get("topic", "")
        questions = faq_block.get("questions", [])
        for q in questions:
            text = f"{topic}: {q}"
            items.append({"text": text, "source": source, "section": "faq"})

    for member in data.get("team", []):
        text = f"{member.get('name', '')}, {member.get('role', '')}: {member.get('bio', '')}".strip()
        if text:
            items.append({"text": text, "source": source, "section": "team"})

    credits = data.get("credits", {})
    chatbot_c = credits.get("chatbot", {})
    if chatbot_c:
        text = (
            f"The ELEO AI chatbot (v2) was developed by {chatbot_c.get('developer', '')} "
            f"(Roll No. {chatbot_c.get('roll', '')}, {chatbot_c.get('program', '')} "
            f"batch {chatbot_c.get('batch', '')} at {chatbot_c.get('institute', '')}). "
            f"ELEO is the AI assistant for ECE Labs. "
            f"The initial keyword-matching v1 prototype of ELEO was created by Jayan Pahuja."
        )
        items.append({"text": text, "source": source, "section": "credits"})
    website_c = credits.get("website", {})
    if website_c:
        members = ", ".join(
            f"{m['name']} ({m['roll']})" for m in website_c.get("team", [])
        )
        text = (
            f"The ECE Labs website (v2) was built by {members}, "
            f"all from {website_c.get('program', '')} batch {website_c.get('batch', '')} "
            f"at {website_c.get('institute', '')}."
        )
        items.append({"text": text, "source": source, "section": "credits"})

    people_overview = (
        "People involved in ECE Labs: "
        "The labs are managed by Research Engineers Ms. Sana Ali Naqvi, Mr. Khagendra Joshi, "
        "Mr. Abhishek Kumar, and Mr. Rahul Gupta. "
        "The ELEO AI chatbot (v2) was developed by Rahul Pardasani (M.Tech CSE 2025), "
        "upgrading the initial keyword-search v1 created by Jayan Pahuja. "
        "The ECE Labs website was built by Rahul Pardasani, Rohit Kumar, and Reehan Sarmah (M.Tech CSE 2025)."
    )
    items.append({"text": people_overview, "source": source, "section": "team_overview"})

    return items


def items_to_documents(items: list[dict]) -> list[Document]:
    return [
        Document(
            page_content=item["text"],
            metadata={"source": item["source"], "section": item["section"]},
        )
        for item in items
    ]


if __name__ == "__main__":
    from pathlib import Path
    frontend_dir = Path("./frontend") if Path("./frontend").exists() else Path("../frontend")
    lab_files = ["be.json", "dc.json", "cil.json", "rf.json", "sho.json", "ael.json"]

    all_items = []
    for filename in lab_files:
        data = load_json(str(frontend_dir / "data" / filename))
        items = extract_lab_content(data, source=filename)
        all_items.extend(items)

    index_data = load_json(str(frontend_dir / "data" / "index.json"))
    all_items.extend(extract_index_content(index_data, source="index.json"))

    documents = items_to_documents(all_items)

    for doc in documents:
        print(doc.metadata["source"], "->", doc.metadata["section"], "->", len(doc.page_content), "characters")

    print("Total documents:", len(documents))
