import os
import threading

from __init import app
from bot_tg import run_bot
from data import db_session
from gallery_page.gallery_logic import gallery_bp
from main_wb.main_page import main
from structure_page.structure_logic import structure
from tg_post_web.page_route_for_tg import news_bp


def start():
    db_session.global_init("db/live.db")
    app.register_blueprint(main)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(structure)
    app.register_blueprint(news_bp)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    if app.config['ENABLE_TELEGRAM_BOT']:
        bot_thread = threading.Thread(
            target=run_bot,
            args=(
                app.config['TELEGRAM_BOT_TOKEN'],
                app.config['TELEGRAM_CHANNEL_ID'],
            ),
            daemon=True
        )
        bot_thread.start()
        app.logger.info("Telegram Bot запущен в фоновом режиме")
    app.run(debug=True, port=8080, use_reloader=False)


if __name__ == '__main__':
    start()
