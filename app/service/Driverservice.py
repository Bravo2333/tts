import time

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.firefox import GeckoDriverManager

class Driverservice:
    def __init__(self):
        pass

    def start_webdriver_with_proxy(self, proxy):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'sslProxy': proxy,
            'noProxy': ''  # 逗号分隔的地址列表，这些地址不使用代理
        })
        profile = webdriver.FirefoxProfile()
        # proxy.add_to_capabilities(webdriver.DesiredCapabilities.FIREFOX)


        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        profile.set_preference("general.useragent.override", user_agent)

        options = webdriver.FirefoxOptions()
        options.add_argument("-private")
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        path = GeckoDriverManager().install()
        # path = 'C:\\Users\\Administrator\\.wdm\\drivers\\geckodriver\\win64\\v0.34.0\\geckodriver.exe'
        print(path)
        return webdriver.Firefox(executable_path=path, options=options, firefox_profile=profile)