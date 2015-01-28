import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'postgres://swbzjtpjzoakwk:eCZTiE0gr6VXURN9FTS38guxxX@ec2-54-235-193-41.compute-1.amazonaws.com:5432/d37fueml6m5cpe'
#SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/puzzle'
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = 'thisissecret'
CSRF_ENABLED = True
SESSION_PROTECTION = 'strong'
