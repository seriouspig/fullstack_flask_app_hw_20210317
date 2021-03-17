from flask import Flask, render_template, request , redirect
from flask import Blueprint
from repositories import task_repository, user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks",__name__)

@tasks_blueprint.route('/tasks')
def tasks():
    # get all the tasks
    tasks = task_repository.select_all()
    # return an HTML view listing all the tasks
    return render_template("tasks/index.html", all_tasks = tasks)

@tasks_blueprint.route('/tasks/new')
def new_task():
    # get all the users from the database
    users = user_repository.select_all()
    # return some html which displays a form to create a new task
    return render_template("tasks/new.html", all_users=users)

@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    # grab all the bits from the form and assign to variables
    description = request.form["description"]
    user_id = request.form["user"]
    duration = request.form["duration"]
    completed = request.form["completed"]
    # find the right user from the database based on the user id from the form data
    user = user_repository.select(user_id)
    # create a new Task object based on that form data
    task = Task(description,user, duration, completed )
    # save it to the database
    task_repository.save(task)
    # redirect back to all tasks view
    return redirect('/tasks')

@tasks_blueprint.route('/tasks/<id>', methods=['GET'])
def show_task(id):
    # capture the id parameter from the url
    # find the right task in the db by the id
    task = task_repository.select(id)
    # render an html view with the task details
    return render_template('tasks/show.html', selected_task=task)

@tasks_blueprint.route("/tasks/<id>/edit", methods=['GET'])
def edit_task(id):
    task = task_repository.select(id)
    users = user_repository.select_all()
    return render_template('tasks/edit.html', task = task, all_users = users)

@tasks_blueprint.route("/tasks/<id>", methods=['POST'])
def update_task(id):
    description = request.form['description']
    user_id     = request.form['user_id']
    duration    = request.form['duration']
    completed   = request.form['completed']
    user        = user_repository.select(user_id)
    task        = Task(description, user, duration, completed, id)
    task_repository.update(task)
    return redirect('/tasks')

@tasks_blueprint.route("/tasks/<id>/delete", methods=['POST'])
def delete_task(id):
    task_repository.delete(id)
    return redirect('/tasks')