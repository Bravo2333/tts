from sqlalchemy import Column, Integer, String,DateTime,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer,primary_key=True)
    link = Column(String)
    ownerlink = Column(String)
    uploadtime = Column(DateTime)
    isactivate = Column(Integer)
    spiderbegin = Column(Date)
    spiderend = Column(Date)
    def to_json(self):

        return {
            'link': self.link,
            'ownerlink': self.ownerlink,
            'uploadtime': self.uploadtime.strftime('%Y-%m-%d'),
            'isactivate': self.isactivate,
            'spiderbegin': self.spiderbegin,
            'spiderend': self.spiderend,
        }
