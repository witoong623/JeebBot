import sys
import uuid

import streamlit as st

from config import Config
from chatbot import Chatbot


st.set_page_config(page_title="จีบบอท", page_icon="❤️")


@st.cache_resource
def get_chatbot():
    if len(sys.argv) < 2:
        raise ValueError('Please provide a config file path as an positional argument')
    return Chatbot(Config(sys.argv[1]))


chatbot = get_chatbot()

st.title("จีบบอท ❤️")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def reset_bot():
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())


# Display settings sidebar
with st.sidebar:
    with st.form("settings"):
        st.text_input("ชื่อของบอท", key="bot_name")
        st.text_area("รายละเอียดของบอทว่าควรเป็นอย่างไร เช่น อาชีพ, นิสัย",
                     key="bot_character")
        st.form_submit_button("บันทึก", on_click=reset_bot)


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        chat_kwargs = {'msg': prompt, 'session_id': st.session_state.session_id}
        if st.session_state.bot_character:
            chat_kwargs['characteristic'] = st.session_state.bot_character
        if st.session_state.bot_name:
            chat_kwargs['name'] = st.session_state.bot_name
        resp_stream = chatbot.chat(**chat_kwargs)
        response = st.write_stream(map(lambda ret: ret.content, resp_stream))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
