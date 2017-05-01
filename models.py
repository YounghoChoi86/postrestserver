from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Posting(Base):
    __tablename__ = 'posting'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    contents = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       	   'id': self.id,
           'name': self.name,
           'contents' : self.contents
       }

engine = create_engine('sqlite:///posting.db')
Base.metadata.create_all(engine)
