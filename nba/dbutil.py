#-*- coding:utf-8 -*-
import pymysql
import json
import string
import random

def getconn(host,port,user,passwd,db):
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
    if conn:
        #print('数据库连接成功')
        return conn
    else:
        print("数据库连接失败")
        return None

def insert_teams(team):
    conn = return_conn()
    cur = conn.cursor()
    cur.execute("insert into teams (id,url,cname,ename) values(%s,%s,%s,%s)"  ,team)
    conn.commit()

def insert_teamdetail(teamdetail):
    conn = return_conn()
    cur = conn.cursor()
    cur.execute("insert into teamdetail (infoid,timeofnba,home,division,homepage,headcoach) values(%s,%s,%s,%s,%s,%s)"  ,teamdetail)
    conn.commit()
    conn.close()

def insert_player(player):
    conn = return_conn()
    cur = conn.cursor()
    cur.execute("insert into players (playerid,name,position,height,weight,birthday,belongteam,school,draft,nationality)"
                +"values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",player)
    conn.commit()
    conn.close()

    
def return_conn():
    host="localhost"
    port=3306
    user="root"
    password="hello"
    db="nba"
    conn = getconn(host,port,user,password,db)
    return conn

def get_teamid(ename):
    conn = return_conn()
    cur = conn.cursor()
    cur.execute("select id from teams where ename = %s" ,ename)
    data = cur.fetchall()
    if len(data) > 0:
        #print(type(data[0][0]))
        print(data[0][0])
        return data[0][0]
    else:
        print("获取teamid失败")
        return None;

def get_ename():
    conn = return_conn()
    cur = conn.cursor()
    cur.execute("select  ename from teams ")
    data =  cur.fetchall()
    datalist = []
    for i in data:
        datalist.append(i[0])
    print(datalist)
    conn.close()
    return datalist
    
def generate_id(randomlength=14):
    strs = ''
    chars = string.ascii_letters+string.digits
    length = len(chars)-1
    for i in range(randomlength):
        strs += chars[random.randint(0,length)]
    return strs

if __name__== "__main__":
    ename = 'magic'
    #conn = mainn()
    #data = get_teamid(ename)
    #querymovie(conn)
    #cur = conn.cursor()
    get_ename()
    
    #cur.execute("select * from maoyantop100")
   #conn= getconn(host,port,user,password,db)
   # insert(conn,"12","12","12","12","13")

