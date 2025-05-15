from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from .db_session import SqlAlchemyBase


class VKTeam(SqlAlchemyBase):
    __tablename__ = 'vk_teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    captain_link = Column(String(255), nullable=False)
    group_link = Column(String(255), nullable=False)
    telegram_link = Column(String(255), nullable=False)
    group_id = Column(String(255), nullable=False)
    group_name = Column(String(255), nullable=False)
    photo = Column(String(255))  # Путь к изображению
    description = Column(Text)  # Для длинных описаний
    description2 = Column(Text)  # Для длинных описаний

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<VKTeam {self.id} - {self.group_link}>'