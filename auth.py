from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_web_app.app import User, db
from flask_login import login_user, logout_user, login_required
from flask_web_app.forms import RegistrationForm, LoginForm


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

#@auth.route('/signup')
#def signup():
#    return render_template("signup.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists.', 'warning')
            return redirect(url_for('auth.signup'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=form.email.data, name=form.username.data, password=generate_password_hash(form.password.data, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You may now login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', title='Register', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))