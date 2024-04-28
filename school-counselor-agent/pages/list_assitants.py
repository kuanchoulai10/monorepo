import json
import time

import requests
import streamlit as st

st.header(f"List Assitants")

openai_api_key = st.secrets["openai"]["api_key"]

headers = {
    "Authorization": f'Bearer {openai_api_key}',
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v1"
}


requests.get(
    "https://api.openai.com/v1/assistants",
    headers=headers,
    data=json.dumps(
        {}
    )
)