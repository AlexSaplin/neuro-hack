from flask import Flask
from flask import render_template, sessions, redirect, url_for
from services.users.users_interface import UsersInterface
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("login.html")

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

@app.route("/doTask/<id>", methods='POST')
def doTaskHandler(id):
    ui = UsersInterface()
    user_id = sessions['user_id']
    ui.add_task_executor(task_id=int(id), user_id=user_id)
    tasks = ui.get_tasks()
    current_task = None
    for task in tasks:
        if task.id == int(id):
            current_task = task
    return render_template("doTask.html", name=current_task.name, id=id)


@app.route("/completed/<id>", methods="POST")
def completeTaskHandler(id):
    ui = UsersInterface()
    user_id = sessions['user_id']
    ui.remove_task_executor(task_id=int(id), user_id=user_id)
    return redirect(url_for('list'))

