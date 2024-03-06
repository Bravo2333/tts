from sqlalchemy import create_engine, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Masterinfo(Base):
    __tablename__ = 'masterinfo'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    account = Column(String)
    ipaddress = Column(String)
    follow = Column(Integer)
    followed = Column(Integer)
    nickname = Column(String)
    likecount = Column(Integer)
    updatetime = Column(DateTime)
    def to_json(self):

        return {
            'id': self.id,
            'link': self.link[:-1],
            'account': self.account,
            'ipaddress': self.ipaddress,
            'follow': self.follow,
            'followed': self.followed,
            'nickname': self.nickname,
            'likecount': self.likecount,
            'updatetime': self.updatetime.strftime('%Y-%m-%d'),
        }