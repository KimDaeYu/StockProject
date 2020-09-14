import pymysql

use_db = 'study_db'

def Connect_DB():
    con = pymysql.connect(
        user='root', 
        passwd='12345678',
        host='65.49.54.68', 
        db= use_db, 
        charset='utf8'
    )
    return con

def Get_DB():
    return use_db