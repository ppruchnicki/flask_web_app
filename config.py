import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY') #'+=uo_)pczyks9(3dtpg2kgn-%g08=v'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT') #'basdhHUIASDgvmsda38jn'
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL_USER') #'pp3148212@gmail.com'
    MAIL_PASSWORD = config('MAIL_PASSWORD') #'beTk7VQnFHKr3j3'
    FLASK_ADMIN_SWATCH = 'yeti'