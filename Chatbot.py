from openai import OpenAI
import streamlit as st
import requests
import json
from neumai.Client.NeumClient import NeumClient

query_params = st.experimental_get_query_params()

if "neumai_api_key" not in st.session_state:
    st.session_state["neumai_api_key"] = query_params.get("neumai_api_key", [""])[0]
if "neumai_pipeline_id" not in st.session_state:
    st.session_state["neumai_pipeline_id"] = query_params.get("neumai_pipeline_id", [""])[0]
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""
if "context" not in st.session_state:
    st.session_state["context"] = ""
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = "You are a helpful assistant that answers questions based on the following context:{}. Limit your answers to the context provided."

with st.sidebar:
    st.title("Neum AI Chatbot")
    st.markdown("Neum AI helps you connect and synchronize your data to a vector database. Simply set up a pipeline and let Neum AI automatically synchronize your data.")
    st.markdown("This app allows you to chat with the data connected to your pipeline")
    st.markdown("To get started [create](https://dashboard.neum.ai/) a Neum AI account and [setup](https://docs.neum.ai/docs/build-in-the-ui) your data pipeline.")
    neumai_api_key = st.text_input("Neum AI API Key", key="neumai_api_key", type="password", value=st.session_state["neumai_api_key"])
    neumai_pipeline_id = st.text_input("Neum AI Pipeline ID", key="neumai_pipeline_id", value=st.session_state["neumai_pipeline_id"])
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value=st.session_state["openai_api_key"])
    include_context = st.toggle("Include context in messages", True)
    system_prompt = st.toggle("Change system prompt", False)
    if system_prompt:
        initial_value = st.session_state["system_prompt"]
        st.session_state["system_prompt"] = st.text_area(label="System Prompt", value=initial_value, height=200)

st.title("Chat with your pipeline")
st.caption("Simple chatbot powered by Neum AI and OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "system", "content": st.session_state["system_prompt"].format(st.session_state["context"])})
    st.session_state["messages"].append({"role": "assistant", "content": "How can I help you?", "context":""})

for msg in st.session_state.messages:
    if(msg["role"] != "system"):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and msg["context"] != "" and include_context:
                with st.expander("Context"):
                    st.text(msg["context"])

if prompt := st.chat_input():
    if not openai_api_key or not neumai_api_key or not neumai_pipeline_id:
        st.info("Please add your API key and Pipeline ID to continue.")
        st.stop()

    # Get context from Neum AI

    neumClient = NeumClient(api_key=neumai_api_key)
    json_response = neumClient.search_pipeline(pipeline_id=neumai_pipeline_id, query=prompt, num_of_results=5)
    # Extract the 'results' list from the JSON response
    # Additional metadata fields are available as well as id and score.
    results = [ json.loads(result)['metadata']['text'] for result in json_response] 
    st.session_state["context"] = '\n\n'.join(results)
    st.session_state["messages"][0] = {"role": "system", "content": st.session_state["system_prompt"].format(st.session_state["context"])}

    # Request to Open AI
    client = OpenAI(
        api_key=openai_api_key
    )

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    messages = [{k: v for k, v in item.items() if k != 'context'} for item in st.session_state.messages]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role":"assistant", "content":msg, "context":st.session_state["context"]})
    with st.chat_message("assistant"):
        st.write(msg)
        if include_context:
            with st.expander("Context"):
                st.text(st.session_state["context"])
