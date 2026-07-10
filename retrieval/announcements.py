import sys
sys.path.append(".")

from ingestion.load_json import load_json


def get_recent_announcements(limit: int = 5) -> list[dict]:
    """Read announcements directly from index.json, freshest first."""
    data = load_json("data/raw/index.json")
    announcements = data.get("announcements", [])
    return announcements[:limit]


if __name__ == "__main__":
    results = get_recent_announcements(limit=3)
    for a in results:
        print(a["date"], "-", a["title"])