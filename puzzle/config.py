import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
#SQLALCHEMY_DATABASE_URI = 'postgres://eedfuqmgrbyzml:0o1RVkhp7l9FS94kyk3nqfozrs@ec2-54-204-40-96.compute-1.amazonaws.com:5432/d8uars1eukmnaa'
SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/puzzle'
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = 'thisissecret'
CSRF_ENABLED = True
SESSION_PROTECTION = 'strong'
