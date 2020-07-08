from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_web_app.app import db, Todo
from flask_login import login_required, current_user
from flask_web_app.forms import TodosForm

todos = Blueprint('todos', __name__)

@todos.route('/todos')
@login_required
def show_todos():
    form = TodosForm()
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todos.html", name=current_user.name, todos=todos, form=form)


@todos.route('/todos/add', methods=['POST','GET'])
@login_required
def add_todo():
    form = TodosForm()
    if form.validate_on_submit():

        # create new todo with the form data
        new_todo = Todo(text=form.text.data, done=form.done.data, user_id=current_user.id)

        # add the new todo to the database
        db.session.add(new_todo)
        db.session.commit()

        flash('You have successfully added a todo.','success')
        return redirect(url_for('todos.show_todos'))

    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todos.html", name=current_user.name, todos=todos, form=form)


@todos.route('/delete_todo/<id>')
@login_required
def delete_todo(id):

    # filter specific node
    todo = Todo.query.filter_by(id=int(id)).first()

    # add the new todo to the database
    db.session.delete(todo)
    db.session.commit()

    flash('You have deleted the todo.','danger')
    return redirect(url_for('todos.show_todos'))


@todos.route('/edit_todo/<id>', methods=['POST','GET'])
@login_required
def edit_todo(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    print(todo.text)
    form = TodosForm()
    print(form.text.data)
    if form.validate_on_submit():
        print("into if")

        todo.text = form.text.data
        db.session.commit()
        
        flash('You have successfully edited the todo.','success')
        return redirect(url_for('todos.show_todos'))
    elif request.method == 'GET':
        form.text.data = todo.text
        print("into elif")
    
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todos.html", name=current_user.name, todos=todos, form=form)

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


