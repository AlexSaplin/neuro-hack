import flask
from services.users import users_interface

app = flask.Flask('users_interface', template_folder='html')


@app.route('/login', methods=['POST'])
def check():
    if app.users_interface.check_user_data(flask.request.form['u'], flask.request.form['p']):
        app.users_interface.add_user(flask.request.form['u'], flask.request.form['p'])
        return  # страница с кабинетом
    return flask.render_template('login_failure.html')


@app.route('/reg', methods=['POST'])
def reg():
    try:
        app.users_interface.add_user(flask.request.form['u'], flask.request.form['p'])
    except Exception as e:
        return flask.render_template('reg_failure.html')
    return  # страница с кабинетом
