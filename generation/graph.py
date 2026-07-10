import sys
sys.path.append(".")

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.knowledge_tools import search_knowledge_base, get_recent_announcements
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

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
    "You should give answers in conversational style and also in short and crisp manner."
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

memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "test-1"}}

    result = graph.invoke({"messages": [("user", "What is the BE lab about?")]}, config)
    print(result["messages"][-1].content[:200])

    print("---")

    result2 = graph.invoke({"messages": [("user", "Which room is it in?")]}, config)
    print(result2["messages"][-1].content[:200])

    print("---")

    config2 = {"configurable": {"thread_id": "test-2"}}
    result3 = graph.invoke({"messages": [("user", "Which room is it in?")]}, config2)
    print(result3["messages"][-1].content[:200])