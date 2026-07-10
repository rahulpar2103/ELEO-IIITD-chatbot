import sys
sys.path.append(".")

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.knowledge_tools import search_knowledge_base, get_recent_announcements
from langchain_core.messages import SystemMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.environ.get("LLM_MODEL", "gemini-2.0-flash"),
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)
SYSTEM_PROMPT = SystemMessage(content=(
    "You are the ECE Labs assistant. You do not know anything about ECE Labs "
    "from your own knowledge. For any question about labs, courses, projects, "
    "FAQs, team members, or policies, you must call search_knowledge_base. "
    "For any question about what's new or recent, you must call "
    "get_recent_announcements. Never answer from memory."
))


tools = [search_knowledge_base, get_recent_announcements]
llm_with_tools = llm.bind_tools(tools)


def agent_node(state: MessagesState):
    response = llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"messages": [("user", "What is the BE lab about?")]})
    for m in result["messages"]:
        print(type(m).__name__, "-", getattr(m, "tool_calls", None) or m.content[:100])
        print()

    graph.get_graph().draw_mermaid_png(output_file_path="generation/graph.png")