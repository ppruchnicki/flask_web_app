from flask import Flask, redirect, url_for
from flask_login import UserMixin, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from app import db, admin
from models import User, Note, Todo

class MyUserView(ModelView):
    form_columns = ['name', 'email', 'password', 'admin']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class MyAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated  

class AppMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated  

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyAdminView(Note, db.session))
admin.add_view(MyAdminView(Todo, db.session))
admin.add_link(LogoutMenuLink(name='App', category='', url="/"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))