import json
from langchain_core.documents import Document


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
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
    lab_files = ["be.json", "dc.json", "cil.json", "rf.json", "sho.json", "ael.json"]

    all_items = []
    for filename in lab_files:
        data = load_json(f"data/raw/{filename}")
        items = extract_lab_content(data, source=filename)
        all_items.extend(items)

    index_data = load_json("data/raw/index.json")
    all_items.extend(extract_index_content(index_data, source="index.json"))

    documents = items_to_documents(all_items)

    for doc in documents:
        print(doc.metadata["source"], "->", doc.metadata["section"], "->", len(doc.page_content), "characters")

    print("Total documents:", len(documents))