from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from config import Config


class Chatbot:
    ''' This class can't be serialized because one of langchain objects can't be serialized '''
    def __init__(self, config: Config):
        self.config = config

        chat_kwargs = {
            'openai_api_key': config.openai_api_key,
        }
        if config.openai_base_url:
            chat_kwargs['base_url'] = config.openai_base_url
        else:
            # it is OpenAI API, select model
            chat_kwargs['model'] = 'gpt-4o-mini'
        self.llm = ChatOpenAI(**chat_kwargs)
        self.store = {}
        self.setup_chain()

    def setup_chain(self):
        system_prompt = (
            "คุณเป็นคนธรรมดาคนหนึ่งที่ต้องการสนทนาเพื่อหาเพื่อน หรือพัฒนาความสัมพันธ์ "
            "กรุณาสทนา ตอบคำถาม ชวนสนทนาเรื่องต่างๆ หรือสอบถามข้อมูลต่างๆ โดยใช้ภาษาไทย "
            "โดยใช้ภาษาไม่เป็นทางการ และไม่ใช้ภาษาที่ไม่เหมาะสม "
            "คุณมีชื่อว่า ตูน และเพศของคุณจะเป็นเพศตรงข้ามกับผู้สนทนา"
        )
        # This prompt include input, previous conversation history and input message.
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        qa_chain = qa_prompt | self.llm

        self.conversation_chain = RunnableWithMessageHistory(
            qa_chain,
            self.get_session_history,
            input_messages_key="messages"
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self, msg, session_id="123"):
        return self.conversation_chain.stream(
            {"messages": [HumanMessage(content=msg)]},
            config={"configurable": {"session_id": session_id}}
        )
