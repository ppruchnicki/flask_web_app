from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_web_app.app import db, Note
from flask_login import login_required, current_user
from flask_web_app.forms import NotesForm

notes = Blueprint('notes', __name__)

@notes.route('/notes')
@login_required
def show_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", name=current_user.name, notes=notes)

@notes.route('/notes/add', methods=['POST', 'GET'])
@login_required
def add_note():
    form = NotesForm()
    if form.validate_on_submit():

        # create new note with the form data
        new_note = Note(title=form.title.data, text=form.text.data, user_id=current_user.id)

        # add the new note to the database
        db.session.add(new_note)
        db.session.commit()

        flash('You have successfully added a note.','success')
        return redirect(url_for('notes.show_notes'))
    
    return render_template("notes_add.html", title='Add Note', form=form)

@notes.route('/delete_note/<id>')
@login_required
def delete_note(id):

    # filter specific node
    note = Note.query.filter_by(id=int(id)).first()

    # add the new note to the database
    db.session.delete(note)
    db.session.commit()

    flash('You have deleted the note.','danger')
    return redirect(url_for('notes.show_notes'))

@notes.route('/edit_note/<id>', methods=['POST','GET'])
@login_required
def edit_note(id):
    note = Note.query.filter_by(id=int(id)).first()
    form = NotesForm()
    if form.validate_on_submit():

        db.session.commit()

        flash('You have successfully edited the note.','success')
        return redirect(url_for('notes.show_notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.text.data = note.text

    return render_template('notes_edit.html', form=form, note=note)


