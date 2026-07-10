import sys
sys.path.append(".")

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.knowledge_tools import search_knowledge_base, get_recent_announcements

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.environ.get("LLM_MODEL", "gemini-2.0-flash"),
    google_api_key=os.environ.get("GEMINI_API_KEY"),
)

llm_with_tools = llm.bind_tools([search_knowledge_base, get_recent_announcements])

if __name__ == "__main__":
    response = llm_with_tools.invoke("What is the BE lab about?")
    print(response.tool_calls)

    response2 = llm_with_tools.invoke("What's the latest announcement?")
    print(response2.tool_calls)