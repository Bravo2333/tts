import time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datautils
from bs4 import BeautifulSoup
from app.models.Masterinfo import Masterinfo
from app.models.Master import Master

from app.service.Driverservice import Driverservice


class Masterservice:
    def __init__(self):
        self.driverservice = Driverservice()
        self.driver = self.driverservice.start_webdriver_with_proxy('8.130.54.57:8112')
        self.engine = create_engine('mysql+mysqlconnector://root:root2333@localhost:3306/spider')
        pass

    def __del__(self):
        self.driver.quit()

    def get_master_baseinfo(self, link):
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
        self.driver.get("https://v.douyin.com/" + link + '/')
        time.sleep(1)
        html = self.driver.page_source
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')
        # up = driver.find_element_by_class_name('SrsmYBkS R8fA8Vp7 b1kBsbLh').find_element_by_class_name('M7M0nmSI aKy92uTH Y7dISI5p')
        # results = soup.find_all(class_='SrsmYBkS R8fA8Vp7 b1kBsbLh')
        # 抽取达人信息
        nickname = soup.find_all(class_='j5WZzJdp')[0].text
        follow = soup.find_all(class_='sCnO6dhe')[0].text
        followed = soup.find_all(class_='sCnO6dhe')[1].text
        likecount = soup.find_all(class_='sCnO6dhe')[2].text
        account = soup.find_all(class_='TVGQz3SI')[0].text.split('：')[-1]
        ipaddress = soup.find_all(class_='W5BoFrmn')
        if len(ipaddress) == 0:
            ipaddress = None
        else:
            ipaddress = ipaddress[0].text.split('：')[-1]
        print(nickname)
        print(datautils.string2int(likecount))
        likecount = datautils.string2int(likecount)
        print(datautils.string2int(follow))
        follow = datautils.string2int(follow)
        print(datautils.string2int(followed))
        followed = datautils.string2int(followed)
        print(account)
        print(ipaddress)
        masterinfo = Masterinfo(nickname=nickname, likecount=likecount, follow=follow, followed=followed,
                                account=account,
                                ipaddress=ipaddress, link=link, updatetime=datetime.now())
        return masterinfo

    def addmasterinfo(self, masterinfo):
        if type(masterinfo) != list:
            Session = sessionmaker(bind=self.engine)
            dbsession = Session()
            dbsession.add(masterinfo)
            dbsession.commit()
            dbsession.close()
        else:
            Session = sessionmaker(bind=self.engine)
            dbsession = Session()
            for i in masterinfo:
                dbsession.add(i)
            dbsession.commit()
            dbsession.close()

    def masterinit(self, link):
        if type(link) != list:
            master = Master(link=link, isactive=1, deploydate=datetime.now())
            Session = sessionmaker(bind=self.engine)
            dbsession = Session()
            dbsession.add(master)
            dbsession.commit()
            dbsession.close()
        else:
            Session = sessionmaker(bind=self.engine)
            dbsession = Session()
            for i in link:
                master = Master(link=i, isactive=1, deploydate=datetime.now())
                dbsession.add(master)
            dbsession.commit()
            dbsession.close()


# if __name__ == '__main__':
#     ms = Masterservice()
#     Session = sessionmaker(bind=ms.engine)
#     dbsession = Session()
#     masters = dbsession.query(Master).filter_by(isactive=1).all()
#     for i in masters:
#         print(i.link)
#         mastersbaseinfo = None
#         while mastersbaseinfo == None:
#             try:
#                 mastersbaseinfo = ms.get_master_baseinfo(i.link)
#             except:
#                 mastersbaseinfo = None
#                 print('获取达人信息失败，重新获取')
#
#         ms.addmasterinfo(mastersbaseinfo)
