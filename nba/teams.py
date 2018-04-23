# -*- coding:utf-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup
from dbutil import generate_id,insert_teams,get_teamid,insert_teamdetail,get_ename,insert_player
import time
def get_url(url):
    response = requests.get(url)
    return response.text


def get_teams(html):
    soup = BeautifulSoup(html,'lxml')
    a = soup.find_all(attrs={'class':'a_teamlink'})
    content = []
    #conn = return_conn()
    #获取球队
    for i in a:
        d = {'id':generate_id(),'url':i.get('href'),'ename':i.get('href').split('/')[-1],'cname':i.h2.get_text()}
        content.append(d)
    for item in content:
        team = (item['id'],item['url'],item['cname'],item['ename'])
        #insert_teams(team)
    #with open('nbda.txt','a',encoding='utf-8') as f:
        #f.write(json.dumps(content))
    #print(content)
    return content

def get_teamdetail(url):
    response = requests.get(url)
    html = response.text
    regstr = re.compile('<div class="content_a".*?p>(.*?)</p>.*?p>(.*?)</p>.*?href="(.*?)".*?/p>.*?p>(.*?)</p>',re.S)

    data = re.findall(regstr,html)
    for i in data:
        infoid = get_teamid(url.split('/')[-1])
        time = i[0].split('：')[-1]
        home = i[1].split('：')[1].split('&')[0]
        division =  i[1].split('：')[-1]
        homepage = i[2]
        headcoach = i[3].split('：')[-1]
        teamdetail = (infoid,time,home,division,homepage,headcoach)
        print(teamdetail)
        insert_teamdetail(teamdetail)
        
    #print(data)
    return data
#<p>(.*?)</p>.*?href="(.*?)".*?<p>(.*?)</p>    

#获取球员信息列表
def get_playerlist():
    namelist = get_ename()
    urllist = []
    for name in namelist:
        url = "https://nba.hupu.com/players/"+name
        response = get_url(url)
        
        regstr = re.compile('<td class="left">.*?<a target=.*?href="(.*?)".*?</td>',re.S)
        data = re.findall(regstr,response)
        urllist.append(data)
    return urllist

#将球员导入数据库  
def get_players():
    urllist = get_playerlist()
    for item in urllist:
        for j in item:
            response = get_url(j)
            regstr = re.compile('div class="team_data".*?h2>(.*?)</h2>.*?class="font">.*?p>(.*?)</p>.*?p>(.*?)</p>.*?'
                                +'p>(.*?)</p>.*?p>(.*?)</p>.*?p>(.*?)</p>.*?p>(.*?)</p>.*?p>(.*?)</p>.*?p>(.*?)</p>.*?p>(.*?)'
                                +'</p>.*?p>(.*?)</p>',re.S)
            data  = re.findall(regstr,response)
            
            print(j)
            for i in data:
                playerid = generate_id()
                name = i[0].strip()
                position = i[1].split('：')[-1]
                height = i[2].split('：')[-1]
                weight = i[3].split('：')[-1]
                birthday = i[4].split('：')[-1]
                belongteam = i[5][i[5].index('href'):].split("\"")[1].split('/')[-1]
                school = i[6].split('：')[-1]
                draft = i[7].split('：')[-1]
                nationality =  i[8].split('：')[-1]
                #salary = i[9].split('：')[-1]
                #contract = i[10].split('：')[-1]
                player = (playerid,name,position,height,weight,birthday,belongteam,school,draft,nationality)
                insert_player(player)
            time.sleep(5)
            
            
    
def main():
    url =  'https://nba.hupu.com/teams'
    response = get_url(url)
    content = get_teams(response)
    for i in content:
        dd = get_teamdetail(i['url'])
        print(dd)
        
if  __name__ == "__main__":
    '''url =  'https://nba.hupu.com/teams'
    html = get_url(url)
    get_teams(html)'''
    get_players()
    #main()
    #url = 'https://nba.hupu.com/teams/pelicans'
    #dd = get_teamdetail(url)
    
