# -*- coding:utf-8 -*-

import requests
import re
import os
import time
import random

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }

session = requests.Session()
email = input('input email:')
password = input('input password:')
data = {
    "redir":"https://www.douban.com/people/78578070/",
    "form_email":email,
    "form_password":password,
    "user_login":u"登录"
    }

def get_html(url):
    html = session.post(url,data,headers=headers)
    return html.text

def get_content(html):
    patstr =re.compile('<img id="captcha_image" src="(.*?)"',re.S)
    items = re.findall(patstr,html)
    print(items)
    captcha_image = items[0]
    captcha_id =captcha_image.split("id=")[1].split("&")[0]
    print(captcha_image,captcha_id)
    return captcha_image,captcha_id

def login(url):
    html = get_html(url)
    if "雨天的渔人" in html:
        return session
    else:
        captcha_image,captcha_id = get_content(html)
        data['captcha-id'] = captcha_id
        req = requests.get(captcha_image)
        with open('ma.jpg','wb') as f:
            f.write(req.content)
        captcha_solution = input("请输入验证码:\n")
        data['captcha-solution'] = captcha_solution
        #print(data)
        response = session.post(url,data,headers=headers)
        #print(response.text)
        return session

def get_piclist(html):
    regstr = re.compile('<li.*?cover.*?href="(.*?)"',re.S)
    items = re.findall(regstr,html)
    #print(items)
    return items

def get_pic(html):
    regstr = re.compile('class="mainphoto.*?img src="(.*?)"',re.S)
    items = re.findall(regstr,html)
    print(items)
    return items

def save(url,filedir):
    p =  requests.get(url)
    filename = url.split('/')[-1]
    with open(filedir+'/'+filename,'wb') as f:
        f.write(p.content)
    
if __name__ == "__main__":
    url = "https://accounts.douban.com/login"
    session = login(url)
    dirname = "xinhengjieyi"
    if os.path.exists(dirname) == False:
        os.mkdir(dirname)

    for i in range(39,42):
        baseurl = "https://movie.douban.com/celebrity/1018562/photos/?type=C&start="+str(i*40)+"&sortby=like&size=a&subtype=a"
        html = session.get(baseurl)
        items = get_piclist(html.text)

        print("正在下载第%d页............" %(i+1))
        for item in items:
            html = session.get(item)
            pics = get_pic(html.text)
            for pic in pics:
                save(pic,dirname)

            time.sleep(1)
        time.sleep(1)
            
    


