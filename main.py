import sys

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

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Display settings sidebar
with st.sidebar:
    with st.form("settings"):
        bot_character = st.text_area("รายละเอียดของบอทว่าควรเป็นอย่างไร เช่น อาชีพ, นิสัย",
                                     key="bot_character")
        save_setting = st.form_submit_button("บันทึก")

    if save_setting:
        st.text(bot_character)


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(map(lambda ret: ret.content, chatbot.chat(prompt)))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
