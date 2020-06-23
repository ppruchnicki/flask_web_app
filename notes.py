from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_web_app.app import db
from flask_web_app.models import Note
from flask_login import login_required, current_user

notes = Blueprint('notes', __name__)

@notes.route('/notes')
@login_required
def show_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", name=current_user.name, notes=notes)

@notes.route('/notes/add')
@login_required
def add_note():
    return render_template("notes_add.html")

@notes.route('/notes/add/post_note', methods=['POST'])
@login_required
def post_note():
    title = request.form.get('title')
    text = request.form.get('text')

    # create new note with the form data
    new_note = Note(title=title, text=text, user_id=current_user.id)

    # add the new note to the database
    db.session.add(new_note)
    db.session.commit()

    flash('You have successfully added a note.')
    return redirect(url_for('notes.show_notes'))

@notes.route('/delete_note/<id>')
@login_required
def delete_note(id):

    # filter specific node
    note = Note.query.filter_by(id=int(id)).first()

    # add the new note to the database
    db.session.delete(note)
    db.session.commit()

    flash('You have successfully deleted the note.')
    return redirect(url_for('notes.show_notes'))

@notes.route('/edit_note/<id>')
@login_required
def edit_note(id):
    note = Note.query.filter_by(id=int(id)).first()

    return render_template('notes_edit.html', note=note)

@notes.route('/edit_note/<id>/update', methods=['POST'])
@login_required
def update_note(id):
    note = Note.query.filter_by(id=int(id)).first()

    note.title = request.form.get('title')
    note.text = request.form.get('text')
    db.session.commit()

    flash('You have successfully edited the note.')
    return redirect(url_for('notes.show_notes'))


