import json
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

    for resource in data.get("resources", []):
        title = resource.get("title", "")
        category = resource.get("category", "")
        subtitle = resource.get("subtitle", "")
        overview = resource.get("overview", "")
        specs = resource.get("specs", [])
        applications = resource.get("applications", [])

        specs_text = "; ".join(
            f"{s['key']}: {s['val']}" for s in specs if s.get("key") and s.get("val")
        )
        apps_text = ", ".join(applications)

        parts = [
            f"{lab_name} has {title} ({category}): {subtitle}.",
        ]
        if overview:
            parts.append(overview)
        if specs_text:
            parts.append(f"Specifications — {specs_text}.")
        if apps_text:
            parts.append(f"Applications: {apps_text}.")

        text = " ".join(parts).strip()
        if text:
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
            f"The ELEO AI chatbot was developed by {chatbot_c.get('developer', '')} "
            f"(Roll No. {chatbot_c.get('roll', '')}, {chatbot_c.get('program', '')} "
            f"batch {chatbot_c.get('batch', '')} at {chatbot_c.get('institute', '')})."
        )
        items.append({"text": text, "source": source, "section": "credits"})
    website_c = credits.get("website", {})
    if website_c:
        members = ", ".join(
            f"{m['name']} ({m['roll']})" for m in website_c.get("team", [])
        )
        text = (
            f"The ECE Labs website was built by {members}, "
            f"all from {website_c.get('program', '')} batch {website_c.get('batch', '')} "
            f"at {website_c.get('institute', '')}."
        )
        items.append({"text": text, "source": source, "section": "credits"})

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