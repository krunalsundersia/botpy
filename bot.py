# bot.py
# -*- coding: utf-8 -*-
import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

def get_response_from_bot(llm_id: str, query: str, allow_search: bool, system_prompt: str, provider: str):
    try:
        TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY") or "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"
        TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY") or "848fd886c39d477aa5c9e775bc9f7327e9f2b449e6eeee1ec889af8d1b2e3a20"

        if not TAVILY_API_KEY and allow_search:
            return {"error": "Please provide a valid TAVILY_API_KEY.", "is_error": True}
        if not TOGETHER_API_KEY and provider.lower() == "togetherai":
            return {"error": "Please provide a valid TOGETHER_API_KEY.", "is_error": True}

        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

        if provider.lower() == "together":
            llm = ChatOpenAI(
                model=llm_id,
                api_key=TOGETHER_API_KEY,
                base_url="https://api.together.xyz/v1"
            )
        else:
            return {"error": f"Unsupported provider: {provider}. Currently, only 'togetherai' is supported.", "is_error": True}

        # tools = [TavilySearch(max_results=1)] if allow_search else []
        tools = []
        agent = create_react_agent(model=llm, tools=tools)
        print(agent)

        state = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
        }

        response = agent.invoke(state)
        return {"response": response["messages"][-1].content, "is_error": False}
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}", "is_error": True}

if __name__ == "__main__":
    print("--- Using Together AI ---")
    try:
        together_ai_model = "lgai/exaone-3-5-32b-instruct"
        together_response = get_response_from_bot(
            llm_id=together_ai_model,
            query="What is the capital of France?",
            allow_search=True,
            system_prompt="You are a helpful assistant.",
            provider="togetherai"
        )
        if together_response.get("is_error"):
            print(f"Error: {together_response['error']}")
        else:
            print(f"Together AI Response: {together_response['response']}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")