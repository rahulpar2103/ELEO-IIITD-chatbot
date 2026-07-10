import sys
sys.path.append(".")

import logging

from generation.graph import graph

logger = logging.getLogger(__name__)

FALLBACK = "I'm having trouble answering right now, please try again in a moment."


def invoke_graph(message: str, session_id: str) -> str:
    config = {"configurable": {"thread_id": session_id}}
    try:
        result = graph.invoke({"messages": [("user", message)]}, config)
        return result["messages"][-1].content
    except Exception as e:
        logger.error("Graph invocation failed for session %s: %s", session_id, e)
        return FALLBACK
