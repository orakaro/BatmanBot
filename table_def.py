#table_def.py
import sqlalchemy 
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///db/irclog.db', echo=True)
Base = declarative_base()

# Define
class ChatLog(Base):

    __tablename__ = "chatlog"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    user = Column(String)
    content = Column(String)

    def __init__(self, date, user, content):
        self.date = date
        self.user = user 
        self.content= content 

# Create
Base.metadata.create_all(engine)


