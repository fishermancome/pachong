#-*- coding:utf-8 -*-
import pymysql
import json

def getconn(host,port,user,passwd,db):
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
    if conn:
        return conn
    else:
        print("数据库连接失败")
        return None

def insert(conn,yonghu):
       cur = conn.cursor()
    cur.execute("insert into xiami (userid,imgsrc,nickname,time,upvote,downvote,content) values(%s,%s,%s,%s,%s,%s,%s)"  ,yonghu)
    conn.commit()

    
def mainn():
    host="localhost"
    port=3306
    user="root"
    password="hello"
    db="movie"
    conn = getconn(host,port,user,password,db)
    return conn



if __name__== "__main__":
    
    conn = mainn()
   # print(conn)
   
    

