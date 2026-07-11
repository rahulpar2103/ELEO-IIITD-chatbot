import sys
sys.path.append(".")

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.knowledge_tools import search_knowledge_base, get_recent_announcements

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
primary_model = os.environ.get("LLM_MODEL", "gemini-flash-lite-latest")
fallback_models = ["gemini-2.5-flash", "gemini-3.5-flash"]

primary_llm = ChatGoogleGenerativeAI(
    model=primary_model,
    google_api_key=api_key,
)

fallbacks = [
    ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
    for model_name in fallback_models
]

tools = [search_knowledge_base, get_recent_announcements]
primary_with_tools = primary_llm.bind_tools(tools)
fallbacks_with_tools = [f_llm.bind_tools(tools) for f_llm in fallbacks]

llm_with_tools = primary_with_tools.with_fallbacks(fallbacks_with_tools)

if __name__ == "__main__":
    print("--- Listing Available Models from Google API ---")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for m in client.models.list():
            # Filter models to find the ones that support generation
            print(f" - {m.name}")
    except Exception as e:
        print("Failed to list models:", e)

    print("\n--- Individual Model Diagnostic Test ---")
    print(f"Testing Primary Model ({primary_model})...")
    try:
        response = primary_with_tools.invoke("What is the BE lab about?")
        print("Primary Success:", response.tool_calls)
    except Exception as e:
        print("Primary Error:", type(e), e)

    for idx, (fallback_model_name, fallback_runnable) in enumerate(zip(fallback_models, fallbacks_with_tools)):
        print(f"\nTesting Fallback Model {idx + 1} ({fallback_model_name})...")
        try:
            response = fallback_runnable.invoke("What is the BE lab about?")
            print(f"Fallback {idx + 1} Success:", response.tool_calls)
        except Exception as e:
            print(f"Fallback {idx + 1} Error:", type(e), e)

    print("\n--- Fallback Chain Test ---")
    try:
        response = llm_with_tools.invoke("What is the BE lab about?")
        print("Fallback Chain Success:", response.tool_calls)
    except Exception as e:
        print("Fallback Chain Error:", type(e), e)