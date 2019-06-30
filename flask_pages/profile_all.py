import flask
from services.users import users_interface
from flask import session
from flask_table import Table, Col
app = flask.Flask('users_interface', template_folder='html')


@app.route('/')
def show_page():
    tasks = app.users_interface.get_tasks()
    return render_template('cabinet_all.html', tasks=tasks)

