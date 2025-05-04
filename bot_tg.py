import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from data.db_session import create_session
from data.tg_post import TelegramPost
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

logger = logging.getLogger(__name__)

# Список ID администраторов
ADMIN_IDS = {1240611937}


class TelegramBot:
    def __init__(self, token: str, channel_id: int):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.channel_id = channel_id
        self._setup_handlers()

    def _setup_handlers(self):
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            await message.answer("Бот готов к работе. Отправьте мне пост для публикации.")

        @self.dp.message(F.from_user.id.in_(ADMIN_IDS))
        async def handle_admin_post(message: types.Message):
            try:
                # if (message.forward_from_chat and
                #         message.forward_from_chat.id == self.channel_id):
                #     await message.answer("⚠ Этот пост уже находится в целевом канале!")
                #     return

                if await self._post_exists(message):
                    await message.answer("⚠ Этот пост уже существует в базе данных!")
                    return

                if await self._save_post(message):
                    await message.answer("✅ Пост успешно добавлен в канал и базу данных!")
                else:
                    await message.answer("⚠ Пост не был сохранен (ошибка базы данных).")

            except Exception as e:
                logger.error(f"Ошибка обработки поста: {e}")
                await message.answer(f"❌ Ошибка при обработке поста: {str(e)}")

        @self.dp.channel_post()
        async def handle_channel_post(post: types.Message):
            try:
                if not await self._post_exists(post):
                    await self._save_post(post)
            except Exception as e:
                logger.error(f"Ошибка сохранения поста из канала: {e}")

    async def _get_media_url(self, message: types.Message) -> Optional[str]:
        if message.photo:
            photo = message.photo[-1]
            file_info = await self.bot.get_file(photo.file_id)
            return f"https://api.telegram.org/file/bot{self.bot.token}/{file_info.file_path}"
        elif message.video:
            file_info = await self.bot.get_file(message.video.file_id)
            return f"https://api.telegram.org/file/bot{self.bot.token}/{file_info.file_path}"
        elif message.document:
            file_info = await self.bot.get_file(message.document.file_id)
            return f"https://api.telegram.org/file/bot{self.bot.token}/{file_info.file_path}"
        return None

    async def _post_exists(self, message: types.Message) -> bool:
        session = create_session()
        try:
            exists = session.query(TelegramPost).filter_by(
                message_id=message.message_id,
                channel_id=self.channel_id
            ).first()

            if exists:
                return True

            text = message.text or message.caption or ""
            if text:
                post_date = message.date or datetime.now()
                exists = session.query(TelegramPost).filter(
                    TelegramPost.text == text,
                    TelegramPost.channel_id == self.channel_id,
                    TelegramPost.date.between(
                        post_date.replace(hour=0, minute=0, second=0),
                        post_date.replace(hour=23, minute=59, second=59)
                    )).first()
                return exists is not None

            return False
        except SQLAlchemyError as e:
            logger.error(f"Ошибка проверки поста в БД: {e}")
            return False
        finally:
            session.close()

    async def _save_post(self, message: types.Message) -> bool:
        session = create_session()
        try:
            media_url = await self._get_media_url(message)

            new_post = TelegramPost(
                message_id=message.message_id,
                text=message.text or message.caption or "",
                media=media_url,
                date=message.date or datetime.now(),
                telegram_link=self._generate_post_link(message),
                channel_id=self.channel_id
            )
            session.add(new_post)
            session.commit()
            logger.info(f"Сохранён пост ID: {message.message_id}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Ошибка сохранения поста: {e}")
            return False
        finally:
            session.close()

    def _generate_post_link(self, message: types.Message) -> str:
        return f"https://t.me/c/{str(self.channel_id).replace('-100', '')}/{message.message_id}"

    async def start(self):
        await self.dp.start_polling(self.bot)


def run_bot(token: str, channel_id: int):
    bot = TelegramBot(token, channel_id)
    asyncio.run(bot.start())