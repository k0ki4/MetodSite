from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from data.db_session import SqlAlchemyBase
from datetime import datetime


class GalleryPhoto(SqlAlchemyBase):
    __tablename__ = 'gallery_photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String(255), nullable=False)  # Путь к изображению
    title = Column(String(100), nullable=False)  # Название фото
    description = Column(Text)  # Описание фото
    created_at = Column(DateTime, default=datetime.now)  # Дата создания