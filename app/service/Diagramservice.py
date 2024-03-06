from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.models.Master import Master
from app.models.Video import Video
from app.models.Videoinfo import Videoinfo
from app.models.Masterinfo import Masterinfo


class Diagramservice():
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://root:root2333@localhost:3306/spider')
        pass

    def get_master_list(self):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        masters = dbsession.query(Master).all()
        mastersinfolist = []
        for i in masters:
            ownerlink = i.link
            masterlatestinfo = dbsession.query(Masterinfo).filter_by(link=ownerlink).order_by(
                (desc(Masterinfo.updatetime))).first()
            if masterlatestinfo == None:
                continue
            mastersinfolist.append(masterlatestinfo.to_json())
        dbsession.commit()
        dbsession.close()
        return mastersinfolist

    def get_master_totalinfo(self, ownerlink):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        result = []
        masterlatestinfo = dbsession.query(Masterinfo).filter_by(link=ownerlink).all()
        for i in masterlatestinfo:
            result.append(i.to_json())
        dbsession.commit()
        dbsession.close()
        return result

    def get_master_videolist(self, ownerlink):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        result = []
        videolinks = dbsession.query(Video).filter_by(ownerlink=ownerlink).all()
        if len(videolinks) == 0:
            return 'no video'
        for i in videolinks:
            latestvideoinfo = dbsession.query(Videoinfo).filter_by(link=i.link).order_by(
                desc(Videoinfo.updatetime)).first()
            if latestvideoinfo is None:
                continue
            result.append(latestvideoinfo.to_json())
        dbsession.commit()
        dbsession.close()
        return result

    def videodatasolve(self, videolink):
        pass

    def get_Masterrankinfo(self):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        Masters = dbsession.query(Master).filter_by(isactive=1).all()
        result = []
        for i in Masters:
            rankonemaster = {}
            onemasterinfo = dbsession.query(Masterinfo).filter_by(link=i.link).order_by(desc('updatetime')).all()
            rankonemaster['Masterlink'] = i.link
            rankonemaster['Masternickname'] = onemasterinfo[0].nickname
            if len(onemasterinfo) == 1:
                rankonemaster['Three_day_like_increasing'] = 0
                rankonemaster['Three_day_like_increasing_count'] = 0
                rankonemaster['One_day_like_increasing'] = 0
                rankonemaster['One_day_like_increasing_count'] = 0
                rankonemaster['to_current_likecount_increasing'] = 0

                rankonemaster['Three_day_followed_increasing'] = 0
                rankonemaster['Three_day_followed_increasing_count'] = 0
                rankonemaster['One_day_followed_increasing'] = 0
                rankonemaster['One_day_followed_increasing_count'] = 0
                rankonemaster['to_current_followed_increasing'] = 0
                rankonemaster['trace_days'] = 1
                result.append(rankonemaster)
                continue
            if len(onemasterinfo) <= 3:
                rankonemaster['Three_day_like_increasing'] = 0
                rankonemaster['Three_day_like_increasing_count'] = 0
                rankonemaster['One_day_like_increasing'] = (onemasterinfo[0].likecount - onemasterinfo[1].likecount) / (
                            onemasterinfo[1].likecount * 1.0)
                rankonemaster['One_day_like_increasing_count'] = onemasterinfo[0].likecount - onemasterinfo[1].likecount
                rankonemaster['to_current_likecount_increasing'] = onemasterinfo[0].likecount - onemasterinfo[
                    -1].likecount

                rankonemaster['Three_day_followed_increasing'] = 0
                rankonemaster['Three_day_followed_increasing_count'] = 0
                rankonemaster['One_day_followed_increasing'] = (onemasterinfo[0].followed - onemasterinfo[
                    1].followed) / (onemasterinfo[1].likecount * 1.0)
                rankonemaster['One_day_followed_increasing_count'] = onemasterinfo[0].followed - onemasterinfo[
                    1].followed
                rankonemaster['to_current_followed_increasing'] = onemasterinfo[0].followed - onemasterinfo[-1].followed
                rankonemaster['trace_days'] = len(onemasterinfo)
                result.append(rankonemaster)
                continue
            if len(onemasterinfo) > 3:
                rankonemaster['Three_day_like_increasing'] = (onemasterinfo[0].likecount - onemasterinfo[
                    3].likecount) / (onemasterinfo[3].likecount * 1.0)
                rankonemaster['Three_day_like_increasing_count'] = onemasterinfo[0].likecount - onemasterinfo[
                    3].likecount
                rankonemaster['One_day_like_increasing'] = (onemasterinfo[0].likecount - onemasterinfo[1].likecount) / (
                            onemasterinfo[3].likecount * 1.0)
                rankonemaster['One_day_like_increasing_count'] = onemasterinfo[0].likecount - onemasterinfo[1].likecount
                rankonemaster['to_current_likecount_increasing'] = onemasterinfo[0].likecount - onemasterinfo[
                    -1].likecount

                rankonemaster['Three_day_followed_increasing'] = (onemasterinfo[0].followed - onemasterinfo[
                    3].followed) / (onemasterinfo[1].likecount * 1.0)
                rankonemaster['Three_day_followed_increasing_count'] = onemasterinfo[0].followed - onemasterinfo[
                    1].followed
                rankonemaster['One_day_followed_increasing'] = (onemasterinfo[0].followed - onemasterinfo[
                    3].followed) / (onemasterinfo[1].likecount * 1.0)
                rankonemaster['One_day_followed_increasing_count'] = onemasterinfo[0].followed - onemasterinfo[
                    1].followed
                rankonemaster['to_current_followed_increasing'] = onemasterinfo[0].followed - onemasterinfo[-1].followed
                rankonemaster['trace_days'] = len(onemasterinfo)
                result.append(rankonemaster)
                continue
        return result

    def get_video_rank(self):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        Videos = dbsession.query(Video).filter_by(isactivate=1).all()
        result = []
        for i in Videos:
            rankvideo = {}
            onevideoinfo = []
            onevideoinfos = dbsession.query(Videoinfo).filter_by(link=i.link).order_by(desc('updatetime')).all()
            fetchid = []
            print(len(onevideoinfos)==1)
            for it in onevideoinfos:
                if it.fatchid not in fetchid:
                    fetchid.append(it.fatchid)
                    onevideoinfo.append(it)
            if len(onevideoinfo) < 2:
                print(len(onevideoinfo),111)
                continue
            print(2222)
            rankvideo['link'] = i.link
            print(i.link)
            rankvideo['text'] = onevideoinfo[0].text
            rankvideo['one_day_likecount'] = onevideoinfo[0].likecount - onevideoinfo[1].likecount
            rankvideo['one_day_likecount_increasing'] = (onevideoinfo[0].likecount - onevideoinfo[1].likecount) / (
                        onevideoinfo[1].likecount * 1.0)
            rankvideo['one_day_comment'] = onevideoinfo[0].comment - onevideoinfo[1].comment
            rankvideo['one_day_collect'] = onevideoinfo[0].collect - onevideoinfo[1].collect
            rankvideo['follow_shot_bgm'] = onevideoinfo[0].follow_shot_bgm
            rankvideo['one_day_follow_shot_bgm_count'] = onevideoinfo[0].follow_shot_bgm_count - onevideoinfo[
                1].follow_shot_bgm_count
            rankvideo['Masternickname'] = dbsession.query(Masterinfo).filter_by(link = i.ownerlink).first().nickname
            rankvideo['Masterlink'] = i.ownerlink
            rankvideo['uploadtime'] = onevideoinfo[0].uploadtime.strftime('%Y-%m-%d')
            result.append(rankvideo)
        return result
    def get_video_base_info(self):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        Videos = dbsession.query(Video).filter_by(isactivate=1).all()
        result = []
        for i in Videos:
            onevideoinfo = dbsession.query(Videoinfo).filter_by(link=i.link).order_by(desc('updatetime')).first()
            if onevideoinfo is None:
                continue
            owner = dbsession.query(Masterinfo).filter_by(link=i.ownerlink).first().nickname
            result.append(onevideoinfo.to_json_owner(owner))
        return result
# if __name__ =='__main__':
#     ds = Diagramservice()
#     print(ds.get_video_rank())