import time
from datetime import datetime, timedelta

import selenium
from selenium.webdriver import ActionChains
from sqlalchemy import create_engine, update, desc, func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

import datautils
from app.models.Videoinfo import Videoinfo
from app.models.Video import Video
from app.models.Master import Master
from app.service.Driverservice import Driverservice


class Videoservice:
    def __init__(self):
        self.driverservice = Driverservice()
        self.driver = self.driverservice.start_webdriver_with_proxy('8.130.54.57:8112')
        self.engine = create_engine('mysql+mysqlconnector://root:root2333@8.130.54.57:3306/spider')

        pass

    def __del__(self):
        self.driver.quit()

    def get_video_baseinfo(self, link, ownerlink, fatchid=1):
        # driver = self.driverservice.start_webdriver_with_proxy('8.130.54.57:8112')
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.execute_script("window.open('');")
            self.driver.close()
        # self.driver.execute_script("window.localStorage.clear();")
        # self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.delete_all_cookies()
        self.driver.switch_to.window(all_windows[-1])
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        try:
            self.driver.get("https://www.douyin.com/video/" + link + '/')
        except (selenium.common.exceptions.TimeoutException) as e:

            print(e)
            return 'timeout'
        #   # 仅作为示例，根据需要定位到正确的元素
        time.sleep(3)
        try:
            if self.driver.find_element_by_class_name('QhoZcjgq').text=='你要观看的视频不存在':
                return 'video has been deleted'
        except:
            pass
        try:
            self.driver.find_element_by_class_name('dy-account-close').click()
        except:
            print("no close button")
        time.sleep(0.5)
        # 创建 ActionChains 对象
        actions = ActionChains(self.driver)
        actions.send_keys('h')  # 模拟按下 h 键
        actions.perform()
        # getbgmcounter = self.driver.find_element_by_class_name('wobrT4EE dy-tip-container')[3]
        #
        # getbgmcounter.click()
        element = self.driver.find_element_by_class_name("aSJB_0rh")  # 使用适当的选择器来定位元素

        # 使用 JavaScript 修改该元素的 display 属性
        self.driver.execute_script("arguments[0].style.display = 'flex';", element)
        time.sleep(1)
        try:
            self.driver.find_element_by_class_name("yjbA3Cby").click()
        except:
            print('此视频没有bgm信息')
            return 'no bgm'
        time.sleep(1)
        html = self.driver.page_source
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')
        follow_shot_bgm = soup.find_all(class_='LAtwBLze')[0].text

        follow_shot_bgm_count = soup.find_all(class_='n6JBqgGQ')[0].text
        likeset = soup.find_all(class_='xi78nG8b')[0]
        like = []  # 点赞，评论，收藏，转发
        for i in likeset:
            like.append(i.text)
        text = soup.find_all(class_='j5WZzJdp')[2].text
        uploadtime = soup.find_all(class_='D8UdT9V8')[0].text
        if like[0] == '赞':
            print(link, 'analysis fault')
            return 'analysis fault'

        videoinfo = Videoinfo(link=link, likecount=datautils.string2int(like[0]), ownerlink=ownerlink,
                              updatetime=datetime.now(), text=text,
                              comment=datautils.string2int(like[1]), follow_shot_bgm=follow_shot_bgm,
                              follow_shot_bgm_count=datautils.string2int(follow_shot_bgm_count[:-3]),
                              collect=datautils.string2int(like[2]),
                              uploadtime=datetime.fromisoformat(uploadtime[5:]), fatchid=fatchid)

        return videoinfo

    def addvideoinfo(self, videoinfo):
        if type(videoinfo) == list:
            Session = sessionmaker(bind=self.engine)
            dbsession = Session()
            for i in videoinfo:
                dbsession.add(i)
            dbsession.commit()
            dbsession.close()
            return
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        dbsession.add(videoinfo)
        dbsession.commit()
        dbsession.close()

    def videoinit(self, ownerlink):
        videolinks, top = self.getvideolist(ownerlink)
        followvideo_infos = []
        # 常规视频信息抽取
        for i in videolinks:
            info = self.get_video_baseinfo(i, ownerlink)
            if info=='no bgm':
                continue
            while info in ['timeout', 'analysis fault',None]:
                info = self.get_video_baseinfo(i, ownerlink)
            uploadtime = info.uploadtime
            if not datautils.is_within_three_days(uploadtime):
                break
            followvideo_infos.append(info)
        # 置顶视频信息抽取
        for i in top:
            info = self.get_video_baseinfo(i, ownerlink)
            if info=='no bgm':
                continue
            while info in ['timeout', 'analysis fault']:
                info = self.get_video_baseinfo(i, ownerlink)
            uploadtime = info.uploadtime
            if not datautils.is_within_three_days(uploadtime):
                break
            followvideo_infos.append(info)
        if len(followvideo_infos) == 0:
            print('该用户三天内未发布视频')
            return
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        for i in followvideo_infos:
            dbsession.add(i)
        dbsession.commit()
        # 抽取video元信息
        for i in followvideo_infos:
            video = Video(link=i.link, ownerlink=i.ownerlink, uploadtime=i.uploadtime, isactivate=1,
                          spiderbegin=datetime.now().date(), spiderend=datetime.now().date() + timedelta(days=3))
            dbsession.add(video)
        dbsession.commit()
        dbsession.close()

    def getvideolist(self, ownerlink):
        # driver = self.driverservice.start_webdriver_with_proxy('8.130.54.57:8112')
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.execute_script("window.open('');")
            self.driver.close()
        # self.driver.execute_script("window.localStorage.clear();")
        # self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.delete_all_cookies()
        self.driver.switch_to.window(all_windows[-1])
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get("https://v.douyin.com/" + ownerlink + '/')
        time.sleep(2)
        html = self.driver.page_source
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')
        videolinks = []
        top = []
        divs = soup.find_all('div', class_='LPv6KBIL')
        # 遍历找到的div标签
        for div in divs:
            # 在每个div中找到所有的a标签
            links = div.find_all('a')
            # for i in links[0].findAllNext():
            #     print(i.text)
            # 打印出所有a标签的href属性值（即链接）
            for link in links:
                line = link.get('href').split('?')[0].split('/')[-1]
                if 'note' in link.get('href'):
                    continue
                if link.text[:2] == '置顶':
                    print('置顶一只视频')
                    top.append(line)
                    continue
                videolinks.append(line)
        return videolinks, top

    def videoexpired(self):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        expiredvideos = dbsession.query(Video).where(Video.spiderend < datetime.now().date()).all()
        for i in expiredvideos:
            i.isactivate = 0

        # dup_links = dbsession.query(Video.link).group_by(Video.link).having(func.count(Video.id) > 1).all()
        #
        # for link, in dup_links:
        #     # 保留每个重复link的第一条记录，删除其余记录
        #     dup_records = dbsession.query(Video).filter(Video.link == link).order_by(Video.id).all()
        #     for record in dup_records[1:]:  # 保留第一条记录，删除其余记录
        #         dbsession.delete(record)
        dbsession.commit()
        dbsession.close()

    def videoupdate(self, ownerlink):
        Session = sessionmaker(bind=self.engine)
        dbsession = Session()
        latestvideo = dbsession.query(Video).filter_by(ownerlink=ownerlink).order_by(desc(Video.uploadtime)).first()
        if latestvideo is None:
            print(ownerlink,'没有已有视频，进入重新初始化进程')
            self.videoinit(ownerlink)
            return
        newvideo = []
        # latestlink = video.sort(key=Video.uploadtime)[0].link
        todayvideolist,todaytop = self.getvideolist(ownerlink)
        for i in todayvideolist:
            if datautils.is_later_than_latest(latestvideo.link,i):
                print(latestvideo.link,i)
                newvideo.append(i)
        for i in todaytop:
            if datautils.is_later_than_latest(latestvideo.link,i):
                print(latestvideo.link,i)
                newvideo.append(i)
        if len(newvideo)==0:
            print('无新视频')
            return
        videoinfo = []
        for i in newvideo:
            info = self.get_video_baseinfo(i, ownerlink)
            if info=='no bgm':
                continue
            while info in ['timeout', 'analysis fault', None]:
                info = self.get_video_baseinfo(i, ownerlink)
            videoinfo.append(info)
        # 抽取视频元信息
        for i in videoinfo:
            video = Video(link=i.link, ownerlink=i.ownerlink, uploadtime=i.uploadtime, isactivate=1,
                          spiderbegin=datetime.now().date(), spiderend=datetime.now().date() + timedelta(days=3))
            print(video.uploadtime)
            dbsession.add(video)
        dbsession.commit()
        dbsession.close()


