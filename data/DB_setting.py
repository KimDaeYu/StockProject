import pymysql

use_db = 'study_db'

def Connect_DB():
    con = pymysql.connect(
        user='stock', 
        passwd='12345678',
        host='127.0.0.1', 
        db= use_db, 
        charset='utf8'
    )
    return con

def Get_DB():
    return use_db