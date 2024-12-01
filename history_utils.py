import json

from langchain_community.chat_message_histories.sql import DefaultMessageConverter
from langchain_core.messages import message_to_dict


class UTF8MessageConverter(DefaultMessageConverter):
    def to_sql_model(self, message, session_id: str):
        return self.model_class(
            session_id=session_id, message=json.dumps(message_to_dict(message), ensure_ascii=False)
        )
