from flask import Blueprint, render_template, current_app, jsonify, request
from datetime import datetime
import logging

from sqlalchemy import desc

from __init import app
from data.db_session import create_session
from data.group import VKTeam
from data.tg_post import TelegramPost

news_bp = Blueprint('news', __name__,
                    static_folder='img',
                    static_url_path='/img',
                    template_folder='templates_post')
logger = logging.getLogger(__name__)


@news_bp.route('/api/news')
def get_news():
    try:
        # Получаем параметры пагинации
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 5, type=int)
        offset = (page - 1) * limit

        session = create_session()

        # Запрос для получения общего количества постов
        total_posts = session.query(TelegramPost).count()

        # Получаем посты с пагинацией, сортировка по дате (новые сначала)
        posts = session.query(TelegramPost) \
            .order_by(desc(TelegramPost.date)) \
            .offset(offset) \
            .limit(limit) \
            .all()

        # Форматируем данные для ответа
        posts_data = []
        for post in posts:
            post_data = {
                'message_id': post.message_id,
                'original_message_id': getattr(post, 'original_message_id', post.message_id),
                'text': post.text,
                'media': post.media,
                'media_type': getattr(post, 'media_type', None),
                'date': post.date.isoformat(),
                'telegram_link': post.telegram_link,
                'channel_id': post.channel_id
            }
            posts_data.append(post_data)

        # Проверяем, есть ли еще посты для загрузки
        has_more = (offset + limit) < total_posts

        return jsonify({
            'success': True,
            'posts': posts_data,
            'total': total_posts,
            'has_more': has_more
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    finally:
        session.close()


@news_bp.route('/news')
def news_page():
    session = create_session()

    team = session.query(VKTeam).first()

    return render_template('page_post.html',
                           team=team,
                           telegram_channel=app.config.get('TELEGRAM_CHANNEL_USERNAME'),
                           now=datetime.now())
