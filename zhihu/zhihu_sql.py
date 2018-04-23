import pymysql


class DBUtil:
    def __init__(self, host, port, db, user, password):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    def get_conn(self):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            db = self.db,
            user = self.user,
            password = self.password,
            charset = 'utf8'
        )
        if conn:
            return conn
        else:
            print('数据库连接失败')
            return None

    def insert(self,item):
        conn = self.get_conn()
        cur = conn.cursor()
        sql = '''insert into zhihu_user (
            avatar_url_template,badge,
            name,is_advertiser,url,
            gender,user_type,
            headline,avatar_url,
            is_org,type,
            url_token,id) 
            values('%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s','%s','%s')''' %item
        print(sql)
        cur.execute(sql,())
        conn.commit()

    def select(self,id):
        conn = self.get_conn()
        cur = conn.cursor()
        sql = "select count(1) from zhihu_user where id = '%s'" %id
        cur.execute(sql)
        fetch = cur.fetchall()
        if fetch[0][0] >0:
            return False
        else:
            return True






# if __name__=="__main__":
#     db = DBUtil('127.0.0.1',3306,'spider','root','11111')
#     item = ("a",'sdf','dsh','sdf','a',12,'sdf','sdf','a','sdf','sdf','a','sdfd')
#     print(db.select('sddsf'))