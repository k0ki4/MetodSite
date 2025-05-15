from sqlalchemy import Column, String, Integer, Text
from data.db_session import SqlAlchemyBase

class TeamMember(SqlAlchemyBase):
    __tablename__ = 'team_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    role = Column(String(100), nullable=False)
    description = Column(Text)
    photo = Column(String(100)) # Название фото (пример pho.png)
    vk_link = Column(String(100))
    tg_link = Column(String(100))