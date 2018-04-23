# -*- coding:utf-8 -*-

import requests
import json
import re

headers = {
    "Cookie":"gid=150156911229977; _xiamitoken=e2c075a1e9e62e2ceadd788070ae6af8; _unsign_token=9613f8a0e08b3178b3289bc1d9dd38b1; UM_distinctid=15d9c7e5ef5619-0b698d74fcb21b-8383667-100200-15d9c7e5ef63fb; cna=fXPiEX3FqkkCASSVQq27Uxia; XMPLAYER_addSongsToggler=0; XMPLAYER_isOpen=0; user_from=2; join_from=0zqfTI9Kv2Ew3f7BEdw; __XIAMI_SESSID=a42c53cc4bd44f286da3421902464568; login_method=mobilelogin; t_sign_auth=2; CNZZDATA921634=cnzz_eid%3D1839365572-1501658047-null%26ntime%3D1501658047; CNZZDATA2629111=cnzz_eid%3D29981898-1501658072-null%26ntime%3D1501658072; isg=AoqKZSC-50S4wmvpZG-szOiy23Ds0w--hPFAjBTDlF1qxy6B5AiJ5UMxowXg",
    "Referer":"http://www.xiami.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }


def get_param():
    url = "https://login.xiami.com/member/login"

    html = requests.get(url,headers=headers)
    #print(html.text)
    patstr = re.compile('<form method="post" action.*?name="_xiamitoken" value="(.*?)".*?value="(.*?)" '+
                        'name="done".*?src="(.*?)"',re.S)
    items = re.findall(patstr,html.text)
    print(items)
    token ,done,src = items[0]
    imgsrc = "https://login.xiami.com"+src
    with open('code.jpg','wb') as f:
        f.write(requests.get(imgsrc).content)
    return {"_xiamitoken":token,
            "done":done+"%2F%2F",
            }
    
def get_content():
    req = requests.get("http://www.xiami.com/index/collect?_=1501657522472",headers=headers)
    dd = json.loads(req.text)
    print(dd['data']['collects'])
    #print(req.text)
    return req.text


def login(username,password):
    a = get_param()
    a['account'] = username
    a['pw'] = password
    a['submit'] = "登 录"
    #vercode = input("输入验证码:")
    #a['verifycode'] = vercode
    session = requests.Session()
    loginurl = "https://login.xiami.com/passport/login"
    #req = session.post(loginurl,a,headers=headers)
    #print(req.status_code)
    #print(req.text)
    data = {"type":4}
    r = session.post("http://www.xiami.com/commentlist/turnpage/id/3381901/page/1/ajax/1",data,headers=headers)
    print(r.text)
if __name__ == "__main__":
    #get_content()
    #get_param()
    username = "15261825973"
    password = "1553853517c"
    login(username,password)
    
