import pymysql


def connect():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',  # 用户
        password='sb1234567890SB',
        database='government',
        port=3306,
        charset='utf8'
    )


# 定义数据库插入
def insert_or_update(sql):
    con = connect()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 定义数据库查找
def select_data(sql):
    con = connect()
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    con.close()
    return result

