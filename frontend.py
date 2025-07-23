# frontend.py
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
import streamlit as st
import requests

load_dotenv()

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.markdown("Create and Interact with the AI Agents!")

system_prompt = st.text_area(
    "Define your AI Agent:",
    height=70,
    placeholder="Type your system prompt here...",
    value="Act as an AI chatbot who is smart and friendly"
)

MODEL_NAMES_TOGETHER = ["llama3-8b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "lgai/exaone-3-5-32b-instruct"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Together", "OpenAI"))

if provider == "Together":
    selected_model = st.selectbox("Select Together Model:", MODEL_NAMES_TOGETHER)
else:
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search", value=False)

user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask Anything!",
    value="tell me about grok"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:9999/chat")

if st.button("Ask Agent!"):
    if user_query.strip() and system_prompt.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider.lower(),
            "system_prompt": system_prompt,
            "messages": [{"role": "user", "content": user_query}],
            "allow_search": allow_web_search
        }

        try:
            with st.spinner("Waiting for agent response..."):
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {response_data['response']}")
        except requests.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
            if 'response' in locals():
                st.write(f"Status Code: {response.status_code}")
                st.write(f"Response Text: {response.text}")
    else:
        st.error("Please provide both a system prompt and a query.")