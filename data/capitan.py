from sqlalchemy import Column, String, Integer

from data.db_session import SqlAlchemyBase


class TeamCaptain(SqlAlchemyBase):
    __tablename__ = 'team_captain'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    photo = Column(String(100))