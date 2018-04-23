# -*- coding:utf-8 -*-

import requests
import json
import time
import uuid
import sys
import random
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
from  dbutils import DB 
class Team:
    def __init__(self):
        self.headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


    def get_json(self,url):
        req = requests.get(url,headers=self.headers)
        
        data_json = req.text
        #data_json = req.text.encode('utf-8').decode('unicode_escape')
        #print(data_json)
        dictjson = json.loads(data_json)
        if len(dictjson['data']) > 0 :
            if len(dictjson['data']['teams']) > 0:
                teams = dictjson['data']['teams'][0]
                
                rowguid = uuid.uuid1()
                checkin_rate = teams['checkin_rate']
                description = teams['description'].replace("\\","").translate(non_bmp_map)
                print (type(description))
                if "\"" in description:
                    description  = "too long"
                    
                    
                total_rank = teams['total_rank']
                quota = teams['quota']
                rank = teams['rank']
                create_time = teams['create_time']
                welcome_msg = teams['welcome_msg'].translate(non_bmp_map)
                if "\"" in welcome_msg or "\\" in welcome_msg:
                    welcome_msg  = "too long"
                motto = teams['motto']
                if "\"" in motto or "\\" in motto:
                    motto  = "too long"
                next_badge_points = teams['next_badge_points']
                team_type = teams['team_type']
                name = teams['name'].translate(non_bmp_map)
                if "\"" in name or "\\" in name:
                    name  = "too long"
                _id = teams['id']
                tags = teams['id']
                points = teams['points']
                size = teams['size']
                weekly_points = teams['weekly_points']
                leader_id = teams['leader']['id']
                belongteamguid = rowguid
                username = teams['leader']['username'].translate(non_bmp_map)
                if "\"" in  username:
                    username = "too long"
                nickname = teams['leader']['nickname'].translate(non_bmp_map)
                if "\"" in nickname:
                    nickname  = "too long"
                timezone = teams['leader']['timezone']
                avatar = teams['leader']['avatar']

                singleTeam=(rowguid,checkin_rate,description,int(total_rank),int(quota),int(rank),
                                       welcome_msg,create_time,motto,int(next_badge_points),team_type,
                                       name,_id,tags,int(points),int(size),int(weekly_points),leader_id)
                leader = (belongteamguid,username,nickname,timezone,leader_id,avatar)
                db = DB()
                i = db.select_team(_id)
                if i < 1:
                    db.insert_team(singleTeam)
                j = db.select_leader(leader_id)
                if j< 1:
                    db.insert_leader(leader)
        
        





if __name__ == "__main__":
    t = Team()
    for i in range(80000,85900):
        url = 'https://www.shanbay.com/api/v1/team/?rank&page='+str(i)+'&ipp=1'
        print("################==========%d=="%i)
        try: 
            t.get_json(url)
        except requests.exceptions.ConnectionError:
            print("Connection refused by the server")
            print("let me sleep 5 seconds")
            print("ZZZZZZzzzzzzz...")
            time.sleep(5)
            continue
        #interval = random.randint(0,1)
        #time.sleep(interval)
    
    
