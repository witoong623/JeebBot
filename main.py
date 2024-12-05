import json
import os
import sys

import streamlit as st

from config import Config
from chatbot import Chatbot


DEFAULT_STATE_FILE = 'settings_store.json'
st.set_page_config(page_title="จีบบอท", page_icon="❤️")


@st.cache_resource
def get_chatbot():
    if len(sys.argv) < 2:
        raise ValueError('Please provide a config file path as an positional argument')
    return Chatbot(Config(sys.argv[1]))


def save_session_state(session_keys: list[str], file_path=DEFAULT_STATE_FILE):
    ''' Save session state to file. Primarily used to save user configuration settings. '''
    state = {k: st.session_state[k] for k in session_keys}
    with open(file_path, 'w') as f:
        json.dump(state, f, ensure_ascii=False)


def get_session_state(key: str, file_path=DEFAULT_STATE_FILE):
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as f:
        json_obj = json.load(f)
        return json_obj.get(key)


chatbot = get_chatbot()

st.title("จีบบอท ❤️")

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    # temporary make it one session mode
    st.session_state.session_id = '00000000-0000-0000-0000-000000000000'
if 'bot_name' not in st.session_state:
    st.session_state.bot_name = get_session_state('bot_name')
if 'bot_character' not in st.session_state:
    st.session_state.bot_character = get_session_state('bot_character')


# Display chat messages from history on app rerun
# TODO: save chat history to use across sessions
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def on_save_setting():
    st.session_state.messages = []
    # temporary make it one session mode, so don't create new session
    # however, once implement multi-session, reset_bot bot create new session or delete message history?
    chatbot.clear_session_history(st.session_state.session_id)

    save_session_state(['bot_name', 'bot_character'])


def on_delete_history_data():
    st.session_state.messages = []
    st.session_state.bot_name = None
    st.session_state.bot_character = None
    chatbot.clear_session_history(st.session_state.session_id)

    save_session_state(['bot_name', 'bot_character'])


def on_save_memory():
    chatbot.update_memory(st.session_state.session_id)
    

# Display settings sidebar
with st.sidebar:
    st.header("ตั้งค่า")

    with st.form("settings"):
        st.text_input("ชื่อของบอท", key="bot_name")
        st.text_area("รายละเอียดของบอทว่าควรเป็นอย่างไร เช่น อาชีพ, บุคลิกภาพ, นิสัย",
                     key="bot_character")
        st.form_submit_button("บันทึก", on_click=on_save_setting)

    st.divider()

    st.subheader("ความจำ")
    st.markdown("บันทึกประวัติการสนทนาที่ผ่านมาเป็นความจำของบอท")
    st.button("บันทึก", 'save_memory_button', on_click=on_save_memory)

    st.divider()

    st.subheader("ลบข้อมูล")
    st.markdown("ลบการตั้งค่า, ข้อความที่สนทนา และความจำทั้งหมด")
    st.button("ลบข้อมูล", 'delete_history_data_button', on_click=on_delete_history_data)


# React to user input
if prompt := st.chat_input("ข้อความ"):
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