if __name__ == '__main__':
    vs = Videoservice()
    Session = sessionmaker(bind=vs.engine)
    dbsession = Session()
    masters = dbsession.query(Master).filter_by(isactive=1).all()
    for i in masters:
        vs.videoupdate(i.link)
    vs.videoexpired()
    Session = sessionmaker(bind=vs.engine)
    dbsession = Session()
    videos = dbsession.query(Video).filter_by(isactivate =1 ).all()
    for i in videos:
        print(i.ownerlink,i.link)
        videobaseinfo = vs.get_video_baseinfo(i.link,i.ownerlink,int(datetime.now().strftime('%Y%m%d')))
        # videobaseinfo = vs.get_video_baseinfo(i.link,i.ownerlink,20240315)
        if videobaseinfo=='no bgm':
            continue
        while videobaseinfo in ['timeout', 'analysis fault',None]:
            videobaseinfo = vs.get_video_baseinfo(i.link,i.ownerlink,int(datetime.now().strftime('%Y%m%d')))
            # videobaseinfo = vs.get_video_baseinfo(i.link,i.ownerlink,20240315)
        if videobaseinfo=='video has been deleted':
            deletedvideo = dbsession.query(Video).filter_by(link = i.link).first()
            dbsession.delete(deletedvideo)
            continue
        vs.addvideoinfo(videobaseinfo)

