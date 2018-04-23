# -*- coding:utf-8 -*-

import re
import json
import requests
import time
from insertxiami import mainn,insert
headers = {
    "Cookie":"gid=150156911229977; _xiamitoken=e2c075a1e9e62e2ceadd788070ae6af8; _unsign_token=9613f8a0e08b3178b3289bc1d9dd38b1; UM_distinctid=15d9c7e5ef5619-0b698d74fcb21b-8383667-100200-15d9c7e5ef63fb; cna=fXPiEX3FqkkCASSVQq27Uxia; XMPLAYER_addSongsToggler=0; XMPLAYER_isOpen=0; user_from=2; join_from=0zqfTI9Kv2Ew3f7BEdw; __XIAMI_SESSID=a42c53cc4bd44f286da3421902464568; login_method=mobilelogin; t_sign_auth=2; CNZZDATA921634=cnzz_eid%3D1839365572-1501658047-null%26ntime%3D1501658047; CNZZDATA2629111=cnzz_eid%3D29981898-1501658072-null%26ntime%3D1501658072; isg=AoqKZSC-50S4wmvpZG-szOiy23Ds0w--hPFAjBTDlF1qxy6B5AiJ5UMxowXg",
    "Referer":"http://www.xiami.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

data ={
    "type":4
    }

def reg_str(html):
    regstr = re.compile('<li.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)">.*?time">(.*?)</span>.*?'
                        +'rel="0">(.*?)</a>.*?rel="0">(.*?)</a>.*?brief_\d+">(.*?)<br>',re.S)
    regstr1 = re.compile('<li.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)">.*?time">(.*?)</span>.*?rel="0">(.*?)</a>.*?rel="0">(.*?)</a>.*?brief_\d+">(.*?)<br>',re.S)
    items = re.findall(regstr1,html)
    print(items)
    for item in items:
        yield{
                "userid":item[0].split("/")[4],
                "imgsrc":item[1],
                "nickname":item[2],
                "time":item[3],
                "upvote":item[4],
                "downvote":item[5],
                "content":item[6]
            }
def pat_str(html):
    regstr = re.compile('<li.*?href="(.*?)".*?src="(.*?)".*?title="(.*?)".*?time">(.*?)</span>.*?rel="0">(.*?)</a>.*?rel="0">(.*?)</a>.*?brief_\d+">(.*?)<br>',re.S)
    items = re.findall(regstr,html)
    print(len(items))
    #print(items)
    for item in items:
        '''a = {
                "userid":item[0],
                "imgsrc":item[1],
                "nickname":item[2],
                "time":item[3],
                "upvote":item[4],
                "downvote":item[5],
                "content":item[6].strip()
            }
        print(a)'''
        yield{
                "userid":item[0].split('/')[4],
                "imgsrc":item[1],
                "nickname":item[2],
                "time":item[3],
                "upvote":item[4],
                "downvote":item[5],
                "content":item[6].strip()
            }
def write_txt(line):
    with open('file.txt','a+',encoding='utf-8') as f:
        f.write(line)
        
def get_detail(url):
    session = requests.Session()
    html = session.post(url,data,headers=headers).text
    #print(html)
    con = pat_str(html)
    for i in con:
        a = i['userid'],i['imgsrc'],i['nickname'],i['time'],i['upvote'],i['downvote'],i['content']
        print(a)
        conn = mainn()
        insert(conn,a)
        #jsons = json.loads(i)
       # write_txt(jsons)


def get_comment(page):
    if page == 1:
        url = "http://www.xiami.com/commentlist/turnpage/id/1795263120/page/1/ajax/1"
        get_detail(url)
    else:
        url = "http://www.xiami.com/commentlist/turnpage/id/1795263120/page/"+str(page)+"/ajax/1"
        get_detail(url)

if __name__ == "__main__":
    for i in range(1,200):
        time.sleep(5)
        
        get_comment(i)
        print("-------------------正在下载-------------------%d--------------------"%i)
