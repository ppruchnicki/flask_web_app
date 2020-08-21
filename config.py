import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', default ='secret') 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT', default = 'wordpass')
    MAIL_SERVER = config('MAIL_SERVER' , default = 'smtp.mail.com')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL_USER', default = 'mail@mail.com') 
    MAIL_PASSWORD = config('MAIL_PASSWORD', default = 'wordpass') 
    FLASK_ADMIN_SWATCH = 'yeti'