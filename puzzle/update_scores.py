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

	users = session.query(User).filter(User.score > 0)

	for idx,val in enumerate(users):
		temp_timer = session.query(Timer).filter_by(challenge_id=1).filter_by(user_id=val.id).first()
		timeDelta = temp_timer.end_time - temp_timer.start_time
		print "Time elapsed: " + str(timeDelta)
		timeDelta = float((86400 - timeDelta)/86400.00) * 1000
		score = math.floor(10000 + timeDelta + ((15 - temp_timer.rank)/15.0 * 2000))
		val.score = score
		session.commit()

