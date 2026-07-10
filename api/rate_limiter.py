import time
from collections import defaultdict

from fastapi import HTTPException

RATE_LIMIT = 10
WINDOW_SECONDS = 3600

# maps session_id to list of request timestamps within the current window
_session_timestamps: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(session_id: str) -> None:
    now = time.time()
    _session_timestamps[session_id] = [
        t for t in _session_timestamps[session_id] if now - t < WINDOW_SECONDS
    ]
    if len(_session_timestamps[session_id]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="You're sending messages too quickly, please wait a bit before trying again.",
        )
    _session_timestamps[session_id].append(now)
