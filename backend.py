# backend.py
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot import get_response_from_bot

class Message(BaseModel):
    role: str
    content: str

class RequestState(BaseModel):
    model_name: str
    model_provider: str
   s system_prompt: str
    messages: List[Message]
    allow_search: bool

ALLOWED_MODEL_NAMES = ["llama3-8b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini", "lgai/exaone-3-5-32b-instruct"]
ALLOWED_PROVIDERS = ["together", "openai"]

app = FastAPI(title="LangGraph AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat_endpoint(request: RequestState):
    print("Recieved: ", request.model_provider)
    
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": f"Invalid model name. Must be one of {ALLOWED_MODEL_NAMES}"}
    if request.model_provider not in ALLOWED_PROVIDERS:
        return {"error": f"Invalid provider. Must be one of {ALLOWED_PROVIDERS}"}
    llm_id = request.model_name
    query = request.messages[-1].content
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    try:
        response = get_response_from_bot(llm_id, query, allow_search, system_prompt, provider)
        return response
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}", "is_error": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)