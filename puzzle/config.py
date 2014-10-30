import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/puzzle'
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = 'thisissecret'
CSRF_ENABLED = True
SESSION_PROTECTION = 'strong'
