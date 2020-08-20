from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash
from app import app
from models import db, User
import datetime

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

def create_admin():
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
    return