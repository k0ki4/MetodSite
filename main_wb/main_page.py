import os
from datetime import datetime

from flask import Blueprint, render_template, send_from_directory, current_app

from data.capitan import TeamCaptain
from data.db_session import create_session
from data.group import VKTeam
from data.organize import Organizer

main = Blueprint("main", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')


@main.route('/')
def team_page():
    db_sess = create_session()
    team = db_sess.query(VKTeam).first()

    captain = db_sess.query(TeamCaptain).first()
    organizers = db_sess.query(Organizer).all()

    return render_template(
        'page.html',
        team=team,
        captain=captain,
        organizers=organizers,
        now=datetime.now()
    )


@main.route('/img/<filename>')
def serve_images(filename):
    img_dir = os.path.join(current_app.root_path, 'main_wb', 'img')
    return send_from_directory(img_dir, filename)