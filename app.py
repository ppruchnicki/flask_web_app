from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from .login import login_manager
from .config import Config
import os
import datetime


app = Flask(__name__)
app.config.from_object(Config)

#db.init_app(app)

manager = Manager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)

from .models import Todo, Note, User

mail = Mail(app)

if __name__ == '__main__':
    manager.run()

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for notes part of app
from .notes import notes as notes_blueprint
app.register_blueprint(notes_blueprint)

# blueprint for todos part of app
from .todos import todos as todos_blueprint
app.register_blueprint(todos_blueprint)


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


admin = Admin(app, index_view=MyAdminIndexView(), name='Admin', template_mode='bootstrap3')

from .admin import admin

