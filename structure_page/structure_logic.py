from datetime import datetime

from flask import Blueprint, render_template

from data.db_session import create_session
from data.group import VKTeam
from data.structure import TeamMember

structure = Blueprint("structure", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates_structure')


@structure.route('/structure')
def show_page():
    session = create_session()
    team_members = session.query(TeamMember).all()
    current_team = session.query(VKTeam).first()

    return render_template('structure_page.html',
                         team=current_team,
                         team_members=team_members,
                         now=datetime.now())