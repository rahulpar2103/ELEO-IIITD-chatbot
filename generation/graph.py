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
    "You are ELEO, the official assistant for the ECE Labs at IIIT Delhi. "
    "Your ONLY purpose is to answer questions about IIIT Delhi ECE Labs: "
    "lab facilities, courses, projects, equipment, team members, "
    "policies, FAQs, recent announcements, and details about who developed the chatbot or website.\n\n"

    "STRICT SCOPE RULE: If a user asks about anything outside ECE Labs "
    "(general knowledge, coding help, math, science, world events, jokes, etc.) "
    "you MUST politely decline. Say something like: "
    "'I am ELEO, the ECE Labs assistant at IIIT Delhi. I can only help with "
    "questions about our labs, courses, equipment, team, and announcements. "
    "For anything else, please reach out to the appropriate resource.'\n\n"

    "You do not have ECE Labs knowledge in your training data. "
    "For any in-scope question about labs, courses, projects, FAQs, team, "
    "policies, or creator credits, you MUST call search_knowledge_base. "
    "For questions about recent news or announcements, you MUST call "
    "get_recent_announcements. Never answer from memory or training data.\n\n"

    "Keep answers conversational, short, and crisp. "
    "Never use markdown, asterisks, bullet points, or any special formatting. Plain text only."
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