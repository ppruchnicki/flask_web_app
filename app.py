from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
import os
import datetime


app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')


#db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

mail = Mail(app)

migrate = Migrate(app, db)
manager = Manager(app)

from flask_web_app import models

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# blueprint for auth routes in our app
from flask_web_app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from flask_web_app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for notes part of app
from flask_web_app.notes import notes as notes_blueprint
app.register_blueprint(notes_blueprint)

# blueprint for todos part of app
from flask_web_app.todos import todos as todos_blueprint
app.register_blueprint(todos_blueprint)


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


admin = Admin(app, index_view=MyAdminIndexView(), name='Home', template_mode='bootstrap3')

from flask_web_app import admin

