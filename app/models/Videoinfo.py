from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Videoinfo(Base):
    __tablename__ = 'videoinfo'
    id = Column(Integer,primary_key=True)
    link = Column(String)
    likecount = Column(Integer)
    ownerlink = Column(String)
    updatetime = Column(DateTime)
    text = Column(String)
    comment = Column(Integer)
    follow_shot_bgm = Column(String)
    follow_shot_bgm_count = Column(Integer)
    collect = Column(Integer)
    uploadtime = Column(Date)
    fatchid = Column(Integer)

    def to_json(self):
        return {
            'link': self.link,
            'likecount': self.likecount,
            'ownerlink': self.ownerlink,
            'updatetime': self.updatetime,
            'text': self.text,
            'comment': self.comment,
            'follow_shot_bgm': self.follow_shot_bgm,
            'follow_shot_bgm_count': self.follow_shot_bgm_count,
            'collect': self.collect,
            'uploadtime': self.uploadtime.strftime('%Y-%m-%d'),
            'fatchid': self.fatchid,
        }
    def to_json_owner(self,owner):
        return {
            'owner':owner,
            'link': self.link,
            'likecount': self.likecount,
            'ownerlink': self.ownerlink,
            'updatetime': self.updatetime.strftime('%Y-%m-%d'),
            'text': self.text,
            'comment': self.comment,
            'follow_shot_bgm': self.follow_shot_bgm,
            'follow_shot_bgm_count': self.follow_shot_bgm_count,
            'collect': self.collect,
            'uploadtime': self.uploadtime.strftime('%Y-%m-%d'),
            'fatchid': self.fatchid,
        }
