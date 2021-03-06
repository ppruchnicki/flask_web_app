from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is True:
            flash('Already confirmed!', 'warning')
            return redirect(url_for('main.profile'))
        return func(*args, **kwargs)

    return decorated_function