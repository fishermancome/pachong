from selenium import webdriver
import time
import requests
import random

from tutorial.tools.zhihu_sql import DBUtil

s = requests.Session()
s.headers.clear()
login_url = "https://www.zhihu.com/signin"
browser = webdriver.Chrome()
browser.get(login_url)

time.sleep(10)
username = input('input username')
password = input('input password')
browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input[name='username']").send_keys(username)
time.sleep(3)
browser.find_element_by_css_selector(".SignFlow-password input").send_keys(password)
time.sleep(2)
browser.find_element_by_css_selector("button[type='submit']").click()

time.sleep(10)

#获取cookie
cookies  = browser.get_cookies()
browser.quit()

for cookie in cookies:
    s.cookies.set(cookie['name'],cookie['value'])

def transferContent(content):
    if content is None:
        return None
    string = ""
    for c in content:
        if c =="'":
            string  += "\\\'"
        elif c == '"':
            string += '\\\"'
        elif c == "\\":
            string += '\\\\'
        elif c == "%":
            string += '%%'
        else :
            string += c
    return string

initial_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees'
html = s.get(initial_url).text
import json
json_dict = json.loads(html)
is_end = json_dict['paging']['is_end']
next_page = json_dict['paging']['next']
i = 0
while is_end is False:

    json_dict2 = json.loads(s.get(next_page).text)
    is_end = json_dict2['paging']['is_end']
    next_page = json_dict2['paging']['next']
    time.sleep(random.randint(5,10))
    print(json_dict2)
    data = json_dict2['data']
    for item in data:
        avatar_url_template = item['avatar_url_template']
        badge = item['badge']
        if len(badge) > 0:
            badge = []
        name = transferContent(item['name'])
        is_advertiser = item['is_advertiser']
        url = item['url']
        gender = item['gender']
        user_type = item['user_type']
        headline = transferContent(item['headline'])
        avatar_url = item['avatar_url']
        is_org = item['is_org']
        type = item['type']
        url_token = item['url_token']
        id = item['id']

        db = DBUtil('127.0.0.1', 3306, 'spider', 'root', '11111')
        flag = db.select(id)
        if flag:
            user = (
                avatar_url_template,badge,
                name,is_advertiser,url,
                gender,user_type,
                headline,avatar_url,
                is_org,type,
                url_token,id
            )
            db.insert(user)

    # i += 2
    # if i==20:
    #     break
