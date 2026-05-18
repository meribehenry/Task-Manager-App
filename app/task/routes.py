from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from app.forms import TaskForm
from app.models import Task
from app.extensions import db

task = Blueprint("task", __name__)


@task.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()

    if form.validate_on_submit():
        task = form.task.data
        deadline = form.deadline.data

        task = Task(task=task, deadline=deadline, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()

        flash("Task added successfully", "success")
        return redirect(url_for("main.dashboard"))
    
    return render_template("task/add_task.html", form=form, title="Add Task")


@task.route("/update/<int:task_id>", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    form = TaskForm()

    task = Task.query.get_or_404(int(task_id))
    if current_user != task.user:
        abort(403)
    if form.validate_on_submit():
        task.task = form.task.data
        task.deadline = form.deadline.data
        db.session.commit()
        flash("Task successfully updated", "success")
        return redirect(url_for("task.view_task", task_id=task_id))

    elif request.method == "GET":
        form.task.data = task.task
        form.deadline.data = task.deadline 
    
    return render_template("task/add_task.html", form=form, title="Update Task")


@task.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(int(task_id))
    if current_user != task.user:
        abort(403)
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully", "success")
    return redirect(url_for("main.dashboard"))


@task.route("/mark/<int:task_id>")
@login_required
def mark_task(task_id):
    task = Task.query.get_or_404(int(task_id))
    if current_user != task.user:
        abort(403)
    if task.is_completed == False:
        task.is_completed = True
        task.user.completed_task +=  1       
        db.session.commit()
        flash("Task completed successfully", "success") 
    return redirect(url_for("task.view_task", task_id=task_id))

    
@task.route("/view/<int:task_id>")
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(int(task_id))
    if current_user != task.user:
        abort(403)
    return render_template("task/view_task.html", task=task, title="View Task")

