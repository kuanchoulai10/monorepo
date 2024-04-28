import json
import time
from pprint import pp

import requests
import streamlit as st

file_assistant_id_mappings = {
    "201309國民中學學校輔導工作參考手冊": "asst_IVnWFl5e2MicnUN4qVtwyrDi",
    "202210校園親密關係暴力事件實務處理手冊": "asst_p1nkdHdaq6SGCmk0rKSXfKds",
    "202301校園學生自我傷害防治手冊": "asst_cYlBdP6vhl4qWgRrZ2xcoRPx",
    "201704校園親密關係暴力事件實務處理手冊": "asst_dClRxv2mK3WopI0ugjWJsWaY"
}

st.header(f"個案分析")

openai_api_key = st.secrets["openai"]["api_key"]

file = st.selectbox(
    '文件：',
    file_assistant_id_mappings.keys(),
)
assistant_id = file_assistant_id_mappings[file]

instructions = st.text_area(
    "請指示代理人要幫你做什麼",
    "你是一個經驗豐富的台灣國中輔導老師，請根據「個案描述」，回答問題 (#zh-TW)"
)

if st.button("重置對話"):
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_message := st.chat_input("詢問問題"):
    if not instructions:
        st.warning("請先輸入指示再詢問問題")
        st.stop()
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_message)
    # Add user message to chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        headers = {
            "Authorization": f'Bearer {openai_api_key}',
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        # Create a Thread
        # https://platform.openai.com/docs/api-reference/threads/createThread
        response = requests.post(
            'https://api.openai.com/v1/threads',
            headers=headers,
            data=json.dumps(
                {
                    "messages": st.session_state.messages
                }
            )
        )
        obj = json.loads(response.text)
        thread_id = obj.get("id")
        print(f"Thread Created: {thread_id}")
        # Create a Run
        # https://platform.openai.com/docs/api-reference/runs/createRun
        response = requests.post(
            f"https://api.openai.com/v1/threads/{thread_id}/runs",
            headers=headers,
            data=json.dumps(
                {
                    "assistant_id": assistant_id,
                    "instructions": instructions,
                    "tools": [{"type": "file_search"}]
                }
            )
        )
        obj = json.loads(response.text)
        pp(obj)
        run_id = obj.get("id")
        print(f"Run Created: {run_id}")
        # Observe the run
        # https://platform.openai.com/docs/api-reference/runs/getRun
        status = ""
        while status!="completed":
            print(f"Status: {status}")
            time.sleep(10)
            response = requests.get(
                f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
                headers=headers
            )
            obj = json.loads(response.text)
            print("==============================")
            pp(obj)
            status = obj.get('status', "")
        # Check messages
        response = requests.get(
            f"https://api.openai.com/v1/threads/{thread_id}/messages",
            headers=headers
        )
        obj = json.loads(response.text)
        # assitant_message = obj['data'][0]['content'][0]['text']['value']
        assitant_message = obj.get("data", [{}])[0]\
                            .get("content", [{}])[0]\
                            .get("text", {})\
                            .get("value")
        st.markdown(assitant_message)
    # Add user message to chat history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assitant_message
        }
    )
