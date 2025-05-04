import logging
import os

from flask import Flask, send_from_directory

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


app.config.update({
    'SECRET_KEY': 'K0ki4_176',
    'UPLOAD_FOLDER': os.path.join(app.root_path, 'static', 'uploads'),
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'},
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,
    'GALLERY_ACCESS_KEY': 'skype100',
    'TELEGRAM_BOT_TOKEN': '7865417152:AAGIPgzf-CIkGYGfMDEw29bxgeSWVGAEKcM',
    'TELEGRAM_CHANNEL_ID': -1002209355196,
    'TELEGRAM_CHANNEL_USERNAME': 'metodKVN',
    'ENABLE_TELEGRAM_BOT': True,
})
@app.route('/all_group_img/<filename>')
def serve_group_image(filename):
    images_dir = os.path.join(app.root_path, 'all_group_img')
    return send_from_directory(images_dir, filename)

from datetime import datetime

def datetimeformat(value, format='%d.%m.%Y %H:%M'):
    """Фильтр для форматирования даты в Jinja2"""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value).strftime(format)
    elif isinstance(value, datetime):
        return value.strftime(format)
    return value

# После создания app:
app.jinja_env.filters['datetimeformat'] = datetimeformat