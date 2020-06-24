from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_web_app.app import db, Todo
from flask_login import login_required, current_user

todos = Blueprint('todos', __name__)

@todos.route('/todos')
@login_required
def show_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todos.html", name=current_user.name, todos=todos)


@todos.route('/todos/add', methods=['POST'])
@login_required
def post_todo():
    text = request.form.get('text')
    done = request.form.get('done')

    # create new todo with the form data
    new_todo = Todo(text=text, done=done, user_id=current_user.id)

    # add the new todo to the database
    db.session.add(new_todo)
    db.session.commit()

    flash('You have successfully added a todo.')
    return redirect(url_for('todos.show_todos'))

@todos.route('/delete_todo/<id>')
@login_required
def delete_todo(id):

    # filter specific node
    todo = Todo.query.filter_by(id=int(id)).first()

    # add the new todo to the database
    db.session.delete(todo)
    db.session.commit()

    flash('You have successfully deleted the todo.')
    return redirect(url_for('todos.show_todos'))


@todos.route('/edit_todo/<id>', methods=['POST'])
@login_required
def update_todo(id):
    todo = Todo.query.filter_by(id=int(id)).first()

    todo.text = request.form.get('text')
    #todo.done = request.form.get('done')
    db.session.commit()

    flash('You have successfully edited the todo.')
    return redirect(url_for('todos.show_todos'))

@todos.route('/check/<id>')
@login_required
def check_todo(id):
    todo = Todo.query.filter_by(id=int(id)).first()

    todo.done = True
    db.session.commit()

    return redirect(url_for('todos.show_todos'))

@todos.route('/uncheck/<id>')
@login_required
def uncheck_todo(id):
    todo = Todo.query.filter_by(id=int(id)).first()

    todo.done = False
    db.session.commit()

    return redirect(url_for('todos.show_todos'))


