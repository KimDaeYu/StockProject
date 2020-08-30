import pymysql
def Connect_DB():
    con = pymysql.connect(
        user='stock', 
        passwd='12345678',
        host='127.0.0.1', 
        db='study_db', 
        charset='utf8'
    )
    return con