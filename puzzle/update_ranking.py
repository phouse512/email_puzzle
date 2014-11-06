from sqlalchemy.ext.declarative import declarative_base
from models import User, Timer
Base = declarative_base()
import math

if __name__ == '__main__':
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	#PWD = os.path.abspath(os.curdir)

	engine = create_engine('postgres://eedfuqmgrbyzml:0o1RVkhp7l9FS94kyk3nqfozrs@ec2-54-204-40-96.compute-1.amazonaws.com:5432/d8uars1eukmnaa', echo=True)
	#engine = create_engine('postgres://PhilipHouse:house@localhost/puzzle', echo=True)
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()

	user = session.query(Timer).filter(Timer.end_time > 0).filter_by(challenge_id=1)
	#session.add(user)
	#session.commit()
	rank = []
	for idx,val in enumerate(user):
		rank.append((idx+1, val.user_id))

	for idx,val in enumerate(user):
		val.rank = rank[idx][0]
		session.commit()


