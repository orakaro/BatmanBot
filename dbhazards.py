import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import ChatLog

#Create a chat record
def log(date,user,content):
    engine = create_engine('sqlite:///irclog.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    chatlog = ChatLog(date,user,content)
    session.add(chatlog)
    session.commit()

#log(datetime.date(1970,01,01),"Batman","Batman Rock The Gotham")


