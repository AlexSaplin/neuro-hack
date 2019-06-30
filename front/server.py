from flask import Flask, render_template, session, redirect, url_for, request
from services.users.users_interface import UsersInterface

app = Flask(__name__)
app.secret_key = b'Ya.TvoyOtez'
def start():
    app.run()

@app.route("/")
def hello():
    if 'user_id' not in session:
        return render_template("login.html")
    else:
        return redirect(url_for("listHandler"))

@app.route("/task/<id>")
def task(id):
    ui = UsersInterface()
    tasks = ui.get_tasks()
    current_task = None
    for task in tasks:
        if task.id == int(id):
            current_task = task
    return render_template("task-page.html", name=current_task.name, id=current_task.id, description=current_task.description,
                    author = ui.get_usermeta_by_id(current_task.author_id).name)

@app.route("/task/doTask/<id>", methods=['POST'])
def doTaskHandler(id):
    ui = UsersInterface()
    user_id = session['user_id']
    ui.add_task_executor(task_id=int(id), user_id=user_id)
    tasks = ui.get_tasks()
    current_task = None
    for task in tasks:
        if task.id == int(id):
            current_task = task
    return render_template("doTask.html", name=current_task.name, id=id)


@app.route("/completed/<id>", methods=["POST"])
def completeTaskHandler(id):
    ui = UsersInterface()
    user_id = session['user_id']
    ui.remove_task_executor(task_id=int(id), user_id=user_id)
    return redirect(url_for('listHandler'))

@app.route('/login', methods=['POST'])
def check():
    ui = UsersInterface()
    if ui.check_user_data(request.form['u'], request.form['p']):
        id = ui.check_user_data(request.form['u'], request.form['p'])
        session['user_id'] = id
        return  redirect(url_for('listHandler'))
    return render_template('login_failure.html')


@app.route('/register', methods=['POST'])
def reg():
    try:
        ui = UsersInterface()
        id = ui.add_user(request.form['u'], request.form['p'])
    except Exception as e:
        print(e)
        return render_template('reg_failure.html')
    session['user_id'] = id
    return redirect(url_for('listHandler'))

@app.route('/list')
def listHandler():
    ui = UsersInterface()
    tasks = ui.get_tasks()
    return render_template('list.html', tasks=tasks)

@app.route('/mylist')
def mylistHandler():
    ui = UsersInterface()
    user_id = session['user_id']
    tasks = ui.get_tasks(user_id=user_id)
    return render_template('mylist.html', tasks=tasks)

@app.route('/logout', methods=['POST', 'GET'])
def logoutHandler():
    del session['user_id']
    return render_template('login.html')

@app.route('/reg', methods=['POST', 'GET'])
def regHandler():
    return render_template('reg.html')

@app.route('/add_task')
def add_task_handler():
    return render_template('addTask.html')

@app.route('/commit_task', methods=['POST', 'GET'])
def commit_task_handler():
    ui = UsersInterface()
    user_id = session['user_id']
    ui.add_task(user_id=user_id, description=request.values['descriptionField'], duration=request.values['durationField'],
                name=request.values['nameField'])
    return redirect(url_for('listHandler'))