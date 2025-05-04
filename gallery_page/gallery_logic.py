from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from data.db_session import create_session
from data.group import VKTeam
from data.photo_store import GalleryPhoto

gallery_bp = Blueprint('gallery', __name__, template_folder='templates_gallery')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@gallery_bp.route('/gallery')
def show_gallery():
    db_sess = create_session()
    photos = db_sess.query(GalleryPhoto).order_by(GalleryPhoto.created_at.desc()).all()
    team = db_sess.query(VKTeam).first()
    return render_template('gallery.html',
                           gallery_photos=photos,
                           now=datetime.now(),
                           team=team)


@gallery_bp.route('/gallery/add', methods=['POST'])
def add_photo():
    if 'photo' not in request.files:
        flash('Фото не загружено', 'danger')
        return redirect(url_for('gallery.show_gallery'))

    file = request.files['photo']

    if file.filename == '':
        flash('Не выбрано фото', 'danger')
        return redirect(url_for('gallery.show_gallery'))

    if request.form.get('access_key') != current_app.config['GALLERY_ACCESS_KEY']:
        flash('Неверный ключ доступа', 'danger')
        return redirect(url_for('gallery.show_gallery'))

    if not allowed_file(file.filename):
        flash('Недопустимый формат файла', 'danger')
        return redirect(url_for('gallery.show_gallery'))

    filename = secure_filename(file.filename)

    gallery_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'gallery')
    os.makedirs(gallery_folder, exist_ok=True)
    save_path = os.path.join(gallery_folder, filename)

    try:
        file.save(save_path)

        db_sess = create_session()
        photo = GalleryPhoto(
            image_path=filename,
            title=request.form.get('title', 'Без названия'),
            description=request.form.get('description')
        )
        db_sess.add(photo)
        db_sess.commit()

        flash('Фото успешно добавлено в галерею!', 'success')
    except Exception as e:
        flash(f'Ошибка при сохранении фото: {str(e)}', 'danger')

    return redirect(url_for('gallery.show_gallery'))
