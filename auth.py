from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_web_app.app import db, mail
from flask_web_app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_web_app.decorators import is_confirmed
from flask_web_app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
import datetime


auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = User.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))

def send_confirmation_email(user, confirm_url):
    msg = Message('Account confirmation',
                  sender=('No Reply', 'noreply@demo.com'),
                  recipients=[user.email])
    msg.body = f'''To confirm your account, visit the following link:
<a href="{confirm_url}">confirmation link</a>
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@auth.route('/unconfirmed')
@login_required
@is_confirmed
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.profile')
    #flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists.', 'warning')
            return redirect(url_for('auth.signup'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(
                email=form.email.data, 
                name=form.username.data, 
                password=generate_password_hash(form.password.data, method='sha256'),
                confirmed = False
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        token = User.generate_confirmation_token(form.email.data)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        send_confirmation_email(new_user, confirm_url)

        flash(f'Confirmation email sent for {form.username.data}! Go to your email inbox and confirm.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', title='Register', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check if user actually exists
        user = User.query.filter_by(email=form.email.data).first()
        
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=form.remember.data)

        if current_user.confirmed:
            return redirect(url_for('main.profile'))
        return redirect(url_for('auth.unconfirmed'))
        
    
    return render_template("login.html", title='Login', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=('No Reply', 'noreply@demo.com'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@auth.route('/resend')
@login_required
@is_confirmed
def resend_confirmation():
    token = User.generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    send_confirmation_email(current_user, confirm_url)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)    