from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_web_app.app import db, mail
from flask_web_app.decorators import check_confirmed
from flask_login import login_required, current_user
from flask_web_app.models import User
from flask_web_app.forms import ChangePasswordForm, ChangeEmailForm
from flask_mail import Message
import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.current_password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Original password is invalid.', 'danger')
    return render_template("profile.html", form=form)

@main.route('/confirm/change-email/<token>')
@login_required
def confirm_email_change(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
        if current_user.confirmed:
            flash('Account already confirmed.', 'success')
        else:
            current_user.confirmed = True
            current_user.confirmed_on = datetime.datetime.now()
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.profile_change_email'))

def send_email_change_confirmation_email(new_email, confirm_url):
    msg = Message('Email change confirmation',
                  sender=('No Reply', 'noreply@demo.com'),
                  recipients=[new_email])
    msg.body = f'''To confirm email change, visit the following link:
<a href="{confirm_url}">confirmation link</a>
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@main.route('/profile/change-email', methods=['GET','POST'])
@login_required
def profile_change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            confirm_url = url_for('main.confirm_email_change', token=token, _external=True)
            send_email_change_confirmation_email(new_email, confirm_url)   
            
            flash(f'Confirmation of email change request was sent for {current_user.name}! Go to your email inbox and confirm.', 'success')
            return redirect(url_for('main.profile_change_email'))
            

    return render_template("profile_change_email.html", title='Register',form=form)

