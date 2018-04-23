# -*- coding:utf-8 -*-

import pymysql
import json

class DB:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = 'root'
        self.passwd = 'hello'
        self.db = 'shanbei'
        self.charset='utf8'


    def getconn(self):
        conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
        if conn:
            return conn
        else:
            print("数据库连接失败")
            return None

    def insert_team(self,team): 
        conn = self.getconn()
        cur = conn.cursor()
        sql ='''insert into teams (rowguid,check_rate,description,total_rank,quota,
           rank,welcome_msg,create_time,motto,next_badge_points,team_type,name,
           id,tags,points,size,weekly_points,leader_id) values("%s","%s","%s",%d,%d,%d,"%s",
           "%s","%s",%d,"%s","%s","%s","%s",%d,%d,%d,"%s")''' %(team)
        print(sql)
        cur.execute(sql)
        conn.commit()

    def insert_leader(self,leader):
        conn = self.getconn()
        cur = conn.cursor()
        sql = '''insert into leaders(belongteamguid,username,nickname,timezone,id,avatar)
                 values("%s","%s","%s","%s","%s","%s")''' %(leader)
        print (sql)
        cur.execute(sql)
        conn.commit()

    def select_team(self,teamid):
        conn = self.getconn()
        cur = conn.cursor()
        sql = "select * from teams where id = '%s'" %teamid
        cur.execute(sql)
        data = cur.fetchall()
        return len(data)

    def select_leader(self,leader_id):
        conn = self.getconn()
        cur = conn.cursor()
        sql = "select * from leaders where id = '%s' "%leader_id
        cur.execute(sql)
        data = cur.fetchall()
        return len(data)
        
                          

if __name__ == "__main__":
    db = DB()
    conn = db.getconn()
    #team = ("asdf1","d","f's afdf",56,54,2,"dd","2014-12-24T19:11:04","ee",43,"edsf","sdf","we","wer",34,23,34,"34fe")
    #db.insert_team(team)
    #aa = db.select_team("we")
    #print(aa)

