from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger

from .db_session import SqlAlchemyBase


class TelegramPost(SqlAlchemyBase):
    __tablename__ = 'telegram_posts'
    __table_args__ = (
        sqlalchemy.Index('ix_telegram_posts_message_id', 'message_id', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, nullable=False, unique=True)
    text = Column(Text)
    media = Column(String(255))  # URL или путь к медиафайлу
    date = Column(DateTime, nullable=False)
    telegram_link = Column(String(255), nullable=False)
    channel_id = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<TelegramPost {self.message_id} from {self.channel_id}>'