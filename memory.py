from typing import Optional

from sqlalchemy import create_engine, Integer, Text, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, DeclarativeBase, scoped_session, sessionmaker, mapped_column


class Base(DeclarativeBase):
    pass


class ChatMemoryModel(Base):
    __tablename__ = "chat_memory"

    id = mapped_column(Integer, primary_key=True)
    session_id = mapped_column(Text, nullable=False)
    content = mapped_column(Text, nullable=False)



class ChatMemory:
    _table_created = False

    def __init__(self, session_id: str, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.session_maker = scoped_session(sessionmaker(bind=self.engine))

        self._table_created = False
        if not ChatMemory._table_created:
            Base.metadata.create_all(self.engine)
            ChatMemory._table_created = True

        self.session_id = session_id

    @property
    def content(self) -> str | None:
        with self.session_maker() as session:
            select_memory = select(ChatMemoryModel).where(ChatMemoryModel.session_id == self.session_id)

            ret = session.scalars(select_memory).first()
            return ret.content if ret else None

    def update_memory(self, content: str):
        with self.session_maker() as session:
            select_memory = select(ChatMemoryModel).where(ChatMemoryModel.session_id == self.session_id)
            memory = session.scalars(select_memory).first()

            if memory:
                memory.content = content
            else:
                memory = ChatMemoryModel(session_id=self.session_id, content=content)
                session.add(memory)
            session.commit()


__all__ = ["ChatMemory"]
