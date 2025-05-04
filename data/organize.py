from sqlalchemy import Column, String, Integer

from data.db_session import SqlAlchemyBase


class Organizer(SqlAlchemyBase):
    __tablename__ = 'organizers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    photo = Column(String(100))  # Только имя файла, например: "org1.jpg"
    position = Column(String(100))  # Должность/роль организатора
    vk_link = Column(String(255))  # Ссылка на профиль
