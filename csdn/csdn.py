import requests
import time
from scrapy.selector import Selector
from lxml import etree

class CSDN:
    def __init__(self,url):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.session = requests.Session()
        self.url = url

    def get_post_data(self,username,password):
        url = 'https://passport.csdn.net/account/login'
        page = self.session.get(url,headers=self.headers).text
        html = etree.HTML(page)
        lt = html.xpath('//*[@id="fm1"]/input[4]')[0].get('value')
        execution = html.xpath('//*[@id="fm1"]/input[5]')[0].get('value')
        post_data = {
            'username':username,
            'password':password,
            'lt':lt,
            'exection':execution,

        }
        return post_data

    def login(self,username,password):
        data = self.session.post(self.url,data=self.get_post_data(username,password),headers=self.headers)
        return self.session


if __name__ == '__main__':
    url = 'https://passport.csdn.net/account/verify'
    cs = CSDN(url)
    username = input("username:")
    password = input("password")
    session = cs.login(username,password)
    txt = session.get('https://blog.csdn.net/qq_26561265')
    print(txt.text)
