from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Master(Base):
    __tablename__ = 'master'
    link = Column(String, primary_key=True)
    deploydate = Column(DateTime)
    isactive = Column(Integer)
    def to_json(self):

        return {
            'link': self.link,
            'deploydate': self.deploydate,
            'isactive': self.isactive
        }
