from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

import templates as tp
from config import Config
from history_utils import UTF8MessageConverter
from memory import ChatMemory


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
        self.conversation_llm = ChatOpenAI(**chat_kwargs)
        self.summary_llm = ChatOpenAI(temperature=0.0, **chat_kwargs)
        self.store = {}
        self.memory = {}
        self.setup_chain()

    def setup_chain(self):
        self.trimmer = trim_messages(
            max_tokens=2000,
            strategy='last',
            # we use the same LLM class for both conversation and summary
            # so we can use either of them to count tokens
            token_counter=self.conversation_llm,
            include_system=True,
        )
        # TODO: system prompt needs to be changed to match what user set in the settings (bot_name, bot_character)
        # when user continue to chat next time, probably need to be done through streamlit session state
        conversation_prompt = ChatPromptTemplate.from_messages([
            ("system", tp.DEFAULT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ])

        conversation_chain = conversation_prompt | self.trimmer | self.conversation_llm
        self.conversation_chain = RunnableWithMessageHistory(
            conversation_chain,
            self.get_session_history,
            input_messages_key="messages"
        )

        summary_prompt = ChatPromptTemplate.from_template(tp.SUMMARY_PROMPT)
        self.summary_chain = summary_prompt | self.trimmer | self.summary_llm

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        # history contains HumanMessage and AIMessage but not SystemMessage, is it by design?
        return SQLChatMessageHistory(
            session_id=session_id, connection="sqlite:///chat_history.db",
            custom_message_converter=UTF8MessageConverter('message_store')
        )

    def clear_session_history(self, session_id: str):
        history = self.get_session_history(session_id)
        history.clear()

    def update_memory(self, session_id):
        history = self.get_session_history(session_id)
        messages = history.messages
        # TODO: Maybe it is better to use the name of bot instead of "AI" in the formatted_messages
        formatted_messages = "\n".join([f"AI: {m.content}" if isinstance(m, AIMessage) else f"User: {m.content}"
                                        for m in messages])
        summary_args = {
            'messages': formatted_messages
        }

        # get previous memory to be initial memory context
        if session_id in self.memory:
            previous_summary_prompt = tp.MEMORY_CONTEXT_PROMPT.format(previous_memory=self.memory[session_id])
            summary_args['previous_summary_prompt'] = previous_summary_prompt
        else:
            summary_args['previous_summary_prompt'] = ''

        summary = self.summary_chain.invoke(summary_args)

        memory = ChatMemory(session_id, "sqlite:///chat_memory.db")
        memory.update_memory(summary.content)

    def chat(self, msg, session_id,
             name=tp.DEFAULT_BOT_NAME,
             characteristic=tp.DEFAULT_BOT_CHARACTERISTICS):
        # get memory context and add it to the conversation
        chat_memory = ChatMemory(session_id, "sqlite:///chat_memory.db")
        if (chat_memory_content := chat_memory.content):
            memory_context = tp.MEMORY_CONTEXT_PROMPT.format(memory=chat_memory_content)
        else:
            memory_context = ''

        return self.conversation_chain.stream(
            {"messages": [HumanMessage(content=msg)],
             "name": name,
             "character": characteristic,
             'memory_context': memory_context},
             config={"configurable": {"session_id": session_id}}
        )
