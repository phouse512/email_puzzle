from datetime import datetime
import os
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

""" User """
class User(Base):
	__tablename__ = 'puzzle_user'

	id = Column(Integer, primary_key=True)
	username = Column(String(100))
	email = Column(String(200))
	score = Column(Integer)

	def __init__(self, username, email):
		self.username = username
		self.email = email
		self.score = 0

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.username

""" Challenge Timer """
class Timer(Base):
	__tablename__ = 'timer'

	id = Column(Integer, primary_key=True)
	start_time = Column(Integer)
	end_time = Column(Integer)
	challenge_id = Column(Integer, ForeignKey('challenge.id'))
	challenge = relationship("Challenge", backref=backref('timers', order_by=id))
	user_id = Column(Integer, ForeignKey('puzzle_user.id'))
	user = relationship("User", backref=backref('timers', order_by=id))
	hint_used = Column(Boolean)


	def __init__(self, start_time, challenge_id, user_id):
		self.user_id = user_id
		self.start_time = start_time
		self.challenge_id = challenge_id
		self.hint_used = False


	def __repr__(self):
		return '<Timer %r>' % self.start_time

""" Challenge """ 
class Challenge(Base):
	__tablename__ = 'challenge'

	id = Column(Integer, primary_key=True)
	title = Column(String(200))
	answer = Column(String(300))
	prompt = Column(Text)
	weight = Column(Integer)
	active = Column(Boolean)
	hint = Column(Text)

	def __init__(self, title,answer, weight, prompt, hint):
		self.title = title
		self.answer = answer
		self.weight = weight
		self.prompt = prompt
		self.active = False
		self.hint = hint

	def __repr__(self):
		return '<Challenge %r>' % self.prompt

if __name__ == '__main__':
	#from datetime import timedelta

	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	#PWD = os.path.abspath(os.curdir)

	engine = create_engine('postgres://PhilipHouse:house@localhost/puzzle', echo=True)

	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()

	user = User(username='phouse512', email='philiphouse2015@u.northwestern.edu')
	session.add(user)
	session.commit()
