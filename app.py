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


app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

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

manager.add_command('db', MigrateCommand)

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
    notes = db.relationship("Note", backref="user", lazy="dynamic") 
    todos = db.relationship("Todo",  backref="user", lazy="dynamic")

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_admin(self):
        return self.admin

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
            admin = True,
            name='Admin'
        )
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    manager.run()

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

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

class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

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

admin = Admin(app, index_view=MyAdminIndexView(), name='Home', template_mode='bootstrap3')
admin.add_view(MyUserView(User, db.session))
admin.add_view(MyAdminView(Note, db.session))
admin.add_view(MyAdminView(Todo, db.session))
admin.add_link(LogoutMenuLink(name='App', category='', url="/"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

