from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, PasswordField
from wtforms.validators import DataRequired, Length

class AddPhotoForm(FlaskForm):
    title = StringField('Название фото', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Описание к фото')
    photo = FileField('Фото', validators=[DataRequired()])
    access_key = PasswordField('Ключ доступа', validators=[DataRequired()])