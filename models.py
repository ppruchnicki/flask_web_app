from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_web_app.app import db, login_manager, app
import os
import datetime


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Todo %r>' % (self.text)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Note %r>' % (self.title)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    notes = db.relationship("Note", backref="user", lazy="dynamic") 
    todos = db.relationship("Todo",  backref="user", lazy="dynamic")

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_admin(self):
        return self.admin

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_confirmation_token(email, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

    def generate_email_change_token(self, new_email, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.commit()
        return True

    def confirm_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT']
            )
        except:
            return False
        return email

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

if not User.query.filter(User.email == 'ad@min.com').first():

        user = User(
            email='ad@min.com',
            password= generate_password_hash('Password1', method='sha256'),
            name='Admin',
            admin = True,
            confirmed = True,
            confirmed_on = datetime.datetime.now()
        )
        db.session.add(user)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))